# AFES 2.0 Stage A Virtual Telemetry Simulator & Contract Validator

> **Verification Classification**: `[SIMULATED - STAGE A]` (Virtual Simulation & Contract Verification ONLY — **NOT** physical ESP32-S3 hardware verification).
> **Canonical Contract**: [`docs/TELEMETRY_SCHEMA.md`](../../docs/TELEMETRY_SCHEMA.md) (Specification v2.0.0)
> **GitHub Issue**: [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6)

## 1. Purpose and Scope

`simulation/mqtt-publisher` provides a reproducible, hardware-independent **Stage A virtual ESP32-S3 sensing node simulator** and **offline MQTT telemetry contract validator** for AFES 2.0.

- **Contract Fidelity**: Generates and validates only the approved AFES v2 telemetry envelope (`schema_version: "2.0"`) and topic pattern `afes/v2/{tenant_id}/devices/{device_id}/telemetry` (`QoS 1`, `retain = false`) defined in [`docs/TELEMETRY_SCHEMA.md`](../../docs/TELEMETRY_SCHEMA.md).
- **Mandatory Simulation Labelling**: Every emitted payload carries `simulation.is_simulated = true`, a `STAGE_A_SIM_*` scenario identifier, `device.device_type = "VIRTUAL_SIM_NODE"`, and a locally administered unicast MAC address (`02:00:xx:xx:xx:xx`) so simulated frames can never impersonate Stage B physical hardware.
- **Zero-Credential Offline Execution**: Offline generation (`--transport stdout` or `--transport memory`), schema/profile validation (`validate`), and the entire unit/contract test suite (`simulation/tests/`) run on the Python 3.11+ standard library with **no third-party dependencies, no `.env` file, no network sockets, and no credentials required**.

---

## 2. Directory Layout

```text
simulation/
├── mqtt-publisher/
│   ├── .env.example          # Safe placeholder environment variables (AFES_SIM_*)
│   ├── README.md             # This guide
│   ├── requirements.txt      # Optional paho-mqtt==2.1.0 for live broker publishing only
│   └── afes_sim/
│       ├── __init__.py       # Public package exports
│       ├── __main__.py       # CLI entrypoint (python -m afes_sim)
│       ├── cli.py            # `publish` and `validate` CLI subcommands
│       ├── config.py         # AFES_SIM_* environment loader, validation, and redaction
│       ├── generator.py      # Deterministic/seeded and wall-clock telemetry generator
│       ├── publisher.py      # MemoryTransport, StdoutTransport, PahoMqttTransport, pre-publish gate
│       ├── scenarios.py      # Stage A scenarios: normal, warning-smoke, critical-fire
│       ├── schema.py         # Dependency-free JSON Schema Draft-07 subset validator
│       ├── topics.py         # AFES v2 topic builder/parser and segment hygiene
│       └── validator.py      # Schema + Stage A profile validator
├── test-data/
│   ├── schema/
│   │   └── afes_v2_telemetry.schema.json   # Verbatim Draft-07 schema from docs/TELEMETRY_SCHEMA.md §8
│   └── fixtures/
│       ├── valid/            # Deterministic Stage A valid fixtures (.json and .jsonl)
│       └── invalid/          # Deliberately invalid payloads exercising rejection rules
└── tests/                    # Offline unittest suite (23 contract & unit tests)
```

---

## 3. Quick Start (Offline — Zero Dependencies, Zero Credentials)

All commands below run from the **repository root** using only Python 3.11+ standard library modules.

### 3.1. Run the Offline Contract & Unit Test Suite

```bash
python -B -m unittest discover -s simulation/tests -t . -v
```

### 3.2. Validate Committed Fixtures Against the AFES v2 Contract

```bash
# PowerShell:
$env:PYTHONPATH = "simulation/mqtt-publisher"
python -B -m afes_sim validate `
  simulation/test-data/fixtures/valid/stage_a_doc_example.json `
  simulation/test-data/fixtures/valid/stage_a_normal_seed6.json `
  simulation/test-data/fixtures/valid/stage_a_warning_smoke_seed6.json `
  simulation/test-data/fixtures/valid/stage_a_critical_fire_seed6.json `
  simulation/test-data/fixtures/valid/stage_a_multi_step_stream_seed6.jsonl `
  --topic afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry
```

```bash
# POSIX sh / bash:
PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim validate \
  simulation/test-data/fixtures/valid/*.json \
  simulation/test-data/fixtures/valid/*.jsonl \
  --topic afes/v2/stage-a-sim/devices/SIM-ESP32-101/telemetry
```

### 3.3. Generate Reproducible Virtual Telemetry Offline (`stdout`)

In `--fixture-mode` (`seed = 6`, `start_epoch_ms = 1794457200000`), output is 100% deterministic across runs:

```bash
# Normal baseline scenario
PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish \
  --fixture-mode --scenario normal --count 2 --transport stdout

# Smoke pre-alarm warning scenario
PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish \
  --fixture-mode --scenario warning-smoke --count 2 --transport stdout

# Confirmed critical fire scenario
PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish \
  --fixture-mode --scenario critical-fire --count 2 --transport stdout
```

---

## 4. Optional Local MQTT Broker Publishing (`--transport mqtt`)

Publishing over a network socket is optional and only used when `--transport mqtt` is explicitly passed.

1. Install the pinned MQTT client dependency:
   ```bash
   python -m pip install -r simulation/mqtt-publisher/requirements.txt
   ```
2. Optionally copy `simulation/mqtt-publisher/.env.example` to a local, git-ignored `.env` file and adjust local broker settings (never commit `.env` or real credentials).
3. Publish virtual telemetry to a local Mosquitto broker (`localhost:1883`):
   ```bash
   PYTHONPATH=simulation/mqtt-publisher python -B -m afes_sim publish \
     --transport mqtt --fixture-mode --scenario critical-fire --count 5 --no-sleep
   ```

If the broker is unreachable, `PahoMqttTransport` retries `AFES_SIM_MQTT_CONNECT_ATTEMPTS` times with linear backoff (`AFES_SIM_MQTT_RETRY_BACKOFF_S`) and exits with code `1` and a credential-redacted `[SIMULATED - STAGE A] PUBLISH ERROR` message. Cleartext credentials to non-loopback hosts are refused by configuration validation unless `AFES_SIM_MQTT_TLS=true` is enabled.

---

## 5. Configuration Reference (`AFES_SIM_*`)

| Environment Variable | Default | Description |
|---|---|---|
| `AFES_SIM_TENANT_ID` | `stage-a-sim` | Tenant segment in `afes/v2/{tenant_id}/devices/{device_id}/telemetry`. |
| `AFES_SIM_DEVICE_ID` | `SIM-ESP32-101` | Virtual node identifier (`minLength: 3`, single MQTT segment). |
| `AFES_SIM_GATEWAY_ID` | `GW-LOCAL-PC01` | Target Local Gateway identifier (`gateway.gateway_id`). |
| `AFES_SIM_ZONE_ID` | `ZONE-101` | Facility zone identifier (`zone.zone_id`). |
| `AFES_SIM_ROOM_CODE` | `ROOM-101` | Room code (`zone.room_code`). |
| `AFES_SIM_BUILDING_ID` | `BLDG-CSE` | Building identifier (`zone.building_id`). |
| `AFES_SIM_FLOOR_LEVEL` | `1` | Integer floor level (`zone.floor_level`). |
| `AFES_SIM_SCENARIO` | `normal` | Scenario key: `normal`, `warning-smoke`, or `critical-fire`. |
| `AFES_SIM_FIXTURE_MODE` | `false` | When `true`, anchors `seed=6` and `start_epoch_ms=1794457200000`. |
| `AFES_SIM_SEED` | *(unset)* | Optional integer RNG seed for deterministic output. |
| `AFES_SIM_START_EPOCH_MS` | *(unset)* | Optional starting Unix epoch milliseconds (`>= 0`). |
| `AFES_SIM_INTERVAL_MS` | `2000` | Nominal telemetry period in milliseconds (`100..3600000`). |
| `AFES_SIM_COUNT` | `10` | Number of telemetry packets to emit (`1..100000`). |
| `AFES_SIM_NOISE` | `true` | Inject bounded Gaussian noise (`simulation.synthetic_noise_added`). |
| `AFES_SIM_MQTT_HOST` | `localhost` | Optional MQTT broker hostname (`--transport mqtt`). |
| `AFES_SIM_MQTT_PORT` | `1883` | Optional MQTT broker port (`1..65535`). |
| `AFES_SIM_MQTT_CLIENT_ID` | `afes-stage-a-sim-<device_id>` | MQTT client identifier. |
| `AFES_SIM_MQTT_USERNAME` | `""` | Placeholder/local MQTT username (masked in logs). |
| `AFES_SIM_MQTT_PASSWORD` | `""` | Placeholder/local MQTT password (masked in logs). |
| `AFES_SIM_MQTT_TLS` | `false` | Enable TLS on the MQTT connection (`required` for remote auth). |
| `AFES_SIM_MQTT_TLS_CA_FILE` | `""` | Optional CA bundle path when `AFES_SIM_MQTT_TLS=true`. |
| `AFES_SIM_MQTT_KEEPALIVE_S` | `60` | MQTT keepalive interval in seconds. |
| `AFES_SIM_MQTT_CONNECT_TIMEOUT_S` | `5.0` | Socket/publish acknowledgment timeout in seconds. |
| `AFES_SIM_MQTT_CONNECT_ATTEMPTS` | `3` | Bounded connection attempts (`1..20`). |
| `AFES_SIM_MQTT_RETRY_BACKOFF_S` | `1.0` | Base retry backoff in seconds. |

---

## 6. Scenarios & Modelling Assumptions vs. Canonical Contract

| Scenario Key | `simulation.scenario_id` | `status.system_state` | `readings.ai_classification` | Temperature (°C) | Smoke (PPM) | Flame / Actuators |
|---|---|---|---|---|---|---|
| `normal` | `STAGE_A_SIM_NORMAL_BASELINE` | `NORMAL` | `NORMAL` | `20.0..35.0` (ramp `26.5 -> 27.5`) | `50.0..200.0` (ramp `110 -> 130`) | `flame_detected=false`, all actuators `false`, `override_mode="AUTO"` |
| `warning-smoke` | `STAGE_A_SIM_WARNING_SMOKE` | `WARNING` | `SMOKE_SPIKE` | `25.0..49.9` (ramp `29.0 -> 33.0`) | `300.0..499.9` (ramp `320 -> 470`) | `flame_detected=false`, `alarm_led_active=true`, `exhaust_fan_active=true`, `water_pump_relay_active=false`, `override_mode="AUTO"` |
| `critical-fire` | `STAGE_A_SIM_CRITICAL_FIRE` | `CRITICAL` | `FIRE` | `50.1..90.0` (ramp `55.0 -> 68.0`) | `500.1..2000.0` (ramp `620 -> 880`) | `flame_detected=true`, `buzzer_active=true`, `alarm_led_active=true`, `water_pump_relay_active=true`, `override_mode="EMERGENCY_LOCK"` |

- **Documented Contract Thresholds**: Critical fire thresholds (`temperature > 50.0 °C` and `smoke_ppm > 500.0 PPM`) follow [`docs/TELEMETRY_SCHEMA.md` §4.1](../../docs/TELEMETRY_SCHEMA.md) and [`COURSE_REQUIREMENTS.md` T12](../../COURSE_REQUIREMENTS.md).
- **Simulator-Local Assumptions**: The `warning-smoke` pre-alarm band (`300.0..499.9 PPM`) and the linear `smoke_ppm -> smoke_raw_adc` mapping are simulator-local synthetic modelling assumptions and do not modify the canonical contract or represent physical MQ-2 sensor calibration curves.

---

## 7. Stage B Hardware Handoff Boundary

This package is strictly **Stage A virtual simulation**. When physical ESP32-S3 (`YOLO_UNO_S3`) firmware is developed in Stage B under `firmware/esp32-s3/`:

1. Physical firmware must emit the exact same JSON envelope (`docs/TELEMETRY_SCHEMA.md` §3 & §8) and publish to `afes/v2/{tenant_id}/devices/{device_id}/telemetry` (`QoS 1`) or via the Local Gateway (`local-gateway/`).
2. Physical firmware **must** set:
   - `simulation.is_simulated = false`
   - `simulation.scenario_id = null`
   - `simulation.synthetic_noise_added = false`
   - `device.device_type = "YOLO_UNO_S3"` (or `"CUSTOM_SENSOR_NODE"`)
   - Hardware-burned IEEE EUI-48 MAC address from ESP32-S3 eFuse (`esp_read_mac`).
3. Physical hardware verification requires bench serial logs (`115200` baud), real sensor stimuli (DHT20 I2C, RS485 Modbus, BLE, MQ-2, optical flame), and actuator measurements as specified in [`DEVELOPMENT_GUIDE.md`](../../DEVELOPMENT_GUIDE.md).
