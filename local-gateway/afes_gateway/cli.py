"""Minimal operations CLI for the AFES 2.0 Local Gateway (T08)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .config import GatewayConfig
from .coreiot import CoreIOTHttpSink
from .gateway import LocalGateway
from .health import create_health_server


class StdoutSink:
    """Offline sink that prints forwarded envelopes without secrets."""

    def publish(self, topic: str, payload: dict[str, Any], qos: int = 1) -> None:
        sim_flag = payload.get("simulation", {}).get("is_simulated")
        msg_id = payload.get("message_id") or payload.get("request_id")
        print(f"[GATEWAY] publish topic={topic} qos={qos} id={msg_id} is_simulated={sim_flag}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="afes_gateway",
        description="AFES 2.0 Local Gateway operations CLI (T08).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Print redacted gateway configuration and status.")

    val = sub.add_parser("validate", help="Ingest and validate a telemetry JSON file.")
    val.add_argument("file", type=Path, help="Path to telemetry JSON payload.")
    val.add_argument("--topic", default=None, help="Optional MQTT source topic.")

    srv = sub.add_parser("serve", help="Run the minimal HTTP health/status server.")
    srv.add_argument("--host", default=None, help="Bind host (default from config).")
    srv.add_argument("--port", type=int, default=None, help="Bind port (default from config).")

    push = sub.add_parser("push-coreiot", help="Validate and forward a telemetry JSON file to CoreIOT.")
    push.add_argument("file", type=Path, help="Path to telemetry JSON payload.")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    config = GatewayConfig.from_env()

    if args.command == "push-coreiot":
        sink = CoreIOTHttpSink(
            config.coreiot_base_url,
            config.coreiot_token,
            timeout_ms=config.coreiot_timeout_ms,
        )
        gateway = LocalGateway(config=config, upstream=sink)
        payload = json.loads(args.file.read_text(encoding="utf-8"))
        outcome = gateway.ingest_telemetry(payload)
        print(json.dumps({"accepted": outcome.accepted, "status": outcome.status, "reason": outcome.reason, "is_simulated": outcome.is_simulated}))
        return 0 if outcome.accepted and outcome.status == "FORWARDED" else 1

    gateway = LocalGateway(config=config, upstream=StdoutSink())

    if args.command == "status":
        print(json.dumps(gateway.health_snapshot(), indent=2))
        return 0

    if args.command == "validate":
        payload = json.loads(args.file.read_text(encoding="utf-8"))
        outcome = gateway.ingest_telemetry(payload, source_topic=args.topic)
        print(json.dumps({"accepted": outcome.accepted, "status": outcome.status, "reason": outcome.reason}))
        return 0 if outcome.accepted else 1

    if args.command == "serve":
        server = create_health_server(gateway, host=args.host, port=args.port)
        host, port = server.server_address
        print(f"[GATEWAY] Health endpoint listening on http://{host}:{port}/health")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return 0

    return 2
