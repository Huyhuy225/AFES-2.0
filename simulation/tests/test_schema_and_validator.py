"""Offline schema parity and contract validator tests for AFES v2 telemetry."""

from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PUBLISHER_DIR = str(_REPO_ROOT / "simulation" / "mqtt-publisher")
if _PUBLISHER_DIR not in sys.path:
    sys.path.insert(0, _PUBLISHER_DIR)

from afes_sim import (  # noqa: E402
    DEFAULT_SCHEMA_PATH,
    PayloadDecodeError,
    SchemaError,
    SimulatorConfig,
    TelemetryGenerator,
    load_schema,
    validate_telemetry,
)
from afes_sim.schema import loads_strict  # noqa: E402

VALID_FIXTURES_DIR = _REPO_ROOT / "simulation" / "test-data" / "fixtures" / "valid"
INVALID_FIXTURES_DIR = _REPO_ROOT / "simulation" / "test-data" / "fixtures" / "invalid"
TELEMETRY_SCHEMA_DOC = _REPO_ROOT / "docs" / "TELEMETRY_SCHEMA.md"


def _extract_json_block_after_heading(markdown: str, heading_substring: str) -> dict[str, object]:
    pos = markdown.find(heading_substring)
    if pos < 0:
        raise AssertionError(f"Heading {heading_substring!r} not found in docs/TELEMETRY_SCHEMA.md")
    fence_match = re.search(r"```json\s*(\{.*?\})\s*```", markdown[pos:], flags=re.DOTALL)
    if fence_match is None:
        raise AssertionError(f"No JSON block found after {heading_substring!r}")
    return json.loads(fence_match.group(1))


class SchemaAndValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc_text = TELEMETRY_SCHEMA_DOC.read_text(encoding="utf-8")
        cls.schema = load_schema(DEFAULT_SCHEMA_PATH)

    def test_schema_artifact_matches_telemetry_schema_doc_verbatim(self) -> None:
        doc_schema = _extract_json_block_after_heading(
            self.doc_text, "## 8. Formal JSON Schema (Draft-07)"
        )
        self.assertEqual(self.schema, doc_schema)

    def test_doc_stage_a_example_matches_fixture_and_validates(self) -> None:
        doc_stage_a = _extract_json_block_after_heading(
            self.doc_text, "### 7.1. Stage A Simulation Telemetry Packet"
        )
        fixture_stage_a = loads_strict(
            (VALID_FIXTURES_DIR / "stage_a_doc_example.json").read_text(encoding="utf-8")
        )
        self.assertEqual(fixture_stage_a, doc_stage_a)
        result = validate_telemetry(fixture_stage_a, require_simulated=True, schema=self.schema)
        self.assertTrue(result.valid, result.summary())

    def test_doc_stage_b_example_validates_schema_but_rejected_as_stage_a(self) -> None:
        doc_stage_b = _extract_json_block_after_heading(
            self.doc_text, "### 7.2. Stage B Physical Hardware Telemetry Packet"
        )
        stage_b_allowed = validate_telemetry(
            doc_stage_b, require_simulated=False, schema=self.schema
        )
        self.assertTrue(stage_b_allowed.valid, stage_b_allowed.summary())

        stage_a_strict = validate_telemetry(
            doc_stage_b, require_simulated=True, schema=self.schema
        )
        self.assertFalse(stage_a_strict.valid)
        self.assertIn("PROFILE_NOT_SIMULATED", stage_a_strict.codes)

    def test_all_committed_valid_fixtures_pass_strict_stage_a_validation(self) -> None:
        json_files = sorted(VALID_FIXTURES_DIR.glob("*.json"))
        jsonl_files = sorted(VALID_FIXTURES_DIR.glob("*.jsonl"))
        self.assertGreaterEqual(len(json_files), 4)
        self.assertGreaterEqual(len(jsonl_files), 1)

        for path in json_files:
            with self.subTest(fixture=path.name):
                payload = loads_strict(path.read_text(encoding="utf-8"))
                result = validate_telemetry(payload, require_simulated=True, schema=self.schema)
                self.assertTrue(result.valid, f"{path.name}: {result.summary()}")

        for path in jsonl_files:
            with self.subTest(fixture=path.name):
                lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
                self.assertGreaterEqual(len(lines), 3)
                for idx, line in enumerate(lines):
                    payload = loads_strict(line)
                    result = validate_telemetry(payload, require_simulated=True, schema=self.schema)
                    self.assertTrue(result.valid, f"{path.name}:{idx + 1}: {result.summary()}")

    def test_all_committed_invalid_fixtures_are_rejected_with_expected_codes(self) -> None:
        expected_codes_by_file: dict[str, set[str]] = {
            "missing_required_readings.json": {"SCHEMA_REQUIRED"},
            "wrong_schema_version.json": {"SCHEMA_ENUM"},
            "invalid_uuid_not_v4.json": {"PROFILE_UUID_V4"},
            "timestamp_epoch_mismatch.json": {"PROFILE_TIMESTAMP_MISMATCH"},
            "adc_and_risk_out_of_bounds.json": {
                "SCHEMA_MAXIMUM",
                "SCHEMA_MINIMUM",
                "PROFILE_ADC_RANGE",
                "PROFILE_RISK_RANGE",
            },
            "unmarked_simulation_false.json": {"PROFILE_NOT_SIMULATED"},
            "undocumented_extra_field.json": {"PROFILE_UNDOCUMENTED_FIELD"},
        }
        actual_files = {p.name for p in INVALID_FIXTURES_DIR.glob("*.json")}
        self.assertEqual(actual_files, set(expected_codes_by_file))

        for filename, expected_codes in expected_codes_by_file.items():
            with self.subTest(invalid_fixture=filename):
                payload = loads_strict((INVALID_FIXTURES_DIR / filename).read_text(encoding="utf-8"))
                result = validate_telemetry(payload, require_simulated=True, schema=self.schema)
                self.assertFalse(result.valid, f"Expected {filename} to be rejected")
                self.assertTrue(
                    expected_codes.issubset(result.codes),
                    f"{filename}: expected {expected_codes} <= {result.codes}",
                )

    def test_strict_json_loader_rejects_nan_and_infinity(self) -> None:
        for bad in ('{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}', "{unclosed"):
            with self.subTest(raw=bad):
                with self.assertRaises(PayloadDecodeError):
                    loads_strict(bad)

    def test_schema_loader_rejects_unsupported_keyword(self) -> None:
        bad_schema = copy.deepcopy(self.schema)
        bad_schema["additionalProperties"] = False
        from afes_sim.schema import _check_keywords

        with self.assertRaises(SchemaError):
            _check_keywords(bad_schema, "")

    def test_profile_edge_case_rejections(self) -> None:
        base = TelemetryGenerator(SimulatorConfig(fixture_mode=True)).next_payload()

        cases: list[tuple[str, object, str]] = []

        # Boolean masquerading as integer ADC reading
        p_bool = copy.deepcopy(base)
        p_bool["readings"]["smoke_raw_adc"] = True
        cases.append(("bool_as_int", p_bool, "SCHEMA_TYPE"))

        # Negative smoke concentration
        p_neg_smoke = copy.deepcopy(base)
        p_neg_smoke["readings"]["smoke_ppm"] = -0.5
        cases.append(("negative_smoke", p_neg_smoke, "PROFILE_NEGATIVE_CONCENTRATION"))

        # Humidity > 100%
        p_hum = copy.deepcopy(base)
        p_hum["readings"]["humidity"] = 105.0
        cases.append(("humidity_over_100", p_hum, "PROFILE_HUMIDITY_RANGE"))

        # Negative uptime
        p_up = copy.deepcopy(base)
        p_up["timestamps"]["device_uptime_s"] = -1
        cases.append(("negative_uptime", p_up, "PROFILE_UPTIME_NEGATIVE"))

        # Battery out of range
        p_bat = copy.deepcopy(base)
        p_bat["status"]["battery_pct"] = 120.0
        cases.append(("battery_over_100", p_bat, "PROFILE_BATTERY_RANGE"))

        # Unknown AI classification
        p_ai = copy.deepcopy(base)
        p_ai["readings"]["ai_classification"] = "UNKNOWN_LABEL"
        cases.append(("unknown_ai_label", p_ai, "PROFILE_AI_CLASSIFICATION"))

        # Physical device_type while claiming simulation.is_simulated=true
        p_devtype = copy.deepcopy(base)
        p_devtype["device"]["device_type"] = "YOLO_UNO_S3"
        cases.append(("physical_device_type_in_sim", p_devtype, "PROFILE_DEVICE_TYPE"))

        # Globally administered (vendor) MAC address on simulated node
        p_mac = copy.deepcopy(base)
        p_mac["device"]["mac_address"] = "84:F7:03:1A:2B:3C"
        cases.append(("vendor_mac_in_sim", p_mac, "PROFILE_MAC_NOT_LOCAL"))

        # Malformed MAC address
        p_bad_mac = copy.deepcopy(base)
        p_bad_mac["device"]["mac_address"] = "not-a-mac"
        cases.append(("malformed_mac", p_bad_mac, "PROFILE_MAC_FORMAT"))

        # Missing scenario_id when is_simulated=true
        p_no_sc = copy.deepcopy(base)
        p_no_sc["simulation"]["scenario_id"] = None
        cases.append(("null_scenario_id_in_sim", p_no_sc, "PROFILE_SCENARIO_MISSING"))

        for name, mutated, expected_code in cases:
            with self.subTest(case=name):
                res = validate_telemetry(mutated, require_simulated=True, schema=self.schema)
                self.assertFalse(res.valid)
                self.assertIn(expected_code, res.codes, f"{name}: got {res.codes}")


if __name__ == "__main__":
    unittest.main()
