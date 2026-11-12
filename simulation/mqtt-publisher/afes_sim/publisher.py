"""Stage A virtual telemetry publisher and transport abstractions.

Offline transports (``MemoryTransport`` and ``StdoutTransport``) require only
the Python standard library and never open network sockets. The optional
``PahoMqttTransport`` uses ``paho-mqtt`` only when explicitly selected via
``--transport mqtt`` (or instantiated directly) and handles unavailable brokers,
bounded connection retries, and mid-run disconnects safely without exposing
credentials in error messages.

Every payload is validated against the AFES v2 telemetry contract and Stage A
simulation profile before it reaches any transport.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Protocol, TextIO

from .config import SimulatorConfig
from .generator import TelemetryGenerator
from .topics import TELEMETRY_QOS, TELEMETRY_RETAIN
from .validator import validate_telemetry, validate_topic

STAGE_A_BANNER = "[SIMULATED - STAGE A]"


class PublishTransportError(RuntimeError):
    """Raised when the underlying transport cannot connect or publish."""


class ContractRejectionError(ValueError):
    """Raised when a payload or topic fails Stage A contract validation."""


@dataclass(frozen=True)
class PublishedRecord:
    sequence: int
    topic: str
    qos: int
    retain: bool
    payload: dict[str, Any]
    raw_json: str
    stage_label: str = STAGE_A_BANNER


@dataclass(frozen=True)
class PublishRunSummary:
    stage_label: str
    transport_name: str
    topic: str
    qos: int
    retain: bool
    scenario: str
    seed: int | None
    count_requested: int
    count_published: int
    records: tuple[PublishedRecord, ...]


class Transport(Protocol):
    name: str

    def connect(self) -> None: ...

    def publish(
        self,
        topic: str,
        payload_bytes: bytes,
        *,
        qos: int = TELEMETRY_QOS,
        retain: bool = TELEMETRY_RETAIN,
    ) -> None: ...

    def close(self) -> None: ...


class MemoryTransport:
    """In-memory fake transport for offline contract and publisher tests."""

    name = "memory"

    def __init__(
        self,
        *,
        fail_connect_times: int = 0,
        fail_on_publish_indices: set[int] | None = None,
    ) -> None:
        self.fail_connect_times = fail_connect_times
        self.fail_on_publish_indices = set(fail_on_publish_indices or ())
        self.connect_calls = 0
        self.close_calls = 0
        self.connected = False
        self.messages: list[tuple[str, bytes, int, bool]] = []

    def connect(self) -> None:
        self.connect_calls += 1
        if self.connect_calls <= self.fail_connect_times:
            raise PublishTransportError(
                f"memory transport simulated connect failure ({self.connect_calls}/{self.fail_connect_times})"
            )
        self.connected = True

    def publish(
        self,
        topic: str,
        payload_bytes: bytes,
        *,
        qos: int = TELEMETRY_QOS,
        retain: bool = TELEMETRY_RETAIN,
    ) -> None:
        if not self.connected:
            raise PublishTransportError("cannot publish on disconnected memory transport")
        idx = len(self.messages)
        if idx in self.fail_on_publish_indices:
            raise PublishTransportError(f"memory transport simulated publish failure at index {idx}")
        self.messages.append((topic, bytes(payload_bytes), qos, retain))

    def close(self) -> None:
        self.close_calls += 1
        self.connected = False


class StdoutTransport:
    """Offline stream transport that labels every frame as Stage A simulation."""

    name = "stdout"

    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream = sys.stdout if stream is None else stream
        self.connected = False
        self.published_count = 0

    def connect(self) -> None:
        self.connected = True

    def publish(
        self,
        topic: str,
        payload_bytes: bytes,
        *,
        qos: int = TELEMETRY_QOS,
        retain: bool = TELEMETRY_RETAIN,
    ) -> None:
        if not self.connected:
            raise PublishTransportError("stdout transport is not connected")
        envelope = {
            "stage_label": STAGE_A_BANNER,
            "transport": "stdout-offline",
            "topic": topic,
            "qos": qos,
            "retain": retain,
            "payload": json.loads(payload_bytes.decode("utf-8")),
        }
        self._stream.write(json.dumps(envelope, separators=(",", ":")) + "\n")
        self._stream.flush()
        self.published_count += 1

    def close(self) -> None:
        self.connected = False


def _default_paho_client_factory(client_id: str) -> Any:
    try:
        import paho.mqtt.client as mqtt  # type: ignore[import-untyped]
    except ImportError as exc:
        raise PublishTransportError(
            "paho-mqtt is not installed; install simulation/mqtt-publisher/requirements.txt "
            "or use --transport stdout / --transport memory for offline validation"
        ) from exc

    callback_api = getattr(mqtt, "CallbackAPIVersion", None)
    if callback_api is not None:
        return mqtt.Client(callback_api.VERSION2, client_id=client_id)
    return mqtt.Client(client_id=client_id)


class PahoMqttTransport:
    """Optional MQTT v3.1.1 transport with bounded retry and safe error reporting."""

    name = "mqtt"

    def __init__(
        self,
        config: SimulatorConfig,
        *,
        client_factory: Callable[[str], Any] | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        self._client_factory = client_factory or _default_paho_client_factory
        self._sleep = sleep_fn
        self._client: Any | None = None
        self.connected = False

    def _configure_client(self, client: Any) -> None:
        cfg = self.config
        if hasattr(client, "socket_timeout"):
            client.socket_timeout = cfg.mqtt_connect_timeout_s
        if cfg.mqtt_username or cfg.mqtt_pass:
            client.username_pw_set(cfg.mqtt_username, cfg.mqtt_pass or None)
        if cfg.mqtt_tls:
            ca_certs = cfg.mqtt_tls_ca_file or None
            client.tls_set(ca_certs=ca_certs)

    def _attempt_connect_loop(self, client: Any) -> None:
        cfg = self.config
        attempts = max(1, cfg.mqtt_connect_attempts)
        last_exc: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                rc = client.connect(cfg.mqtt_host, cfg.mqtt_port, cfg.mqtt_keepalive_s)
                if isinstance(rc, int) and rc != 0:
                    raise OSError(f"MQTT broker returned non-zero CONNACK rc={rc}")
                if hasattr(client, "loop_start"):
                    client.loop_start()
                self.connected = True
                return
            except Exception as exc:  # noqa: BLE001 - normalize transport failures safely
                last_exc = exc
                if attempt < attempts and cfg.mqtt_retry_backoff_s > 0:
                    self._sleep(cfg.mqtt_retry_backoff_s * attempt)
        raise PublishTransportError(
            f"unable to connect to MQTT broker {cfg.mqtt_host}:{cfg.mqtt_port} "
            f"after {attempts} attempt(s): {type(last_exc).__name__}: {last_exc}"
        ) from last_exc

    def connect(self) -> None:
        client = self._client_factory(self.config.effective_client_id)
        self._configure_client(client)
        self._client = client
        self._attempt_connect_loop(client)

    def _publish_once(
        self,
        topic: str,
        payload_bytes: bytes,
        *,
        qos: int,
        retain: bool,
    ) -> None:
        assert self._client is not None
        info = self._client.publish(topic, payload_bytes, qos=qos, retain=retain)
        rc = getattr(info, "rc", 0)
        if isinstance(rc, int) and rc != 0:
            raise OSError(f"MQTT publish returned non-zero rc={rc}")
        wait_fn = getattr(info, "wait_for_publish", None)
        if callable(wait_fn):
            wait_fn(timeout=self.config.mqtt_connect_timeout_s)
        is_published = getattr(info, "is_published", None)
        if callable(is_published) and not is_published():
            raise TimeoutError("MQTT QoS acknowledgment timed out before completion")

    def publish(
        self,
        topic: str,
        payload_bytes: bytes,
        *,
        qos: int = TELEMETRY_QOS,
        retain: bool = TELEMETRY_RETAIN,
    ) -> None:
        if not self.connected or self._client is None:
            raise PublishTransportError("MQTT transport is not connected")
        try:
            self._publish_once(topic, payload_bytes, qos=qos, retain=retain)
        except Exception as first_exc:  # noqa: BLE001 - attempt one bounded reconnect
            self.connected = False
            try:
                if hasattr(self._client, "loop_stop"):
                    self._client.loop_stop()
                self._attempt_connect_loop(self._client)
                self._publish_once(topic, payload_bytes, qos=qos, retain=retain)
            except Exception as retry_exc:  # noqa: BLE001
                raise PublishTransportError(
                    f"MQTT publish failed on topic {topic!r} after reconnect attempt: "
                    f"{type(retry_exc).__name__}: {retry_exc}"
                ) from first_exc

    def close(self) -> None:
        client, self._client = self._client, None
        self.connected = False
        if client is None:
            return
        try:
            if hasattr(client, "loop_stop"):
                client.loop_stop()
        finally:
            if hasattr(client, "disconnect"):
                client.disconnect()


class TelemetryPublisher:
    """Validates and publishes Stage A virtual telemetry over a configured transport."""

    def __init__(
        self,
        config: SimulatorConfig,
        transport: Transport,
        *,
        generator: TelemetryGenerator | None = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        self.config = config
        self.transport = transport
        self.generator = generator or TelemetryGenerator(config)
        self._sleep_fn = sleep_fn

    def publish_payloads(
        self,
        payloads: Iterable[dict[str, Any]] | None = None,
        *,
        count: int | None = None,
    ) -> PublishRunSummary:
        requested = self.config.count if count is None else count
        source = self.generator.generate(requested) if payloads is None else payloads
        topic = self.config.topic
        records: list[PublishedRecord] = []

        self.transport.connect()
        try:
            for seq, payload in enumerate(source):
                payload_check = validate_telemetry(payload, require_simulated=True)
                if not payload_check.valid:
                    raise ContractRejectionError(
                        f"refusing to publish contract-invalid Stage A payload #{seq}: "
                        f"{payload_check.summary()}"
                    )
                topic_check = validate_topic(topic, payload)
                if not topic_check.valid:
                    raise ContractRejectionError(
                        f"refusing to publish on invalid topic {topic!r}: "
                        f"{topic_check.summary()}"
                    )

                raw_json = json.dumps(payload, separators=(",", ":"), sort_keys=False)
                self.transport.publish(
                    topic,
                    raw_json.encode("utf-8"),
                    qos=TELEMETRY_QOS,
                    retain=TELEMETRY_RETAIN,
                )
                records.append(
                    PublishedRecord(
                        sequence=seq,
                        topic=topic,
                        qos=TELEMETRY_QOS,
                        retain=TELEMETRY_RETAIN,
                        payload=payload,
                        raw_json=raw_json,
                    )
                )
                if self._sleep_fn is not None and seq + 1 < requested:
                    self._sleep_fn(self.config.interval_ms / 1000.0)
        finally:
            self.transport.close()

        return PublishRunSummary(
            stage_label=STAGE_A_BANNER,
            transport_name=self.transport.name,
            topic=topic,
            qos=TELEMETRY_QOS,
            retain=TELEMETRY_RETAIN,
            scenario=self.config.scenario,
            seed=self.config.effective_seed,
            count_requested=requested,
            count_published=len(records),
            records=tuple(records),
        )
