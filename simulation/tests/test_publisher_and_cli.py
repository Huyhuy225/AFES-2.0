"""Tests for Stage A publisher, mocked MQTT transport, and CLI entrypoints."""

from __future__ import annotations

import copy
import io
import json
import sys
import unittest
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PUBLISHER_DIR = str(_REPO_ROOT / "simulation" / "mqtt-publisher")
if _PUBLISHER_DIR not in sys.path:
    sys.path.insert(0, _PUBLISHER_DIR)

from afes_sim import (  # noqa: E402
    STAGE_A_BANNER,
    TELEMETRY_QOS,
    TELEMETRY_RETAIN,
    ContractRejectionError,
    MemoryTransport,
    PahoMqttTransport,
    PublishTransportError,
    SimulatorConfig,
    StdoutTransport,
    TelemetryGenerator,
    TelemetryPublisher,
)
from afes_sim.cli import main as cli_main  # noqa: E402

VALID_FIXTURES_DIR = _REPO_ROOT / "simulation" / "test-data" / "fixtures" / "valid"
INVALID_FIXTURES_DIR = _REPO_ROOT / "simulation" / "test-data" / "fixtures" / "invalid"


class _FakePublishInfo:
    def __init__(self, rc: int = 0, published: bool = True) -> None:
        self.rc = rc
        self._published = published
        self.wait_Timeouts: list[float | None] = []

    def wait_for_publish(self, timeout: float | None = None) -> None:
        self.wait_Timeouts.append(timeout)

    def is_published(self) -> bool:
        return self._published


class _FakePahoClient:
    def __init__(
        self,
        client_id: str,
        *,
        fail_connect_attempts: int = 0,
        fail_publish_calls: set[int] | None = None,
    ) -> None:
        self.client_id = client_id
        self.fail_connect_attempts = fail_connect_attempts
        self.fail_publish_calls = set(fail_publish_calls or ())
        self.connect_calls: list[tuple[str, int, int]] = []
        self.publish_calls: list[tuple[str, bytes, int, bool]] = []
        self.auth: tuple[str, str | None] | None = None
        self.tls_ca_certs: str | None = None
        self.tls_configured = False
        self.loop_started = 0
        self.loop_stopped = 0
        self.disconnected = 0
        self._publish_attempt = 0

    def username_pw_set(self, username: str, password: str | None = None) -> None:
        self.auth = (username, password)

    def tls_set(self, ca_certs: str | None = None) -> None:
        self.tls_configured = True
        self.tls_ca_certs = ca_certs

    def connect(self, host: str, port: int, keepalive: int) -> int:
        self.connect_calls.append((host, port, keepalive))
        if len(self.connect_calls) <= self.fail_connect_attempts:
            raise ConnectionRefusedError("simulated broker unavailable")
        return 0

    def loop_start(self) -> None:
        self.loop_started += 1

    def loop_stop(self) -> None:
        self.loop_stopped += 1

    def disconnect(self) -> None:
        self.disconnected += 1

    def publish(
        self,
        topic: str,
        payload: bytes,
        qos: int = 0,
        retain: bool = False,
    ) -> _FakePublishInfo:
        self._publish_attempt += 1
        if self._publish_attempt in self.fail_publish_calls:
            return _FakePublishInfo(rc=4, published=False)
        self.publish_calls.append((topic, bytes(payload), qos, retain))
        return _FakePublishInfo(rc=0, published=True)


class PublisherAndCliTests(unittest.TestCase):
    def test_memory_transport_publishes_qos1_and_validates_every_packet(self) -> None:
        cfg = SimulatorConfig(fixture_mode=True, scenario="critical-fire", count=4)
        transport = MemoryTransport()
        sleeps: list[float] = []
        publisher = TelemetryPublisher(cfg, transport, sleep_fn=sleeps.append)
        summary = publisher.publish_payloads()

        self.assertEqual(summary.stage_label, STAGE_A_BANNER)
        self.assertEqual(summary.transport_name, "memory")
        self.assertEqual(summary.topic, "afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry")
        self.assertEqual(summary.qos, TELEMETRY_QOS)
        self.assertEqual(summary.retain, TELEMETRY_RETAIN)
        self.assertEqual(summary.count_published, 4)
        self.assertEqual(len(transport.messages), 4)
        self.assertEqual(transport.connect_calls, 1)
        self.assertEqual(transport.close_calls, 1)
        self.assertEqual(sleeps, [2.0, 2.0, 2.0])

        for topic, raw_bytes, qos, retain in transport.messages:
            self.assertEqual(topic, cfg.topic)
            self.assertEqual(qos, 1)
            self.assertFalse(retain)
            decoded = json.loads(raw_bytes.decode("utf-8"))
            self.assertIs(decoded["simulation"]["is_simulated"], True)

    def test_publisher_rejects_unmarked_or_invalid_payload_before_transport(self) -> None:
        cfg = SimulatorConfig(fixture_mode=True, scenario="normal", count=1)
        valid_payload = TelemetryGenerator(cfg).next_payload()

        # Case 1: simulation.is_simulated set to False
        unmarked = copy.deepcopy(valid_payload)
        unmarked["simulation"]["is_simulated"] = False
        transport1 = MemoryTransport()
        pub1 = TelemetryPublisher(cfg, transport1)
        with self.assertRaises(ContractRejectionError):
            pub1.publish_payloads([unmarked], count=1)
        self.assertEqual(len(transport1.messages), 0)
        self.assertEqual(transport1.close_calls, 1)

        # Case 2: payload device_id mismatches topic device_id
        mismatched = copy.deepcopy(valid_payload)
        mismatched["device"]["device_id"] = "SIM-OTHER-999"
        transport2 = MemoryTransport()
        pub2 = TelemetryPublisher(cfg, transport2)
        with self.assertRaises(ContractRejectionError):
            pub2.publish_payloads([mismatched], count=1)
        self.assertEqual(len(transport2.messages), 0)
        self.assertEqual(transport2.close_calls, 1)

    def test_stdout_transport_labels_each_line_as_stage_a_simulation(self) -> None:
        cfg = SimulatorConfig(fixture_mode=True, scenario="warning-smoke", count=2)
        buf = io.StringIO()
        transport = StdoutTransport(stream=buf)
        TelemetryPublisher(cfg, transport).publish_payloads()

        lines = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
        self.assertEqual(len(lines), 2)
        for line in lines:
            envelope = json.loads(line)
            self.assertEqual(envelope["stage_label"], STAGE_A_BANNER)
            self.assertEqual(envelope["qos"], 1)
            self.assertFalse(envelope["retain"])
            self.assertIs(envelope["payload"]["simulation"]["is_simulated"], True)

    def test_paho_mqtt_transport_retries_connect_and_recovers_mid_publish(self) -> None:
        cfg = SimulatorConfig(
            fixture_mode=True,
            scenario="normal",
            count=2,
            mqtt_host="localhost",
            mqtt_port=1883,
            mqtt_username="placeholder_mqtt_user",
            mqtt_pass="placeholder_local_mqtt_password",
            mqtt_tls=True,
            mqtt_tls_ca_file="ca.crt",
            mqtt_connect_attempts=3,
            mqtt_retry_backoff_s=0.5,
        )
        created_clients: list[_FakePahoClient] = []
        backoff_sleeps: list[float] = []

        def factory(client_id: str) -> Any:
            # Fail 1st connect attempt, succeed on 2nd; fail 1st publish to trigger reconnect.
            client = _FakePahoClient(
                client_id,
                fail_connect_attempts=1,
                fail_publish_calls={1},
            )
            created_clients.append(client)
            return client

        transport = PahoMqttTransport(cfg, client_factory=factory, sleep_fn=backoff_sleeps.append)
        summary = TelemetryPublisher(cfg, transport).publish_payloads()

        self.assertEqual(summary.count_published, 2)
        self.assertEqual(len(created_clients), 1)
        fake = created_clients[0]
        self.assertEqual(fake.client_id, "afes-stage-a-sim-SIM-ESP32-101")
        self.assertEqual(
            fake.auth, ("placeholder_mqtt_user", "placeholder_local_mqtt_password")
        )
        self.assertTrue(fake.tls_configured)
        self.assertEqual(fake.tls_ca_certs, "ca.crt")
        self.assertEqual(len(fake.connect_calls), 3)  # 2 initial (1 fail + 1 ok) + 1 reconnect
        self.assertEqual(len(fake.publish_calls), 2)
        self.assertEqual(backoff_sleeps, [0.5])
        self.assertGreaterEqual(fake.disconnected, 1)

    def test_paho_mqtt_transport_raises_safe_error_when_broker_unavailable(self) -> None:
        cfg = SimulatorConfig(
            fixture_mode=True,
            mqtt_host="localhost",
            mqtt_port=1883,
            mqtt_username="placeholder_mqtt_user",
            mqtt_pass="placeholder_secret_value",
            mqtt_connect_attempts=2,
            mqtt_retry_backoff_s=0.25,
        )
        sleeps: list[float] = []
        transport = PahoMqttTransport(
            cfg,
            client_factory=lambda cid: _FakePahoClient(cid, fail_connect_attempts=5),
            sleep_fn=sleeps.append,
        )
        with self.assertRaises(PublishTransportError) as ctx:
            TelemetryPublisher(cfg, transport).publish_payloads()

        err_text = str(ctx.exception)
        self.assertIn("localhost:1883", err_text)
        self.assertNotIn("placeholder_secret_value", err_text)
        self.assertEqual(sleeps, [0.25])

    def test_cli_publish_and_validate_subcommands(self) -> None:
        out_pub, err_pub = io.StringIO(), io.StringIO()
        rc_pub = cli_main(
            [
                "publish",
                "--fixture-mode",
                "--scenario",
                "normal",
                "--count",
                "2",
                "--transport",
                "stdout",
            ],
            stdout=out_pub,
            stderr=err_pub,
        )
        self.assertEqual(rc_pub, 0, err_pub.getvalue())
        self.assertIn(STAGE_A_BANNER, err_pub.getvalue())
        self.assertEqual(len(out_pub.getvalue().strip().splitlines()), 2)

        out_val, err_val = io.StringIO(), io.StringIO()
        valid_paths = [str(p) for p in sorted(VALID_FIXTURES_DIR.glob("*.*"))]
        rc_val = cli_main(["validate", *valid_paths], stdout=out_val, stderr=err_val)
        self.assertEqual(rc_val, 0, err_val.getvalue())
        self.assertIn("VALID", out_val.getvalue())

        out_inv, err_inv = io.StringIO(), io.StringIO()
        rc_inv = cli_main(
            ["validate", str(INVALID_FIXTURES_DIR / "timestamp_epoch_mismatch.json")],
            stdout=out_inv,
            stderr=err_inv,
        )
        self.assertEqual(rc_inv, 1)
        self.assertIn("PROFILE_TIMESTAMP_MISMATCH", err_inv.getvalue())


if __name__ == "__main__":
    unittest.main()
