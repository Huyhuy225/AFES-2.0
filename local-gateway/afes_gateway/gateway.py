"""Core Local Gateway ingestion, validation, buffering, replay, and command routing."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

# Allow importing afes_sim contract validator without duplicating the JSON schema.
_SIM_PKG_ROOT = Path(__file__).resolve().parents[2] / "simulation" / "mqtt-publisher"
if _SIM_PKG_ROOT.is_dir() and str(_SIM_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_SIM_PKG_ROOT))

from afes_sim.validator import validate_telemetry, validate_topic  # noqa: E402

from .buffer import BoundedReplayBuffer
from .commands import CommandCheckResult, validate_downlink_command
from .config import GatewayConfig
from .dedup import DeduplicationCache


class UpstreamSink(Protocol):
    """Abstraction for forwarding validated telemetry/commands upstream or downstream."""

    def publish(self, topic: str, payload: dict[str, Any], qos: int = 1) -> None:
        ...


@dataclass(frozen=True)
class IngestOutcome:
    accepted: bool
    status: str  # "FORWARDED" | "BUFFERED" | "DUPLICATE" | "REJECTED"
    reason: str
    is_simulated: bool | None = None


class LocalGateway:
    """AFES 2.0 Local Gateway (T08)."""

    def __init__(self, config: GatewayConfig, upstream: UpstreamSink) -> None:
        self.config = config
        self.upstream = upstream
        self.dedup = DeduplicationCache(max_size=config.dedup_cache_size)
        self.buffer = BoundedReplayBuffer(max_size=config.buffer_max_size)
        self.upstream_connected: bool = True

        self.metrics: dict[str, int] = {
            "received": 0,
            "forwarded": 0,
            "buffered": 0,
            "replayed": 0,
            "duplicates": 0,
            "rejected": 0,
            "commands_routed": 0,
            "commands_rejected": 0,
        }

    def gateway_telemetry_topic(self, tenant_id: str | None = None) -> str:
        tenant = tenant_id or self.config.tenant_id
        return f"afes/v2/{tenant}/gateways/{self.config.gateway_id}/telemetry"

    def ingest_telemetry(
        self, payload: dict[str, Any], source_topic: str | None = None
    ) -> IngestOutcome:
        """Validate, deduplicate, and forward or buffer one telemetry packet."""
        self.metrics["received"] += 1

        # require_simulated=False so both Stage A (true) and Stage B (false) are accepted
        # while strictly preserving the simulation.is_simulated flag.
        result = validate_telemetry(payload, require_simulated=False)
        if not result.valid:
            self.metrics["rejected"] += 1
            return IngestOutcome(
                accepted=False,
                status="REJECTED",
                reason=result.summary(),
            )
        if source_topic is not None:
            topic_res = validate_topic(source_topic, payload)
            if not topic_res.valid:
                self.metrics["rejected"] += 1
                return IngestOutcome(
                    accepted=False,
                    status="REJECTED",
                    reason=topic_res.summary(),
                )

        device_id = payload["device"]["device_id"]
        message_id = payload["message_id"]
        is_simulated = bool(payload["simulation"]["is_simulated"])

        if self.dedup.seen_or_add(device_id, message_id):
            self.metrics["duplicates"] += 1
            return IngestOutcome(
                accepted=True,
                status="DUPLICATE",
                reason="DUPLICATE_MESSAGE_ID",
                is_simulated=is_simulated,
            )

        target_topic = self.gateway_telemetry_topic()
        if not self.upstream_connected:
            self.buffer.push(target_topic, payload)
            self.metrics["buffered"] += 1
            return IngestOutcome(
                accepted=True,
                status="BUFFERED",
                reason="UPSTREAM_DISCONNECTED",
                is_simulated=is_simulated,
            )

        try:
            self.upstream.publish(target_topic, payload, qos=1)
        except Exception as exc:  # noqa: BLE001
            self.upstream_connected = False
            self.buffer.push(target_topic, payload)
            self.metrics["buffered"] += 1
            return IngestOutcome(
                accepted=True,
                status="BUFFERED",
                reason=f"UPSTREAM_ERROR: {type(exc).__name__}",
                is_simulated=is_simulated,
            )

        self.metrics["forwarded"] += 1
        return IngestOutcome(
            accepted=True,
            status="FORWARDED",
            reason="OK",
            is_simulated=is_simulated,
        )

    def set_upstream_connected(self, connected: bool) -> int:
        """Update upstream connectivity state; on reconnect, replay buffered packets in order."""
        self.upstream_connected = connected
        if not connected or len(self.buffer) == 0:
            return 0

        replayed = 0
        pending = self.buffer.drain_in_order()
        for idx, env in enumerate(pending):
            try:
                self.upstream.publish(env.topic, env.payload, qos=1)
                replayed += 1
                self.metrics["replayed"] += 1
            except Exception:  # noqa: BLE001
                self.upstream_connected = False
                for remaining in pending[idx:]:
                    self.buffer.push(remaining.topic, remaining.payload)
                break
        return replayed

    def route_command(
        self, command: dict[str, Any], tenant_id: str | None = None
    ) -> CommandCheckResult:
        """Validate and route an authorized downlink command to a target device."""
        check = validate_downlink_command(command)
        if not check.allowed:
            self.metrics["commands_rejected"] += 1
            return check

        tenant = tenant_id or self.config.tenant_id
        device_id = command["target_device_id"]
        topic = f"afes/v2/{tenant}/devices/{device_id}/command/req"
        try:
            self.upstream.publish(topic, command, qos=1)
        except Exception as exc:  # noqa: BLE001
            self.upstream_connected = False
            self.metrics["commands_rejected"] += 1
            return CommandCheckResult(False, f"UPSTREAM_ERROR: {type(exc).__name__}")
        self.metrics["commands_routed"] += 1
        return check

    def health_snapshot(self) -> dict[str, Any]:
        """Return operational status without any credentials or secrets."""
        return {
            "status": "ok" if self.upstream_connected else "degraded",
            "upstream_connected": self.upstream_connected,
            "buffered_messages": len(self.buffer),
            "buffer_dropped": self.buffer.dropped_count,
            "dedup_cache_entries": len(self.dedup),
            "metrics": dict(self.metrics),
            "config": self.config.redacted_summary(),
        }
