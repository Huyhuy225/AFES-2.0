# AFES Original System Analysis and Baseline Audit

> **Document Status**: Complete & Verified
> **Target Scope**: Architectural and code baseline audit of the original AFES repository
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Institution**: Ho Chi Minh City University of Technology (HCMUT), VNU-HCM
> **Classification**: Factual Codebase Audit & Architectural Recommendations

---

## 1. Executive Summary

This document presents a comprehensive, objective technical audit of the original **AFES (Advanced Fire Emergency System)** codebase located in the project archives. The analysis provides the factual baseline necessary to architect **AFES 2.0** for the HCMUT Internet of Things course project.

The original AFES project implemented an initial monolithic-edge fire detection prototype combining an ESP32-S3 microcontroller, a Spring Boot application server, a React/Vite dashboard, and a Mosquitto MQTT message broker. While the system demonstrated basic end-to-end telemetry and relay triggering, the codebase reveals substantial architectural deficits, protocol incompatibilities, security vulnerabilities, and complete absence of the CoreIOT platform and Local IoT Gateway tiers required by the course syllabus.

This audit separates **strictly verified observations** (derived directly from code, configuration, and manifests) from **recommendations and assumptions** guiding the AFES 2.0 implementation.

---

## 2. Verified Legacy System Architecture and Components

Based on direct examination of the original AFES repository files, the system consists of the following components:

```
AFES (Original Legacy System)
├── frontend/                     # React 18 + Vite (Submodule: afes_FE)
├── backend/                      # Java 17 + Spring Boot 3.x (Submodule: afes_BE)
├── hardware/                     # PlatformIO C++ firmware (ESP32-S3 DevKitC-1)
├── mqtt/                         # Mosquitto Broker configuration (Submodule: mqtt)
├── k8s/                          # Kubernetes deployment manifests
└── docker-compose.yml            # Multi-container local orchestration
```

### 2.1. Frontend Tier (`frontend/`)
* **Framework**: React 18.x with Vite build tooling and Tailwind CSS styling.
* **Component Library & Icons**: Lucide React icons, Chart.js for time-series visualization.
* **API Client**: Axios instance configured with `VITE_API_URL` pointing to the Spring Boot REST backend.
* **Control UI**: `ControlPanel.jsx` presents manual control actions: `pump_on`, `pump_off`, `test_alarm`, `emergency_alert`, `emergency_off`, `full_test`, `reset_system`, and `all_outputs_off`.
* **Deployment Pattern**: Hybrid deployment model with production static hosting on GitHub Pages and containerized local serving via Docker (Nginx reverse proxy on port 3000).

### 2.2. Backend Tier (`backend/`)
* **Runtime & Framework**: Java 17+, Spring Boot 3.x, Spring Data JPA with Hibernate ORM.
* **Database**: MySQL 8.4 (configured for Azure Database for MySQL or local Docker container on port 3307).
* **Messaging Integration**: Spring Integration MQTT utilizing Eclipse Paho v3 client (`MqttPahoMessageDrivenChannelAdapter` and `MqttClient`).
* **Security & Auth**: Spring Security with JWT authentication (`JwtTokenProvider`, `JwtAuthenticationFilter`, `CustomUserDetailsService`). Roles defined: `ROLE_ADMIN` and `ROLE_USER`.
* **REST Controllers**:
  * `AuthController`: User login and authentication tokens.
  * `RoomController`: Room CRUD, per-room sensor history, and room-scoped control dispatch.
  * `SensorDataController`: Public telemetry ingestion (`/api/sensors/log`) and historical query endpoints.
  * `ControlController`: Admin-only manual control dispatch to MQTT.

### 2.3. Embedded Hardware Tier (`hardware/`)
* **Toolchain & Board Target**: PlatformIO with Arduino framework on Espressif32 platform, targeting board `esp32-s3-devkitc-1` (YoloUNO form factor).
* **Core Libraries**: `knolleary/PubSubClient` (v2.8), `bblanchon/ArduinoJson` (v7.4.3), `tzapu/WiFiManager` (v2.0.17), `suculent/AESLib` (v2.3.6), `miguel5612/MQUnifiedsensor` (v3.0.5), `robtillaart/DHT20` (v0.3.2).
* **Concurrency Model**: FreeRTOS multi-tasking architecture with dedicated tasks:
  * `vTaskWifi`: WiFi connection management and reconnection.
  * `vTaskMqtt`: MQTT client connection, subscription to control topic, and publishing loop.
  * `vTaskSmoke`: Periodic reading and calibration of MQ-2 smoke sensor (ADC pin).
  * `vTaskFlame`: Periodic polling of digital/analog flame sensor pin.
  * `vTaskTemp`: I2C communication with DHT20 temperature/humidity sensor.
  * `vTaskButton`: Debounced hardware push-button polling for emergency toggle.
  * `vTaskBuzz`: Buzzer acoustic frequency modulation during alarms.
  * `vTaskLed`: Warning LED state control.
  * `vTaskPump`: Fire suppression water pump relay control.
* **Synchronization**: Three FreeRTOS mutexes (`xMqttMutex`, `xDataMutex`, `xOutputMutex`).

### 2.4. Infrastructure and Orchestration (`docker-compose.yml`, `k8s/`)
* **Local Docker Compose**: Declares four services:
  * `db`: MySQL 8.4 container with health check.
  * `mosquitto`: Custom Mosquitto MQTT broker container listening on ports 1883 and 9001 (WebSockets).
  * `backend`: Spring Boot container depending on database health and broker readiness.
  * `frontend`: Static web build container exposed on port 3000.
* **Kubernetes Manifests**: `k8s/` contains manifests for `backend-deployment.yaml`, `frontend-deployment.yaml`, `mosquitto-deployment.yaml`, `mysql-deployment.yaml`, `mysql-pvc.yaml`, `namespace.yaml`, and `secret.yaml`.
* **Submodules**: Git submodules used for `frontend` (`Huyhuy225/afes_FE`), `backend` (`Huyhuy225/afes_BE`), and `mqtt` (`nghitrung/mqtt`).

---

## 3. Verified Codebase Flaws and Incompatibilities

Direct static code inspection identified several critical protocol mismatches, architectural gaps, and vulnerabilities:

### 3.1. Telemetry Topic and Ingestion Incompatibility
* **Firmware Behavior**: The firmware publishes an aggregated JSON payload exclusively to a single hardcoded topic:
  ```cpp
  #define TOPIC_VALUE "yolo_uno/sensors/all"
  ```
* **Backend Configuration**: The backend configuration in `application.properties` subscribes to four topics:
  ```properties
  mqtt.topics=yolo_uno/sensors/flame,yolo_uno/sensors/smoke,yolo_uno/sensors/dht20,yolo_uno/sensors/all
  ```
* **Synthetic Splitting**: When `MqttReceiver.java` receives a message on `yolo_uno/sensors/all`, it decrypts the fields and synthesizes three artificial database records using non-existent source topics:
  * `saveData("yolo_uno/sensors/smoke", "Smoke Sensor", smokeVal, room);`
  * `saveData("yolo_uno/sensors/flame", "Flame Sensor", flameVal, room);`
  * `saveData("yolo_uno/sensors/dht20", "Temp Sensor", tempVal, room);`
* **Defect Impact**: The individual sensor topics (`yolo_uno/sensors/smoke`, etc.) are never published by hardware. If an external client or CoreIOT subscribes to individual topics, no telemetry is ever received.

### 3.2. Proprietary Per-Field Symmetric Encryption Flaw
* **Firmware Implementation**: The device uses AES-128-CBC encryption per individual JSON key:
  ```cpp
  doc["room_enc_value"] = encryptData(String(DEVICE_ID));
  doc["smoke_enc_value"] = encryptData(String(smoke));
  doc["flame_enc_value"] = encryptData(String(flame));
  doc["temp_enc_value"] = encryptData(String(temp));
  ```
* **Architectural Flaw**:
  * Individual string values are separately padded, AES-encrypted, and Base64-encoded, multiplying payload overhead by over 300%.
  * Cryptographic keys (`aes_key`) and initialization vectors (`AES_IV`) are hardcoded directly into C++ header/source files and Java class files.
  * Standard MQTT brokers, edge gateways, CoreIOT platforms, and rule engines cannot inspect, route, or filter telemetry because the payload structure is proprietary and opaque.
  * Any discrepancy in padding or cipher implementation silently drops all sensor data.

### 3.3. Control and Reset Command Incompatibilities
* **Command Topic and Payload**: Control commands are published to `yolo_uno/control` wrapped in an encrypted wrapper: `{"cmd_enc_value": "<cipher>"}`.
* **Firmware Command Parser**:
  `applyControlAction` in `mqtt_setup.cpp` specifically handles only the following strings:
  `pump_on`, `pump_off`, `test_alarm`, `reset_system`, `full_test`, `emergency_alert`, `emergency_off`, `auto_mode`, `all_outputs_off`.
* **Reset Mismatches**:
  1. **Generic API Mismatch**: In `ControlController.java`, the generic endpoint `@PostMapping("/api/control")` accepts a raw action string from the request body. If a frontend or API consumer sends `{"action": "reset"}`, the firmware reports:
     ```
     [CTRL] unknown action: reset
     ```
     The firmware requires `"reset_system"`, not `"reset"`.
  2. **Transient State Clearing Defect**: In `mqtt_setup.cpp`, `reset_system` zeroes manual override flags:
     ```cpp
     manual_pump_on = false; manual_alarm_on = false; manual_emergency_on = false;
     fire_alert = false; smoke_alert = false; temp_alert = false;
     ```
     However, the autonomous FreeRTOS tasks (`vTaskSmoke`, `vTaskFlame`, `vTaskTemp`) execute continuous while-loops. If physical sensor readings remain above threshold (or during the initial warmup window), the sensor tasks immediately re-assert `smoke_alert = true` and `fire_alert = true` within 50–100 milliseconds, defeating the reset command without operator feedback.
  3. **No Command Acknowledgment**: The firmware provides no MQTT response topic (e.g., `yolo_uno/control/ack`) to confirm whether an action was accepted, ignored due to `roomId` mismatch, or rejected due to syntax errors. The backend assumes success unconditionally.

### 3.4. Security and Credential Vulnerabilities
* **Committed Secrets**: Database connection strings, administrative usernames, database passwords, and MQTT broker access tokens were committed directly into `application.properties`, `docker-compose.yml`, and `k8s/secret.yaml`.
* **Static Cryptographic Keys**: Hardcoded 128-bit AES keys and IVs are shared globally across all devices and backend services.
* **Unprotected REST Ingestion**: In `SensorDataController.java`, the endpoint `@PostMapping("/api/sensors/log")` is annotated with `@PreAuthorize("permitAll()")`. Any client on the network can inject arbitrary sensor data into the database without authentication or rate limiting.
* **Missing Transport Security**: MQTT communication between ESP32 and Mosquitto operates over unencrypted TCP port 1883 without TLS.

---

## 4. Assessment of Absent Course Requirements (T01–T15)

The HCMUT IoT Course Syllabus (Semester 261) specifies fifteen required technology elements (T01–T15) across five groups. The original AFES codebase implements almost none of these required elements:

| Group | Code | Technology Element | Original AFES Status | Verified Codebase Finding |
|---|---|---|---|---|
| **Sensors** | **T01** | Sensor using I2C on Tasmota | **ABSENT** | DHT20 used raw Arduino library; Tasmota firmware not utilized. |
| | **T02** | Sensor using Modbus RS485 | **ABSENT** | No RS485 hardware transceiver, Modbus master, or RTU driver. |
| | **T03** | Sensor connected via BLE | **ABSENT** | ESP32-S3 BLE stack is uninitialized; only Wi-Fi STA mode used. |
| **TinyML** | **T04** | TinyML AI inference on device | **ABSENT** | Hardcoded scalar threshold checks; no TensorFlow Lite Micro or Edge Impulse model. |
| | **T05** | Tooling for data collection & training | **ABSENT** | No dataset recording scripts, feature extraction, or model export pipelines. |
| **Local Comms** | **T06** | Wireless communication via ESP-NOW | **ABSENT** | Standard Wi-Fi connection only; ESP-NOW peer-to-peer unconfigured. |
| | **T07** | On-device self-implemented web server | **ABSENT** | No HTTP server running on ESP32; relies entirely on external backend. |
| **Local Gateway** | **T08** | IoT Gateway on PC/Pi aggregating data | **ABSENT** | Nodes connect directly to cloud/central Mosquitto; no local edge gateway tier. |
| | **T09** | AI function running on Local IoT Gateway | **ABSENT** | No gateway-level computer vision, time-series anomaly detection, or edge ML. |
| | **T10** | Monitoring/control UI on Local Gateway | **ABSENT** | No local touchscreen, CLI, or local web UI for gateway operations. |
| **CoreIOT** | **T11** | CoreIOT templates, dashboards, control | **ABSENT** | No ThingsBoard/CoreIOT entity profiles, dashboards, or widgets. |
| | **T12** | CoreIOT RuleChain smart features | **ABSENT** | No RuleChain definitions; alarm logic hardcoded in Java and C++. |
| | **T13** | Alert notifications on threshold | **PARTIAL/ABSENT** | Local buzzer and backend log exist, but no CoreIOT alarm triggers or notifications. |
| | **T14** | OTA firmware updates for devices | **ABSENT** | Flashing requires wired USB connection; no OTA update service or CoreIOT OTA package. |
| | **T15** | CoreIOT Gateway synchronized with Local Gateway | **ABSENT** | No CoreIOT Gateway connector, MQTT mapping, or state sync mechanism. |

---

## 5. Licensing and Attribution Audit

* **Firmware License Header**: `hardware/LICENSE` contains:
  ```text
  MIT License
  Copyright (c) 2026 ng_trung1405
  ```
* **Git Submodule Origins**:
  * `frontend`: `https://github.com/Huyhuy225/afes_FE` (owned by Huyhuy225)
  * `backend`: `https://github.com/Huyhuy225/afes_BE` (owned by Huyhuy225)
  * `mqtt`: `https://github.com/nghitrung/mqtt` (external personal repo)
* **Academic Integrity Requirement**: To comply with HCMUT academic honesty guidelines:
  1. The original repository must be explicitly cited in the course report.
  2. Third-party contributions (e.g., `ng_trung1405`) must be acknowledged.
  3. AFES 2.0 must clearly distinguish re-architected contracts, new gateway modules, CoreIOT assets, and simulation tools from legacy code.
  4. No proprietary keys or credentials from external repositories may be replicated in AFES 2.0.

---

## 6. Summary Matrix: Verified Legacy Facts vs. AFES 2.0 Target

| Dimension | Original AFES (Verified Legacy) | AFES 2.0 (Target Contract) |
|---|---|---|
| **Architecture Model** | 3-tier: ESP32 $\to$ Mosquitto $\to$ Spring Boot $\to$ React | 5-tier: ESP32 $\to$ Local Gateway $\to$ CoreIOT $\leftrightarrow$ Backend $\leftrightarrow$ Frontend |
| **Telemetry Topics** | Single monolithic topic `yolo_uno/sensors/all` | Hierarchical: `afes/v2/{tenant}/devices/{device}/telemetry` |
| **Payload Format** | Custom AES-128-CBC encrypted strings per field | Open, standardized JSON Schema v2.0 with type safety and metadata |
| **Simulation Marker** | None; all data assumed to be physical hardware | Explicit `is_simulated: true/false` envelope flag for Stage A/B |
| **Command Protocol** | Proprietary encrypted command string without ACK | Standardized RPC contract with idempotency key and ACK status |
| **Platform Cloud** | None (pure custom Spring Boot & Mosquitto) | CoreIOT Platform (ThingsBoard-based) with RuleChain, OTA, Alarms |
| **Edge Processing** | Hardcoded threshold comparators in C++ | Local Gateway aggregation, offline buffering, and Edge AI (T08, T09) |
| **Sensors** | Physical MQ-2, Flame, DHT20 only | I2C Tasmota (T01), Modbus RS485 (T02), BLE (T03), Virtual Nodes |
| **Security Model** | Hardcoded secrets, static AES keys, open REST ingest | Vault/Environment secrets, JWT RBAC, TLS, no browser CoreIOT tokens |

---

## 7. Migration Recommendations for AFES 2.0

1. **Adopt Open Telemetry Schema**: Deprecate custom per-field AES encryption in favor of standard TLS transport security and open JSON schema envelopes (`[TELEMETRY_SCHEMA.md](TELEMETRY_SCHEMA.md)`).
2. **Implement Local IoT Gateway Tier**: Create a standalone Python or Node-based Local Gateway service (`gateway/`) capable of aggregating local sensor traffic, running edge AI anomaly detection, buffering data during network outages, and interfacing with CoreIOT.
3. **CoreIOT Platform Integration**: Provision CoreIOT device profiles, telemetry mappings, RuleChains for automated alarms, and dashboards mapping to requirements T11–T15.
4. **Secure Backend Proxy Pattern**: Re-engineer the Spring Boot backend to act strictly as a secure business facade and RBAC provider. Browser frontends must never directly hold CoreIOT administrative credentials.
5. **Stage A / Stage B Decoupling**: Build robust virtual simulation nodes with the `is_simulated` marker to enable end-to-end testing and contract verification before deploying physical ESP32-S3 hardware.
