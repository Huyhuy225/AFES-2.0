"""Automated unit and integration tests for Local Gateway T08 (Quality Gate 3)."""

from __future__ import annotations

import copy
import json
import sys
import threading
import unittest
import urllib.request
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_GW_ROOT = _REPO_ROOT / "local-gateway"
if str(_GW_ROOT) not in sys.path:
    sys.path.insert(0, str(_GW_ROOT))

from afes_gateway.config import GatewayConfig  # noqa: E402
from afes_gateway.coreiot import to_coreiot_telemetry  # noqa: E402
from afes_gateway.gateway import LocalGateway  # noqa: E402
from afes_gateway.health import create_health_server  # noqa: E402

_FIXTURES_DIR = _REPO_ROOT / "simulation" / "test-data" / "fixtures"


class RecordingSink:
    def __init__(self) -> None:
        self.published: list[tuple[str, dict[str, Any], int]] = []

    def publish(self, topic: str, payload: dict[str, Any], qos: int = 1) -> None:
        self.published.append((topic, payload, qos))


def _load_fixture(rel_path: str) -> dict[str, Any]:
    return json.loads((_FIXTURES_DIR / rel_path).read_text(encoding="utf-8"))


def _sample_command(**overrides: Any) -> dict[str, Any]:
    cmd: dict[str, Any] = {
        "schema_version": "2.0",
        "request_id": "cmd-d4b89211-12c8-4712-b13a-96ea9d880401",
        "target_device_id": "ESP32S3-Z1-01",
        "target_zone_id": "ZONE-A-FL1",
        "action": "PUMP_ON",
        "parameters": {"duration_ms": 15000, "override_safety_lock": False},
        "issuer": {"user_id": "usr-admin-01", "role": "ROLE_ADMIN"},
        "idempotency_key": "idemp-20261112-00412",
        "timestamp_epoch_ms": 1794456950000,
        "timeout_ms": 5000,
    }
    cmd.update(overrides)
    return cmd


class LocalGatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sink = RecordingSink()
        self.config = GatewayConfig(dedup_cache_size=16, buffer_max_size=3)
        self.gw = LocalGateway(self.config, self.sink)

    def test_valid_simulated_and_physical_telemetry_forward_and_preserve_flag(self) -> None:
        sim_pkt = _load_fixture("valid/stage_a_normal_seed6.json")
        res_sim = self.gw.ingest_telemetry(sim_pkt)
        self.assertTrue(res_sim.accepted)
        self.assertEqual(res_sim.status, "FORWARDED")
        self.assertTrue(res_sim.is_simulated)

        phys_pkt = copy.deepcopy(sim_pkt)
        phys_pkt["message_id"] = "f8e43477-84bc-40d1-9252-78d102e3b2e9"
        phys_pkt["device"]["device_id"] = "ESP32S3-YOLO-01"
        phys_pkt["device"]["device_type"] = "YOLO_UNO_S3"
        phys_pkt["device"]["mac_address"] = "34:85:18:11:22:33"
        phys_pkt["simulation"] = {
            "is_simulated": False,
            "scenario_id": None,
            "synthetic_noise_added": False,
        }
        res_phys = self.gw.ingest_telemetry(phys_pkt)
        self.assertTrue(res_phys.accepted)
        self.assertEqual(res_phys.status, "FORWARDED")
        self.assertFalse(res_phys.is_simulated)
        self.assertEqual(len(self.sink.published), 2)

    def test_invalid_payload_is_rejected_safely(self) -> None:
        bad_pkt = _load_fixture("invalid/missing_required_readings.json")
        res = self.gw.ingest_telemetry(bad_pkt)
        self.assertFalse(res.accepted)
        self.assertEqual(res.status, "REJECTED")
        self.assertEqual(len(self.sink.published), 0)
        self.assertEqual(self.gw.metrics["rejected"], 1)

    def test_duplicate_message_id_is_deduplicated(self) -> None:
        pkt = _load_fixture("valid/stage_a_normal_seed6.json")
        first = self.gw.ingest_telemetry(pkt)
        second = self.gw.ingest_telemetry(pkt)
        self.assertEqual(first.status, "FORWARDED")
        self.assertEqual(second.status, "DUPLICATE")
        self.assertEqual(len(self.sink.published), 1)
        self.assertEqual(self.gw.metrics["duplicates"], 1)

    def test_disconnect_buffers_and_reconnect_replays_in_order(self) -> None:
        base = _load_fixture("valid/stage_a_normal_seed6.json")
        self.gw.set_upstream_connected(False)

        uuids = [
            "11111111-1111-4111-8111-111111111111",
            "22222222-2222-4222-8222-222222222222",
            "33333333-3333-4333-8333-333333333333",
        ]
        for uid in uuids:
            pkt = copy.deepcopy(base)
            pkt["message_id"] = uid
            res = self.gw.ingest_telemetry(pkt)
            self.assertEqual(res.status, "BUFFERED")

        self.assertEqual(len(self.sink.published), 0)
        replayed = self.gw.set_upstream_connected(True)
        self.assertEqual(replayed, 3)
        self.assertEqual([p[1]["message_id"] for p in self.sink.published], uuids)

    def test_command_authorization_and_unsafe_rejection(self) -> None:
        ok_res = self.gw.route_command(_sample_command())
        self.assertTrue(ok_res.allowed)

        bad_action = self.gw.route_command(_sample_command(action="FORMAT_FLASH"))
        self.assertFalse(bad_action.allowed)
        self.assertEqual(bad_action.reason, "UNPERMITTED_ACTION")

        bad_role = self.gw.route_command(
            _sample_command(issuer={"user_id": "guest", "role": "ROLE_VIEWER"})
        )
        self.assertFalse(bad_role.allowed)
        self.assertEqual(bad_role.reason, "UNAUTHORIZED_ROLE")

        unsafe_override = self.gw.route_command(
            _sample_command(
                issuer={"user_id": "op-1", "role": "ROLE_OPERATOR"},
                parameters={"duration_ms": 5000, "override_safety_lock": True},
            )
        )
        self.assertFalse(unsafe_override.allowed)
        self.assertEqual(unsafe_override.reason, "UNSAFE_SAFETY_OVERRIDE")
        self.assertEqual(self.gw.metrics["commands_routed"], 1)
        self.assertEqual(self.gw.metrics["commands_rejected"], 3)

    def test_health_endpoint_exposes_status_without_secrets(self) -> None:
        server = create_health_server(self.gw, host="127.0.0.1", port=0)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode("utf-8")
                data = json.loads(body)
                self.assertEqual(data["status"], "ok")
                self.assertNotIn("mqtt_password", body)
                self.assertNotIn("placeholder_local_mqtt_password", body)
                self.assertNotIn("coreiot_token\"", body)
        finally:
            server.shutdown()
            server.server_close()

    def test_coreiot_mapping_preserves_simulation_flag_and_readings(self) -> None:
        pkt = _load_fixture("valid/stage_a_normal_seed6.json")
        mapped = to_coreiot_telemetry(pkt)
        self.assertEqual(mapped["ts"], pkt["timestamps"]["timestamp_epoch_ms"])
        self.assertTrue(mapped["values"]["is_simulated"])
        self.assertEqual(mapped["values"]["device_id"], "SIM-ESP32-101")
        self.assertIn("temperature", mapped["values"])
        self.assertIn("smoke_ppm", mapped["values"])


if __name__ == "__main__":
    unittest.main()
