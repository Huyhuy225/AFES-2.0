"""Tests for Stage A virtual telemetry scenarios, determinism, and fixture parity."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PUBLISHER_DIR = str(_REPO_ROOT / "simulation" / "mqtt-publisher")
if _PUBLISHER_DIR not in sys.path:
    sys.path.insert(0, _PUBLISHER_DIR)

from afes_sim import (  # noqa: E402
    SCENARIOS,
    SimulatorConfig,
    TelemetryGenerator,
    generate_payloads,
    validate_telemetry,
    validate_topic,
)
from afes_sim.scenarios import (  # noqa: E402
    SMOKE_ALARM_THRESHOLD_PPM,
    SMOKE_PREALARM_FLOOR_PPM,
    TEMP_ALARM_THRESHOLD_C,
)
from afes_sim.schema import loads_strict  # noqa: E402

VALID_FIXTURES_DIR = _REPO_ROOT / "simulation" / "test-data" / "fixtures" / "valid"


class GeneratorAndScenariosTests(unittest.TestCase):
    def test_all_three_scenarios_generate_valid_stage_a_telemetry(self) -> None:
        self.assertEqual(set(SCENARIOS), {"normal", "warning-smoke", "critical-fire"})
        for scenario_key in ("normal", "warning-smoke", "critical-fire"):
            for noise in (True, False):
                with self.subTest(scenario=scenario_key, noise=noise):
                    cfg = SimulatorConfig(
                        scenario=scenario_key,
                        seed=42,
                        start_epoch_ms=1794457200000,
                        interval_ms=2000,
                        count=25,
                        noise=noise,
                    )
                    gen = TelemetryGenerator(cfg)
                    payloads = list(gen.generate())
                    self.assertEqual(len(payloads), 25)
                    seen_ids: set[str] = set()
                    prev_epoch: int | None = None

                    for payload in payloads:
                        res = validate_telemetry(payload, require_simulated=True)
                        self.assertTrue(res.valid, res.summary())
                        self.assertTrue(validate_topic(gen.topic, payload).valid)

                        # Explicit Stage A simulation labelling
                        self.assertIs(payload["simulation"]["is_simulated"], True)
                        self.assertEqual(payload["simulation"]["synthetic_noise_added"], noise)
                        self.assertTrue(
                            payload["simulation"]["scenario_id"].startswith("STAGE_A_SIM_")
                        )
                        self.assertEqual(payload["device"]["device_type"], "VIRTUAL_SIM_NODE")
                        self.assertTrue(payload["device"]["mac_address"].startswith("02:00:"))

                        msg_id = payload["message_id"]
                        self.assertNotIn(msg_id, seen_ids)
                        seen_ids.add(msg_id)

                        epoch = payload["timestamps"]["timestamp_epoch_ms"]
                        if prev_epoch is not None:
                            self.assertEqual(epoch - prev_epoch, 2000)
                        prev_epoch = epoch

    def test_scenario_specific_signal_bands_and_actuator_states(self) -> None:
        # 1. normal scenario
        normal_payloads = generate_payloads(
            SimulatorConfig(scenario="normal", fixture_mode=True, count=15)
        )
        for p in normal_payloads:
            self.assertEqual(p["status"]["system_state"], "NORMAL")
            self.assertEqual(p["readings"]["ai_classification"], "NORMAL")
            self.assertFalse(p["readings"]["flame_detected"])
            self.assertLess(p["readings"]["temperature"], TEMP_ALARM_THRESHOLD_C)
            self.assertLess(p["readings"]["smoke_ppm"], SMOKE_PREALARM_FLOOR_PPM)
            self.assertLessEqual(p["readings"]["ai_inferred_fire_risk"], 0.10)
            self.assertFalse(p["actuators"]["buzzer_active"])
            self.assertFalse(p["actuators"]["alarm_led_active"])
            self.assertFalse(p["actuators"]["water_pump_relay_active"])
            self.assertEqual(p["actuators"]["override_mode"], "AUTO")

        # 2. warning-smoke scenario
        warning_payloads = generate_payloads(
            SimulatorConfig(scenario="warning-smoke", fixture_mode=True, count=15)
        )
        for p in warning_payloads:
            self.assertEqual(p["status"]["system_state"], "WARNING")
            self.assertEqual(p["readings"]["ai_classification"], "SMOKE_SPIKE")
            self.assertFalse(p["readings"]["flame_detected"])
            self.assertLess(p["readings"]["temperature"], TEMP_ALARM_THRESHOLD_C)
            self.assertGreaterEqual(p["readings"]["smoke_ppm"], SMOKE_PREALARM_FLOOR_PPM)
            self.assertLess(p["readings"]["smoke_ppm"], SMOKE_ALARM_THRESHOLD_PPM)
            self.assertTrue(p["actuators"]["alarm_led_active"])
            self.assertTrue(p["actuators"]["exhaust_fan_active"])
            self.assertFalse(p["actuators"]["water_pump_relay_active"])
            self.assertEqual(p["actuators"]["override_mode"], "AUTO")

        # 3. critical-fire scenario
        critical_payloads = generate_payloads(
            SimulatorConfig(scenario="critical-fire", fixture_mode=True, count=15)
        )
        for p in critical_payloads:
            self.assertEqual(p["status"]["system_state"], "CRITICAL")
            self.assertEqual(p["readings"]["ai_classification"], "FIRE")
            self.assertTrue(p["readings"]["flame_detected"])
            self.assertGreater(p["readings"]["temperature"], TEMP_ALARM_THRESHOLD_C)
            self.assertGreater(p["readings"]["smoke_ppm"], SMOKE_ALARM_THRESHOLD_PPM)
            self.assertGreaterEqual(p["readings"]["ai_inferred_fire_risk"], 0.85)
            self.assertTrue(p["actuators"]["buzzer_active"])
            self.assertTrue(p["actuators"]["alarm_led_active"])
            self.assertTrue(p["actuators"]["water_pump_relay_active"])
            self.assertEqual(p["actuators"]["override_mode"], "EMERGENCY_LOCK")

    def test_fixture_mode_reproduces_committed_fixtures_deterministically(self) -> None:
        fixture_map = {
            "normal": "stage_a_normal_seed6.json",
            "warning-smoke": "stage_a_warning_smoke_seed6.json",
            "critical-fire": "stage_a_critical_fire_seed6.json",
        }
        for scenario_key, filename in fixture_map.items():
            with self.subTest(scenario=scenario_key):
                cfg = SimulatorConfig(fixture_mode=True, scenario=scenario_key, count=3)
                generated = generate_payloads(cfg, count=3)
                committed = loads_strict(
                    (VALID_FIXTURES_DIR / filename).read_text(encoding="utf-8")
                )
                self.assertEqual(generated[0], committed)

                if scenario_key == "normal":
                    stream_lines = [
                        json.loads(line)
                        for line in (VALID_FIXTURES_DIR / "stage_a_multi_step_stream_seed6.jsonl")
                        .read_text(encoding="utf-8")
                        .splitlines()
                        if line.strip()
                    ]
                    self.assertEqual(generated, stream_lines)


if __name__ == "__main__":
    unittest.main()
