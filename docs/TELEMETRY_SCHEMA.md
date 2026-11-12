# AFES 2.0 Telemetry and Event Schema Specification

> **Specification Version**: 2.0.0
> **Status**: Approved Architecture Baseline
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Target Audience**: Firmware Engineers, Gateway Developers, Backend Engineers, CoreIOT Integrators

---

## 1. Specification Overview

The **AFES 2.0 Telemetry and Event Schema** defines the standardized, versioned contract for all data exchange between sensing nodes (ESP32-S3 / virtual simulators), the Local IoT Gateway, the platform-neutral CoreIOT platform, and the Application Backend.

This specification replaces the legacy, proprietary per-field AES encryption mechanism with an open, structured JSON schema enforced at transport boundaries via standard TLS and JWT/token authentication.

### 1.1. Key Principles
1. **Dual-Stage Lifecycle (Stage A / Stage B)**: All payloads carry an explicit `simulation` object with the `is_simulated` boolean flag to cleanly segregate Stage A virtual simulation data from Stage B physical hardware measurements.
2. **Deterministic Idempotency**: Every telemetry packet and event message includes a globally unique `message_id` (UUID v4) and monotonic epoch timestamp to eliminate duplicate processing and detect out-of-order delivery.
3. **Zoning and Multi-Tenancy**: Payloads carry device, zone, and gateway coordinates, supporting multi-node room monitoring and spatial localization.
4. **Local-Gateway-First Architecture**: Sensing nodes route telemetry through the Local IoT Gateway as the primary path for aggregation, edge intelligence, and offline resilience, with platform-specific CoreIOT mappings deferred to Issue #3.

---

## 2. MQTT Topic Hierarchy

AFES 2.0 establishes a clean, hierarchical MQTT topic structure:

```
afes/v2/{tenant_id}/devices/{device_id}/telemetry
afes/v2/{tenant_id}/devices/{device_id}/status
afes/v2/{tenant_id}/devices/{device_id}/events
afes/v2/{tenant_id}/devices/{device_id}/command/req
afes/v2/{tenant_id}/devices/{device_id}/command/res
afes/v2/{tenant_id}/gateways/{gateway_id}/telemetry
afes/v2/{tenant_id}/gateways/{gateway_id}/status
```

### 2.1. Topic Descriptions

| Topic Pattern | Direction | QoS | Description |
|---|---|---|---|
| `afes/v2/{tenant_id}/devices/{device_id}/telemetry` | Node $\to$ Gateway / Broker | 1 | Periodic environmental telemetry published by an individual sensing node. |
| `afes/v2/{tenant_id}/devices/{device_id}/status` | Node $\to$ Gateway / Broker | 1 (Retained) | Node connection state and Last Will and Testament (LWT: `ONLINE`, `OFFLINE`). |
| `afes/v2/{tenant_id}/devices/{device_id}/events` | Node $\to$ Gateway / Broker | 2 | High-priority asynchronous state transitions, threshold triggers, and emergency alarms. |
| `afes/v2/{tenant_id}/devices/{device_id}/command/req` | CoreIOT / Gateway $\to$ Node | 1 | Downlink RPC actuator commands (buzzer, pump, reset, test, emergency shutdown). |
| `afes/v2/{tenant_id}/devices/{device_id}/command/res` | Node $\to$ CoreIOT / Gateway | 1 | Uplink command execution acknowledgment and status code. |
| `afes/v2/{tenant_id}/gateways/{gateway_id}/telemetry` | Local Gateway $\to$ CoreIOT | 1 | Batch-aggregated telemetry forwarded by the Local IoT Gateway (primary path). |
| `afes/v2/{tenant_id}/gateways/{gateway_id}/status` | Local Gateway $\to$ CoreIOT | 1 (Retained) | Local Gateway health, resource consumption, and connectivity state. |

### 2.2. CoreIOT Integration and Local Gateway Primary Path

In AFES 2.0, the **Local IoT Gateway** (`afes/v2/{tenant_id}/gateways/{gateway_id}/telemetry`) serves as the primary, approved ingestion path for sensing nodes connecting to CoreIOT.

To maintain platform neutrality and prevent unconfirmed vendor assumptions:
* The telemetry envelope defined in this specification serves as the canonical domain contract.
* Direct platform-specific topic mappings, attribute payloads, provisioning handshakes, and gateway synchronization RPC contracts for CoreIOT are platform-neutral at this stage and formally specified in [Issue #3 (Prepare secure CoreIOT project onboarding plan)](https://github.com/Huyhuy225/AFES-2.0/issues/3).

---

## 3. Telemetry Payload Specification

### 3.1. Envelope Data Dictionary

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | String | Yes | Contract version. Must be `"2.0"`. |
| `message_id` | String | Yes | UUID v4 unique identifier for idempotency and deduplication. |
| `correlation_id` | String | No | References a prior command `request_id` if emitted in response to RPC. |
| `device` | Object | Yes | Device hardware and identity metadata. |
| `device.device_id` | String | Yes | Unique alphanumeric hardware identifier (e.g., `"ESP32S3-Z1-01"`). |
| `device.device_type` | String | Yes | `"YOLO_UNO_S3"`, `"VIRTUAL_SIM_NODE"`, or `"CUSTOM_SENSOR_NODE"`. |
| `device.firmware_version`| String | Yes | Semantic firmware version (e.g., `"2.1.0-stageA"`). |
| `device.hardware_version`| String | Yes | Hardware revision (e.g., `"v1.2"` or `"SIM-v2"`). |
| `device.mac_address` | String | Yes | EUI-48 physical MAC address or simulated virtual MAC. |
| `zone` | Object | Yes | Spatial positioning within the facility. |
| `zone.zone_id` | String | Yes | Logical zone identifier (e.g., `"ZONE-A-FL1"`). |
| `zone.room_code` | String | Yes | Room identifier (e.g., `"ROOM-101"`). |
| `zone.building_id` | String | Yes | Building identifier (e.g., `"BLDG-CSE-B1"`). |
| `zone.floor_level` | Integer | Yes | Numeric floor level (e.g., `1`). |
| `gateway` | Object | Yes | Local gateway metadata. |
| `gateway.gateway_id` | String | Yes | Gateway identifier (e.g., `"GW-LOCAL-PC01"` or `"DIRECT"`). |
| `gateway.protocol` | String | Yes | Ingestion protocol: `"MQTT"`, `"ESP_NOW"`, `"BLE"`, `"MODBUS_RS485"`. |
| `gateway.mesh_role` | String | Yes | Node topology role: `"ENDPOINT"`, `"REPEATER"`, or `"GATEWAY"`. |
| `timestamps` | Object | Yes | Monotonic and UTC wall-clock time records. |
| `timestamps.timestamp_utc` | String | Yes | ISO 8601 UTC timestamp (`YYYY-MM-DDTHH:mm:ss.sssZ`). |
| `timestamps.timestamp_epoch_ms` | Integer | Yes | Unix epoch milliseconds timestamp (int64). |
| `timestamps.device_uptime_s` | Integer | Yes | Microcontroller uptime in seconds since boot. |
| `status` | Object | Yes | Operating and self-diagnostic state. |
| `status.system_state` | String | Yes | `"NORMAL"`, `"WARNING"`, `"CRITICAL"`, `"MAINTENANCE"`, `"FAULT"`. |
| `status.sensor_health`| String | Yes | `"HEALTHY"`, `"DEGRADED"`, `"WARMING_UP"`, `"ERROR"`. |
| `status.battery_pct` | Number | No | Battery percentage (`0.0`–`100.0`) or `null` for mains power. |
| `status.rssi_dbm` | Integer | Yes | Wi-Fi / ESP-NOW received signal strength in dBm. |
| `readings` | Object | Yes | Measured environmental sensor values. |
| `readings.temperature` | Number | Yes | Ambient temperature in degrees Celsius (°C). |
| `readings.humidity` | Number | Yes | Relative humidity in percentage (%RH). |
| `readings.smoke_ppm` | Number | Yes | Calibrated smoke concentration in Parts Per Million (PPM). |
| `readings.smoke_raw_adc` | Integer | Yes | Raw 12-bit ADC reading (`0`–`4095`) from analog front-end. |
| `readings.flame_detected` | Boolean | Yes | Optical flame presence detection flag. |
| `readings.flame_raw_adc` | Integer | Yes | Raw flame sensor ADC value (`0`–`4095`). |
| `readings.gas_co_ppm` | Number | No | Carbon monoxide concentration in PPM (optional). |
| `readings.ai_inferred_fire_risk` | Number | No | On-device TinyML / Edge AI fire probability (`0.0`–`1.0`). |
| `readings.ai_classification` | String | No | Classification label: `"NORMAL"`, `"SMOKE_SPIKE"`, `"FIRE"`. |
| `actuators` | Object | Yes | Local actuator states on the node. |
| `actuators.buzzer_active` | Boolean | Yes | Acoustic alarm siren active state. |
| `actuators.alarm_led_active` | Boolean | Yes | Visual warning beacon/strobe active state. |
| `actuators.water_pump_relay_active` | Boolean | Yes | Fire suppression relay state. |
| `actuators.exhaust_fan_active` | Boolean | No | Ventilation exhaust relay state. |
| `actuators.override_mode` | String | Yes | `"AUTO"`, `"MANUAL_OVERRIDE"`, or `"EMERGENCY_LOCK"`. |
| `simulation` | Object | Yes | Explicit simulation marker for course compliance. |
| `simulation.is_simulated`| Boolean | Yes | `true` for Stage A simulation; `false` for Stage B physical hardware. |
| `simulation.scenario_id`| String | No | Simulated scenario ID (e.g., `"SCENARIO_SMOKE_SPIKE_03"`). |
| `simulation.synthetic_noise_added` | Boolean | Yes | Indicates whether synthetic Gaussian noise was injected. |

---

## 4. Asynchronous Alarm and Event Schema

Events and threshold violations are published immediately upon trigger without waiting for the periodic telemetry cycle.

### 4.1. Event Payload Structure

```json
{
  "schema_version": "2.0",
  "event_id": "evt-7a91fc32-94f1-4820-928d-1901a88bb4a2",
  "timestamp_utc": "2026-11-12T04:15:30.120Z",
  "timestamp_epoch_ms": 1794456930120,
  "device_id": "ESP32S3-Z1-01",
  "zone_id": "ZONE-A-FL1",
  "room_code": "ROOM-101",
  "event_type": "FIRE_ALARM_CRITICAL",
  "severity": "CRITICAL",
  "trigger_source": "MULTI_SENSOR_FUSION",
  "trigger_details": {
    "temperature_c": 64.2,
    "temperature_threshold_c": 50.0,
    "smoke_ppm": 850.5,
    "smoke_threshold_ppm": 500.0,
    "flame_detected": true,
    "tinyml_fire_confidence": 0.94
  },
  "autonomous_actions_taken": [
    "LOCAL_BUZZER_ACTIVE",
    "LOCAL_PUMP_ENGAGED",
    "EMERGENCY_LOCK_ENGAGED"
  ],
  "ack_required": true,
  "ack_status": "PENDING",
  "simulation": {
    "is_simulated": true,
    "scenario_id": "STAGE_A_FLASH_FIRE_TEST"
  }
}
```

### 4.2. Event Types and Severities

| Event Type | Severity | Description |
|---|---|---|
| `SYSTEM_BOOT` | `INFO` | Microcontroller boot or restart event with reset reason. |
| `SENSOR_WARMUP_COMPLETE` | `INFO` | MQ-2 / MQ-135 heating cycle completed; readings valid. |
| `HEARTBEAT` | `INFO` | Periodic health confirmation packet. |
| `SMOKE_THRESHOLD_WARNING` | `WARNING` | Smoke PPM exceeded pre-alarm warning threshold. |
| `TEMP_THRESHOLD_WARNING` | `WARNING` | Ambient temperature exceeded normal baseline warning threshold. |
| `SENSOR_DISCONNECT_FAULT` | `WARNING` | I2C / Modbus sensor communication timed out or failed CRC. |
| `FIRE_ALARM_CRITICAL` | `CRITICAL` | Confirmed fire detected via flame sensor, smoke, and temperature fusion. |
| `MANUAL_PANIC_ENGAGED` | `CRITICAL` | Hardware push-button emergency override activated. |
| `FAILSAFE_SHUTDOWN` | `CRITICAL` | Hardware self-protection due to overcurrent or thermal limit. |

---

## 5. Downlink Actuator Control (RPC) Schema

Downlink commands sent from CoreIOT or the Application Backend to devices use an explicit request/response contract.

### 5.1. Downlink Request (`command/req`)

```json
{
  "schema_version": "2.0",
  "request_id": "cmd-d4b89211-12c8-4712-b13a-96ea9d880401",
  "target_device_id": "ESP32S3-Z1-01",
  "target_zone_id": "ZONE-A-FL1",
  "action": "PUMP_ON",
  "parameters": {
    "duration_ms": 15000,
    "override_safety_lock": false
  },
  "issuer": {
    "user_id": "usr-admin-01",
    "role": "ROLE_ADMIN",
    "client_ip": "192.168.1.100"
  },
  "idempotency_key": "idemp-20261112-00412",
  "timestamp_epoch_ms": 1794456950000,
  "timeout_ms": 5000
}
```

### 5.2. Permitted Actions

| Action String | Description | Default Duration |
|---|---|---|
| `PUMP_ON` | Engages water pump relay. | 15,000 ms |
| `PUMP_OFF` | Disengages water pump relay. | Immediate |
| `TEST_ALARM` | Tests siren and warning strobe. | 5,000 ms |
| `FULL_SYSTEM_TEST`| Sequentially tests LED, buzzer, and pump relay. | 10,000 ms |
| `EMERGENCY_SHUTDOWN` | Engages all suppression outputs and locks state. | 30,000 ms |
| `EMERGENCY_RELEASE` | Clears emergency override and returns to AUTO mode. | Immediate |
| `RESET_ALERTS` | Acknowledges and resets latched sensor alerts. | Immediate |
| `REBOOT_DEVICE` | Commands software microcontroller restart. | Immediate |

### 5.3. Downlink Response (`command/res`)

```json
{
  "schema_version": "2.0",
  "request_id": "cmd-d4b89211-12c8-4712-b13a-96ea9d880401",
  "device_id": "ESP32S3-Z1-01",
  "action": "PUMP_ON",
  "status": "SUCCESS",
  "status_code": 200,
  "message": "Water pump relay energized for 15000 ms",
  "timestamp_epoch_ms": 1794456950150,
  "execution_duration_ms": 150,
  "current_actuator_state": {
    "water_pump_relay_active": true,
    "override_mode": "MANUAL_OVERRIDE"
  }
}
```

---

## 6. Deduplication and Idempotency Strategy

To prevent duplicate processing caused by MQTT QoS 1 re-transmissions or network buffering:

1. **Deterministic Message Fingerprinting**:
   The unique tuple `(device_id, message_id)` serves as the primary idempotency key.
2. **Gateway and Ingestion De-duplication Cache**:
   The Local Gateway and Backend maintain an in-memory Sliding Window LRU Cache (retention window and capacity configurable; baseline targets marked TBD during gateway performance benchmarking). If a packet with an existing `message_id` arrives within the active window, it is logged as duplicate and dropped before database write.
3. **Out-of-Order Handling**:
   Packets arriving with `timestamp_epoch_ms` significantly older than the last persisted reading (configurable threshold, default marked TBD) are tagged with `status.quality = "OUT_OF_ORDER"` and inserted into historical archives without updating real-time zone summaries.

---

## 7. Concrete Examples

### 7.1. Stage A Simulation Telemetry Packet

```json
{
  "schema_version": "2.0",
  "message_id": "c1f3b392-563b-4866-9e67-d86bfa2549a1",
  "correlation_id": null,
  "device": {
    "device_id": "SIM-ESP32-101",
    "device_type": "VIRTUAL_SIM_NODE",
    "firmware_version": "2.0.0-sim",
    "hardware_version": "VIRTUAL-NODE",
    "mac_address": "02:00:00:AA:BB:01"
  },
  "zone": {
    "zone_id": "ZONE-101",
    "room_code": "ROOM-101",
    "building_id": "BLDG-CSE",
    "floor_level": 1
  },
  "gateway": {
    "gateway_id": "GW-LOCAL-PC01",
    "protocol": "MQTT",
    "mesh_role": "ENDPOINT"
  },
  "timestamps": {
    "timestamp_utc": "2026-11-12T04:20:00.000Z",
    "timestamp_epoch_ms": 1794457200000,
    "device_uptime_s": 3600
  },
  "status": {
    "system_state": "NORMAL",
    "sensor_health": "HEALTHY",
    "battery_pct": null,
    "rssi_dbm": -55
  },
  "readings": {
    "temperature": 27.8,
    "humidity": 62.4,
    "smoke_ppm": 120.3,
    "smoke_raw_adc": 820,
    "flame_detected": false,
    "flame_raw_adc": 110,
    "gas_co_ppm": 4.2,
    "ai_inferred_fire_risk": 0.02,
    "ai_classification": "NORMAL"
  },
  "actuators": {
    "buzzer_active": false,
    "alarm_led_active": false,
    "water_pump_relay_active": false,
    "exhaust_fan_active": false,
    "override_mode": "AUTO"
  },
  "simulation": {
    "is_simulated": true,
    "scenario_id": "BASELINE_MONITORING_SCENARIO",
    "synthetic_noise_added": true
  }
}
```

### 7.2. Stage B Physical Hardware Telemetry Packet

```json
{
  "schema_version": "2.0",
  "message_id": "f8e43477-84bc-40d1-9252-78d102e3b2e9",
  "correlation_id": null,
  "device": {
    "device_id": "ESP32S3-YOLO-01",
    "device_type": "YOLO_UNO_S3",
    "firmware_version": "2.0.0-prod",
    "hardware_version": "ESP32-S3-DevKitC-1-v1.1",
    "mac_address": "84:F7:03:1A:2B:3C"
  },
  "zone": {
    "zone_id": "ZONE-101",
    "room_code": "ROOM-101",
    "building_id": "BLDG-CSE",
    "floor_level": 1
  },
  "gateway": {
    "gateway_id": "GW-LOCAL-RPI4",
    "protocol": "ESP_NOW",
    "mesh_role": "ENDPOINT"
  },
  "timestamps": {
    "timestamp_utc": "2026-11-12T04:22:15.842Z",
    "timestamp_epoch_ms": 1794457335842,
    "device_uptime_s": 8421
  },
  "status": {
    "system_state": "NORMAL",
    "sensor_health": "HEALTHY",
    "battery_pct": null,
    "rssi_dbm": -68
  },
  "readings": {
    "temperature": 29.4,
    "humidity": 58.1,
    "smoke_ppm": 145.0,
    "smoke_raw_adc": 910,
    "flame_detected": false,
    "flame_raw_adc": 85,
    "gas_co_ppm": 2.1,
    "ai_inferred_fire_risk": 0.04,
    "ai_classification": "NORMAL"
  },
  "actuators": {
    "buzzer_active": false,
    "alarm_led_active": false,
    "water_pump_relay_active": false,
    "exhaust_fan_active": false,
    "override_mode": "AUTO"
  },
  "simulation": {
    "is_simulated": false,
    "scenario_id": null,
    "synthetic_noise_added": false
  }
}
```

---

## 8. Formal JSON Schema (Draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AFES2TelemetryPayload",
  "type": "object",
  "required": [
    "schema_version",
    "message_id",
    "device",
    "zone",
    "gateway",
    "timestamps",
    "status",
    "readings",
    "actuators",
    "simulation"
  ],
  "properties": {
    "schema_version": { "type": "string", "enum": ["2.0"] },
    "message_id": { "type": "string", "format": "uuid" },
    "correlation_id": { "type": ["string", "null"] },
    "device": {
      "type": "object",
      "required": ["device_id", "device_type", "firmware_version", "hardware_version", "mac_address"],
      "properties": {
        "device_id": { "type": "string", "minLength": 3 },
        "device_type": { "type": "string" },
        "firmware_version": { "type": "string" },
        "hardware_version": { "type": "string" },
        "mac_address": { "type": "string" }
      }
    },
    "zone": {
      "type": "object",
      "required": ["zone_id", "room_code", "building_id", "floor_level"],
      "properties": {
        "zone_id": { "type": "string" },
        "room_code": { "type": "string" },
        "building_id": { "type": "string" },
        "floor_level": { "type": "integer" }
      }
    },
    "gateway": {
      "type": "object",
      "required": ["gateway_id", "protocol", "mesh_role"],
      "properties": {
        "gateway_id": { "type": "string" },
        "protocol": { "type": "string", "enum": ["MQTT", "ESP_NOW", "BLE", "MODBUS_RS485", "DIRECT"] },
        "mesh_role": { "type": "string", "enum": ["ENDPOINT", "REPEATER", "GATEWAY"] }
      }
    },
    "timestamps": {
      "type": "object",
      "required": ["timestamp_utc", "timestamp_epoch_ms", "device_uptime_s"],
      "properties": {
        "timestamp_utc": { "type": "string", "format": "date-time" },
        "timestamp_epoch_ms": { "type": "integer" },
        "device_uptime_s": { "type": "integer" }
      }
    },
    "status": {
      "type": "object",
      "required": ["system_state", "sensor_health", "rssi_dbm"],
      "properties": {
        "system_state": { "type": "string", "enum": ["NORMAL", "WARNING", "CRITICAL", "MAINTENANCE", "FAULT"] },
        "sensor_health": { "type": "string", "enum": ["HEALTHY", "DEGRADED", "WARMING_UP", "ERROR"] },
        "battery_pct": { "type": ["number", "null"] },
        "rssi_dbm": { "type": "integer" }
      }
    },
    "readings": {
      "type": "object",
      "required": [
        "temperature",
        "humidity",
        "smoke_ppm",
        "smoke_raw_adc",
        "flame_detected",
        "flame_raw_adc"
      ],
      "properties": {
        "temperature": { "type": "number" },
        "humidity": { "type": "number" },
        "smoke_ppm": { "type": "number" },
        "smoke_raw_adc": { "type": "integer", "minimum": 0, "maximum": 4095 },
        "flame_detected": { "type": "boolean" },
        "flame_raw_adc": { "type": "integer", "minimum": 0, "maximum": 4095 },
        "gas_co_ppm": { "type": "number" },
        "ai_inferred_fire_risk": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "ai_classification": { "type": "string" }
      }
    },
    "actuators": {
      "type": "object",
      "required": [
        "buzzer_active",
        "alarm_led_active",
        "water_pump_relay_active",
        "override_mode"
      ],
      "properties": {
        "buzzer_active": { "type": "boolean" },
        "alarm_led_active": { "type": "boolean" },
        "water_pump_relay_active": { "type": "boolean" },
        "exhaust_fan_active": { "type": "boolean" },
        "override_mode": { "type": "string", "enum": ["AUTO", "MANUAL_OVERRIDE", "EMERGENCY_LOCK"] }
      }
    },
    "simulation": {
      "type": "object",
      "required": ["is_simulated", "synthetic_noise_added"],
      "properties": {
        "is_simulated": { "type": "boolean" },
        "scenario_id": { "type": ["string", "null"] },
        "synthetic_noise_added": { "type": "boolean" }
      }
    }
  }
}
```
