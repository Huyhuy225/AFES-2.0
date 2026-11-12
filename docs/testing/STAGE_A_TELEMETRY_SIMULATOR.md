# AFES 2.0 – Stage A Telemetry Simulator & MQTT Contract Test Evidence

> **Verification Classification**: `[SIMULATED - STAGE A]` — Software Simulation & Offline Contract Verification ONLY
> **Hardware Claim Disclaimer**: **Zero physical ESP32-S3 hardware, physical sensors, or live external/cloud MQTT broker delivery is claimed by this document.**
> **Canonical Contract**: [`docs/TELEMETRY_SCHEMA.md`](../TELEMETRY_SCHEMA.md) (v2.0.0)
> **GitHub Issue**: [#6 – Stage A: build ESP32-S3 telemetry simulator and MQTT contract tests](https://github.com/Huyhuy225/AFES-2.0/issues/6)
> **Course Traceability**: Stage A preparation supporting **T08** (Local IoT Gateway ingestion) and **T13** (Threshold alert notification testing); status of T08/T13 remains unchanged until gateway/CoreIOT integration is executed.

---

## 1. Scope and Verification Summary

This document records the reproducible test procedure and executed **Stage A simulation / contract-level verification** for the virtual ESP32-S3 telemetry simulator under `simulation/`:

1. **Schema Parity Verification**: Confirms `simulation/test-data/schema/afes_v2_telemetry.schema.json` is an exact, unmodified copy of the formal Draft-07 JSON Schema in [`docs/TELEMETRY_SCHEMA.md` §8](../TELEMETRY_SCHEMA.md).
2. **Offline Contract & Profile Validation**: Validates required fields, JSON types, enumerations, RFC 4122 UUID v4 `message_id`, exact ISO 8601 UTC millisecond format (`YYYY-MM-DDTHH:mm:ss.sssZ`) coherent with `timestamp_epoch_ms`, 12-bit ADC bounds (`0..4095`), fire risk bounds (`0.0..1.0`), rejection of undocumented fields, and mandatory Stage A simulation labelling (`simulation.is_simulated == true`, non-empty `simulation.scenario_id`, `device.device_type == "VIRTUAL_SIM_NODE"`, locally administered MAC `02:00:xx:xx:xx:xx`).
3. **Scenario & Topic Coverage**: Exercises deterministic telemetry generation across `normal`, `warning-smoke`, and `critical-fire` scenarios on the canonical MQTT topic `afes/v2/{tenant_id}/devices/{device_id}/telemetry` (`QoS 1`, `retain = false`).
4. **Transport & Error-Handling Verification**: Exercises `MemoryTransport`, `StdoutTransport`, and `PahoMqttTransport` (via a fake/mocked MQTT client) including pre-publish contract rejection, bounded connection retries, mid-run disconnect recovery, and credential-redacted error reporting.

---

## 2. Executed Commands and Recorded Results (`[SIMULATED - STAGE A]`)

### 2.1. Automated Offline Unit & Contract Test Suite

- **Command**:
  ```bash
  python -B -m unittest discover -s simulation/tests -t . -v
  ```
- **Exit Code**: `0`
- **Recorded Output (`[SIMULATED - STAGE A]`)**:
  ```text
  test_all_three_scenarios_generate_valid_stage_a_telemetry (simulation.tests.test_generator_and_scenarios.GeneratorAndScenariosTests.test_all_three_scenarios_generate_valid_stage_a_telemetry) ... ok
  test_fixture_mode_reproduces_committed_fixtures_deterministically (simulation.tests.test_generator_and_scenarios.GeneratorAndScenariosTests.test_fixture_mode_reproduces_committed_fixtures_deterministically) ... ok
  test_scenario_specific_signal_bands_and_actuator_states (simulation.tests.test_generator_and_scenarios.GeneratorAndScenariosTests.test_scenario_specific_signal_bands_and_actuator_states) ... ok
  test_cli_publish_and_validate_subcommands (simulation.tests.test_publisher_and_cli.PublisherAndCliTests.test_cli_publish_and_validate_subcommands) ... ok
  test_memory_transport_publishes_qos1_and_validates_every_packet (simulation.tests.test_publisher_and_cli.PublisherAndCliTests.test_memory_transport_publishes_qos1_and_validates_every_packet) ... ok
  test_paho_mqtt_transport_raises_safe_error_when_broker_unavailable (simulation.tests.test_publisher_and_cli.PublisherAndCliTests.test_paho_mqtt_transport_raises_safe_error_when_broker_unavailable) ... ok
  test_paho_mqtt_transport_retries_connect_and_recovers_mid_publish (simulation.tests.test_publisher_and_cli.PublisherAndCliTests.test_paho_mqtt_transport_retries_connect_and_recovers_mid_publish) ... ok
  test_publisher_rejects_unmarked_or_invalid_payload_before_transport (simulation.tests.test_publisher_and_cli.PublisherAndCliTests.test_publisher_rejects_unmarked_or_invalid_payload_before_transport) ... ok
  test_stdout_transport_labels_each_line_as_stage_a_simulation (simulation.tests.test_publisher_and_cli.PublisherAndCliTests.test_stdout_transport_labels_each_line_as_stage_a_simulation) ... ok
  test_all_committed_invalid_fixtures_are_rejected_with_expected_codes (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_all_committed_invalid_fixtures_are_rejected_with_expected_codes) ... ok
  test_all_committed_valid_fixtures_pass_strict_stage_a_validation (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_all_committed_valid_fixtures_pass_strict_stage_a_validation) ... ok
  test_doc_stage_a_example_matches_fixture_and_validates (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_doc_stage_a_example_matches_fixture_and_validates) ... ok
  test_doc_stage_b_example_validates_schema_but_rejected_as_stage_a (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_doc_stage_b_example_validates_schema_but_rejected_as_stage_a) ... ok
  test_profile_edge_case_rejections (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_profile_edge_case_rejections) ... ok
  test_schema_artifact_matches_telemetry_schema_doc_verbatim (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_schema_artifact_matches_telemetry_schema_doc_verbatim) ... ok
  test_schema_loader_rejects_unsupported_keyword (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_schema_loader_rejects_unsupported_keyword) ... ok
  test_strict_json_loader_rejects_nan_and_infinity (simulation.tests.test_schema_and_validator.SchemaAndValidatorTests.test_strict_json_loader_rejects_nan_and_infinity) ... ok
  test_env_example_loads_cleanly_and_redacts_credentials (simulation.tests.test_topics_and_config.TopicsAndConfigTests.test_env_example_loads_cleanly_and_redacts_credentials) ... ok
  test_invalid_env_values_raise_config_error (simulation.tests.test_topics_and_config.TopicsAndConfigTests.test_invalid_env_values_raise_config_error) ... ok
  test_remote_credentials_require_tls_by_default (simulation.tests.test_topics_and_config.TopicsAndConfigTests.test_remote_credentials_require_tls_by_default) ... ok
  test_telemetry_topic_construction_and_parsing (simulation.tests.test_topics_and_config.TopicsAndConfigTests.test_telemetry_topic_construction_and_parsing) ... ok
  test_topic_rejects_wildcards_separators_and_wrong_channels (simulation.tests.test_topics_and_config.TopicsAndConfigTests.test_topic_rejects_wildcards_separators_and_wrong_channels) ... ok
  test_validate_topic_detects_device_mismatch (simulation.tests.test_topics_and_config.TopicsAndConfigTests.test_validate_topic_detects_device_mismatch) ... ok

  ----------------------------------------------------------------------
  Ran 23 tests in 0.048s

  OK
  ```

### 2.2. Offline Fixture Contract Validation CLI

- **Command**:
  ```bash
  PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim validate \
    simulation/test-data/fixtures/valid/stage_a_doc_example.json \
    simulation/test-data/fixtures/valid/stage_a_normal_seed6.json \
    simulation/test-data/fixtures/valid/stage_a_warning_smoke_seed6.json \
    simulation/test-data/fixtures/valid/stage_a_critical_fire_seed6.json \
    simulation/test-data/fixtures/valid/stage_a_multi_step_stream_seed6.jsonl \
    --topic afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry
  ```
- **Exit Code**: `0`
- **Recorded Output (`[SIMULATED - STAGE A]`)**:
  ```text
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_doc_example.json
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_normal_seed6.json
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_warning_smoke_seed6.json
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_critical_fire_seed6.json
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_multi_step_stream_seed6.jsonl:1
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_multi_step_stream_seed6.jsonl:2
  [SIMULATED - STAGE A] VALID simulation/test-data/fixtures/valid/stage_a_multi_step_stream_seed6.jsonl:3
  ```

### 2.3. Deterministic Offline Telemetry Generation Across All Three Scenarios

- **Commands**:
  ```bash
  PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish --fixture-mode --scenario normal --count 1
  PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish --fixture-mode --scenario warning-smoke --count 1
  PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish --fixture-mode --scenario critical-fire --count 1
  ```
- **Exit Code**: `0` for each command.
- **Recorded Summary Lines (`stderr`, `[SIMULATED - STAGE A]`)**:
  ```text
  [SIMULATED - STAGE A] Completed virtual telemetry run (NOT physical ESP32-S3 hardware verification): transport=stdout topic=afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry qos=1 retain=False scenario=normal seed=6 published=1/1
  [SIMULATED - STAGE A] Completed virtual telemetry run (NOT physical ESP32-S3 hardware verification): transport=stdout topic=afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry qos=1 retain=False scenario=warning-smoke seed=6 published=1/1
  [SIMULATED - STAGE A] Completed virtual telemetry run (NOT physical ESP32-S3 hardware verification): transport=stdout topic=afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry qos=1 retain=False scenario=critical-fire seed=6 published=1/1
  ```
- **Broker Verification Note**: No external or local Mosquitto broker daemon was running in this execution environment; therefore, MQTT transport behavior (QoS 1 publish, TLS/auth wiring, connection retry/backoff, and mid-run reconnect) is verified strictly at the **contract and mocked-transport level** (`test_paho_mqtt_transport_*`), and **no live broker delivery is claimed**.

---

## 3. Committed Fixture Inventory

| Fixture Path | Classification | Purpose & Verified Rules |
|---|---|---|
| `simulation/test-data/schema/afes_v2_telemetry.schema.json` | Schema Artifact | Verbatim Draft-07 JSON Schema from `docs/TELEMETRY_SCHEMA.md` §8. |
| `simulation/test-data/fixtures/valid/stage_a_doc_example.json` | Valid (`[SIMULATED - STAGE A]`) | Exact Stage A example packet from `docs/TELEMETRY_SCHEMA.md` §7.1. |
| `simulation/test-data/fixtures/valid/stage_a_normal_seed6.json` | Valid (`[SIMULATED - STAGE A]`) | Deterministic `normal` scenario fixture (`seed=6`, `epoch=1794457200000`). |
| `simulation/test-data/fixtures/valid/stage_a_warning_smoke_seed6.json` | Valid (`[SIMULATED - STAGE A]`) | Deterministic `warning-smoke` scenario fixture (`300..500 PPM` pre-alarm). |
| `simulation/test-data/fixtures/valid/stage_a_critical_fire_seed6.json` | Valid (`[SIMULATED - STAGE A]`) | Deterministic `critical-fire` scenario fixture (`>50 °C`, `>500 PPM`, flame & suppression active). |
| `simulation/test-data/fixtures/valid/stage_a_multi_step_stream_seed6.jsonl` | Valid (`[SIMULATED - STAGE A]`) | 3-packet deterministic JSONL stream verifying monotonic timestamps and uptime progression. |
| `simulation/test-data/fixtures/invalid/missing_required_readings.json` | Invalid Rejection | Missing required `readings.smoke_ppm`, `readings.flame_raw_adc`, and `simulation` (`SCHEMA_REQUIRED`). |
| `simulation/test-data/fixtures/invalid/wrong_schema_version.json` | Invalid Rejection | Unsupported `schema_version: "1.0"` (`SCHEMA_ENUM`). |
| `simulation/test-data/fixtures/invalid/invalid_uuid_not_v4.json` | Invalid Rejection | Non-v4 UUID `message_id` rejected by Stage A profile (`PROFILE_UUID_V4`). |
| `simulation/test-data/fixtures/invalid/timestamp_epoch_mismatch.json` | Invalid Rejection | Incoherent `timestamp_utc` vs `timestamp_epoch_ms` (`PROFILE_TIMESTAMP_MISMATCH`). |
| `simulation/test-data/fixtures/invalid/adc_and_risk_out_of_bounds.json` | Invalid Rejection | Out-of-range 12-bit ADC (`4096`, `-5`) and fire risk (`1.25`) (`SCHEMA_MAXIMUM`, `SCHEMA_MINIMUM`, `PROFILE_ADC_RANGE`, `PROFILE_RISK_RANGE`). |
| `simulation/test-data/fixtures/invalid/unmarked_simulation_false.json` | Invalid Rejection | `simulation.is_simulated: false` / physical `YOLO_UNO_S3` packet rejected by Stage A validator (`PROFILE_NOT_SIMULATED`). |
| `simulation/test-data/fixtures/invalid/undocumented_extra_field.json` | Invalid Rejection | Undocumented top-level and nested properties rejected (`PROFILE_UNDOCUMENTED_FIELD`). |

---

## 4. Hardware Handoff Boundaries for Stage B ESP32-S3 Firmware

When physical ESP32-S3 (`YoloUNO`) nodes are commissioned in Stage B (`firmware/esp32-s3/`), the following strict handoff rules apply:

1. **Unchanged Wire Contract**: Physical firmware and the Local IoT Gateway (`local-gateway/`) consume and emit the exact same `AFES2TelemetryPayload` schema (`schema_version: "2.0"`) and topic structure `afes/v2/{tenant_id}/devices/{device_id}/telemetry` (`QoS 1`, `retain = false`).
2. **Physical Identity & Simulation Flag Flip**:
   - `simulation.is_simulated` **must** be set to `false` (`simulation.scenario_id = null`, `simulation.synthetic_noise_added = false`).
   - `device.device_type` **must** be `"YOLO_UNO_S3"` (or `"CUSTOM_SENSOR_NODE"`), never `"VIRTUAL_SIM_NODE"`.
   - `device.mac_address` **must** be the factory-burned IEEE EUI-48 MAC read from hardware eFuse (`esp_read_mac`), never a locally administered `02:00:*` simulator address.
3. **Real Sensor Acquisition & Calibration**:
   - Replace synthetic `Signal` ramps in `scenarios.py` and the linear ADC approximation in `generator.py` with real hardware drivers: I2C temperature/humidity (`T01`), RS485 Modbus (`T02`), BLE peripheral client (`T03`), calibrated MQ-2 smoke ADC curve, optical flame GPIO/ADC, and on-device TinyML TFLite Micro inference (`T04`).
4. **Separate Stage B Evidence Path**:
   - Stage B pull requests must provide physical serial monitor traces (`115200` baud), hardware stimulus measurements, and bench photographs under `reports/evidence/Txx/` as mandated by [`DEVELOPMENT_GUIDE.md`](../../DEVELOPMENT_GUIDE.md).
