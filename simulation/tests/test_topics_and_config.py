"""Tests for AFES v2 MQTT topic construction and environment configuration."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PUBLISHER_DIR = str(_REPO_ROOT / "simulation" / "mqtt-publisher")
if _PUBLISHER_DIR not in sys.path:
    sys.path.insert(0, _PUBLISHER_DIR)

from afes_sim import (  # noqa: E402
     TELEMETRY_QOS,
    TELEMETRY_RETAIN,
    ConfigError,
    SimulatorConfig,
    TelemetryGenerator,
    TopicError,
    load_env_file,
    parse_telemetry_topic,
    telemetry_topic,
    validate_topic,
)


class TopicsAndConfigTests(unittest.TestCase):
    def test_telemetry_topic_construction_and_parsing(self) -> None:
        topic = telemetry_topic("hcmut-lab", "SIM-ESP32-101")
        self.assertEqual(topic, "afes/v2/hcmut-lab/devices/SIM-ESP32-101/telemetry")
        self.assertEqual(TELEMETRY_QOS, 1)
        self.assertFalse(TELEMETRY_RETAIN)
        tenant_id, device_id = parse_telemetry_topic(topic)
        self.assertEqual((tenant_id, device_id), ("hcmut-lab", "SIM-ESP32-101"))

    def test_topic_rejects_wildcards_separators_and_wrong_channels(self) -> None:
        bad_segments = [
            "",
            "tenant/evil",
            "tenant+wild",
            "tenant#wild",
            "$SYS",
            "-leading-dash",
            "has space",
            "a" * 65,
        ]
        for seg in bad_segments:
            with self.subTest(bad_segment=seg):
                with self.assertRaises(TopicError):
                    telemetry_topic(seg, "SIM-ESP32-101")
                with self.assertRaises(TopicError):
                    telemetry_topic("stage-a-sim", seg)

        bad_topics = [
            "afes/v1/stage-a-sim/devices/SIM-ESP32-101/telemetry",
            "afes/v2/stage-a-sim/devices/SIM-ESP32-101/status",
            "afes/v2/stage-a-sim/devices/SIM-ESP32-101/events",
            "afes/v2/stage-a-sim/gateways/GW-LOCAL-PC01/telemetry",
            "afes/v2/+/devices/SIM-ESP32-101/telemetry",
            "afes/v2/stage-a-sim/devices/#/telemetry",
        ]
        for bad_topic in bad_topics:
            with self.subTest(bad_topic=bad_topic):
                with self.assertRaises(TopicError):
                    parse_telemetry_topic(bad_topic)

    def test_validate_topic_detects_device_mismatch(self) -> None:
        cfg = SimulatorConfig(fixture_mode=True, device_id="SIM-ESP32-101")
        payload = TelemetryGenerator(cfg).next_payload()
        self.assertTrue(validate_topic(cfg.topic, payload).valid)

        wrong_topic = telemetry_topic(cfg.tenant_id, "SIM-ESP32-999")
        mismatch = validate_topic(wrong_topic, payload)
        self.assertFalse(mismatch.valid)
        self.assertIn("TOPIC_DEVICE_MISMATCH", mismatch.codes)

    def test_env_example_loads_cleanly_and_redacts_credentials(self) -> None:
        env_example_path = _REPO_ROOT / "simulation" / "mqtt-publisher" / ".env.example"
        env_map = load_env_file(env_example_path)
        cfg = SimulatorConfig.from_env(env_map)
        self.assertEqual(cfg.tenant_id, "stage-a-sim")
        self.assertEqual(cfg.device_id, "SIM-ESP32-101")
        self.assertEqual(cfg.gateway_id, "GW-LOCAL-PC01")
        self.assertTrue(cfg.fixture_mode)
        self.assertEqual(cfg.effective_seed, 6)
        self.assertEqual(cfg.mqtt_host, "localhost")
        self.assertEqual(cfg.mqtt_port, 1883)

        redacted = cfg.redacted()
        self.assertEqual(redacted["mqtt_username"], "***")
        self.assertEqual(redacted["mqtt_pass"], "***")
        self.assertNotIn("placeholder_local_mqtt_password", repr(cfg))

    def test_remote_credentials_require_tls_by_default(self) -> None:
        with self.assertRaises(ConfigError):
            SimulatorConfig.from_env(
                {
                    "AFES_SIM_MQTT_HOST": "broker.example.local",
                    "AFES_SIM_MQTT_USERNAME": "placeholder_user",
                    "AFES_SIM_MQTT_PASSWORD": "placeholder_password",
                    "AFES_SIM_MQTT_TLS": "false",
                }
            )

        secure_cfg = SimulatorConfig.from_env(
            {
                "AFES_SIM_MQTT_HOST": "broker.example.local",
                "AFES_SIM_MQTT_USERNAME": "placeholder_user",
                "AFES_SIM_MQTT_PASSWORD": "placeholder_password",
                "AFES_SIM_MQTT_TLS": "true",
            }
        )
        self.assertTrue(secure_cfg.mqtt_tls)

    def test_invalid_env_values_raise_config_error(self) -> None:
        invalid_envs = [
            {"AFES_SIM_SCENARIO": "nonexistent-scenario"},
            {"AFES_SIM_INTERVAL_MS": "10"},
            {"AFES_SIM_COUNT": "0"},
            {"AFES_SIM_MQTT_PORT": "70000"},
            {"AFES_SIM_DEVICE_ID": "ab"},
            {"AFES_SIM_FLOOR_LEVEL": "not-an-int"},
            {"AFES_SIM_NOISE": "maybe"},
        ]
        for env in invalid_envs:
            with self.subTest(env=env):
                with self.assertRaises(ConfigError):
                    SimulatorConfig.from_env(env)


if __name__ == "__main__":
    unittest.main()
