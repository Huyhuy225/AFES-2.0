# AFES 2.0 – System Integration Plan and Verification Protocols

> **Document Version**: 2.0.0
> **Status**: DRAFT — pending Technical Lead approval
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Course**: Internet of Things (IoT) – Semester 261 (HCMUT)
> **Documentation Location**: `docs/project-management/INTEGRATION_PLAN.md`

---

## 1. System Integration Principles and Stage Boundaries

The AFES 2.0 integration strategy systematically brings together the five tiers of the architecture:
* **Tier 1: Sensing Nodes** (Stage A: `tools/mock_simulator/` [Planned path]; Stage B: `firmware/esp32-s3/` [Planned path])
* **Tier 2: Local IoT Gateway** (`local-gateway/src/engine/`, `edge_ai/`, `ui/` [Planned paths])
* **Tier 3: CoreIOT Platform** (`coreiot/dashboards/`, `rulechains/`, `notifications/` [Planned paths])
* **Tier 4: Application Server** (`backend/` [Planned path] Spring Boot 3 REST and STOMP WebSocket service)
* **Tier 5: Presentation Layer** (`frontend/` [Actual source] React 18 / Vite Operations Dashboard)

Integration executes in two distinct chronological stages:
1. **Stage A Integration (Virtual Simulation & Contract Verification)**: Focuses exclusively on automated contract validation, MQTT topic serialization, REST schemas, WebSocket event streams, and error propagation using pure software simulators and local brokers. No physical electronics are powered.
2. **Stage B Integration (Physical Hardware-in-the-Loop)**: Focuses on physical sensor bus integrity (I2C, Modbus RS485, BLE), RF mesh stability (ESP-NOW, Wi-Fi), microcontroller memory constraints, on-device TinyML inference latency, and physical relay actuation in the laboratory.

---

## 2. Progressive Integration Phases

```
+---------------------------------------------------------------------------------------------------+
| PHASE INT-1: Stage A Edge Contract Verification (Simulator <--> Local Gateway MQTT)               |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE INT-2: Stage A Fullstack Local Pipeline (Gateway <--> Spring Boot Backend <--> React SPA)   |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE INT-3: CoreIOT Cloud Sandbox Integration (Local Gateway <--> CoreIOT Hub <--> Backend)     |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE INT-4: Stage B Hardware-in-the-Loop Commissioning (ESP32-S3 Physical Nodes <--> Gateway)    |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE INT-5: End-to-End System Commissioning & Emergency Evacuation Simulation                   |
+---------------------------------------------------------------------------------------------------+
```

### Phase INT-1: Stage A Edge Contract Verification
* **Scope**: Virtual Telemetry Simulator (`tools/mock_simulator/` [Planned deliverable path]) $\longleftrightarrow$ Local IoT Gateway (`local-gateway/src/engine/` [Planned deliverable path]).
* **Implementation State**: `NOT_STARTED` (Simulator in Issue #6, Gateway in Issue #7; assignable to Khánh upon acceptance).
* **Interface Contract**: [`docs/TELEMETRY_SCHEMA.md`](../TELEMETRY_SCHEMA.md) (`DOCUMENTED`).
* **Integration Steps**:
  1. Launch local Mosquitto MQTT broker on `localhost:1883`.
  2. Start telemetry simulator emitting multi-zone synthetic records flagged with `simulation.is_simulated = true`.
  3. Start Local Gateway engine; verify subscription to `afes/v2/{tenant_id}/devices/{device_id}/telemetry`.
  4. Validate schema conformance, timestamp monotonicity, and SQLite offline buffering.
  5. Issue mock downlink command via `afes/v2/{tenant_id}/devices/{device_id}/command/req` and verify execution receipt on `.../command/res`.
* **Success Verification Gate**: 100 consecutive synthetic packets ingested without JSON parsing errors or schema drops; offline SQLite table correctly records packets during broker interruption.

### Phase INT-2: Stage A Fullstack Local Pipeline
* **Scope**: Local Gateway (`local-gateway/` [Planned path]) $\longleftrightarrow$ Spring Boot Backend (`backend/` [Planned path]) $\longleftrightarrow$ React Frontend (`frontend/` [Actual source]).
* **Implementation State**: `NOT_STARTED` (Backend scheduled for M4; Frontend Stage A baseline `TESTED` locally in commit `bb5bba7`).
* **Interface Contract**: [`docs/API_SPECIFICATION.md`](../API_SPECIFICATION.md) (`DOCUMENTED`).
* **Integration Steps**:
  1. Boot Spring Boot backend connected to local MySQL container.
  2. Local Gateway submits batched telemetry via `/api/v2/telemetry/ingest`.
  3. Launch frontend dashboard with `VITE_USE_MOCK_DATA=false` pointing to `http://localhost:8080/api/v2`.
  4. Verify live data rendering in `ZoneCard`, `DeviceList`, and `TelemetryChart`.
  5. Trigger manual alarm acknowledgment and control command; verify backend database update and STOMP event broadcast to connected frontend sessions.
* **Success Verification Gate**: Zero fallback to `mockStore` during live operation; mutation errors correctly bubble up to UI `ErrorBanner` if backend rejects requests.

### Phase INT-3: CoreIOT Cloud Sandbox Integration
* **Scope**: Local Gateway $\longleftrightarrow$ CoreIOT Platform Hub $\longleftrightarrow$ Spring Boot Backend.
* **Implementation State**: `BLOCKED` (Blocked on CoreIOT onboarding in Issue #3; owned by Technical Lead Huy).
* **Interface Contract**: Course Elements **T11, T12, T13, T15** (`DOCUMENTED`).
* **Integration Steps**:
  1. Provision CoreIOT tenant, device profiles, and gateway credentials per `docs/COREIOT_ONBOARDING.md` (Planned deliverable).
  2. Configure Local Gateway CoreIOT sync module (`local-gateway/src/coreiot_sync/` [Planned path]) with secure gateway access token.
  3. Validate automatic child device provisioning in CoreIOT dashboard (Course T15).
  4. Inject simulated thermal spike $> 50^\circ\text{C}$; verify CoreIOT RuleChain triggers automated pump RPC (Course T12).
  5. Verify CoreIOT notification rule dispatches alert email / webhook (Course T13).
* **Success Verification Gate**: Gateway appears `ONLINE` in CoreIOT dashboard; bidirectional RPC latency target TBD pending measurement plan.

### Phase INT-4: Stage B Hardware-in-the-Loop Commissioning
* **Scope**: Physical ESP32-S3 (YoloUNO) $\longleftrightarrow$ Physical Sensors $\longleftrightarrow$ Local Gateway.
* **Implementation State**: `NOT_STARTED` (Scheduled for Milestone 5).
* **Interface Contract**: Course Elements **T01, T02, T03, T04, T05, T06, T07, T14** (`DOCUMENTED`).
* **Integration Steps**:
  1. Wire I2C DHT20 sensor to ESP32-S3; verify sensor address on I2C bus scan (Course T01).
  2. Wire MAX485 transceiver to UART pins; verify Modbus RTU register polling (Course T02).
  3. Pair ESP32-S3 with BLE environmental beacon; verify GATT notifications (Course T03).
  4. Flash on-device TinyML TFLite Micro model; benchmark inference latency on physical CPU (Course T04).
  5. Transmit telemetry frames over ESP-NOW 2.4GHz RF to receiving gateway board (Course T06).
  6. Access on-device web server over SoftAP/LAN (Course T07).
  7. Deploy remote OTA update package from CoreIOT; verify firmware reboot and version increment (Course T14).
* **Success Verification Gate**: Continuous sensor streaming (duration target TBD pending measurement plan) without bus lockups, memory leaks, or unhandled FreeRTOS watchdog resets.

### Phase INT-5: End-to-End System Commissioning & Evacuation Simulation
* **Scope**: Complete integrated system (Nodes $\to$ Gateway $\to$ CoreIOT $\to$ Backend $\to$ Frontend $\to$ Physical Actuators).
* **Implementation State**: `NOT_STARTED` (Scheduled for Milestone 6).
* **Integration Steps**:
  1. Stage physical fire/smoke stimulus (or calibrated test aerosol) at sensor node.
  2. Verify TinyML detects anomaly and triggers local alarm buzzer within latency target (TBD pending measurement plan).
  3. Verify ESP-NOW transmits event to Local Gateway; Local Gateway edge AI correlates spatial anomaly.
  4. Gateway activates water pump relay and forwards event to CoreIOT and Backend.
  5. React operations dashboard flashes critical alarm, sounds alert, and presents operator triage options.
  6. Operator clicks "Acknowledge" and "Emergency Reset"; verify commands route back to physical node.
* **Success Verification Gate**: Total incident detection-to-cloud notification latency target TBD pending measurement plan; actuator command execution verified (target fidelity TBD pending measurement plan); complete execution recorded in demo video.

---

## 3. Fail-Safe, Isolation, and Error Propagation Mechanisms

To ensure system reliability and life-safety integrity:

1. **Explicit Mock vs. Live Segregation**:
   * All Stage A simulated data packets carry `simulation.is_simulated: true` and a dedicated `scenario_id`.
   * Frontend provides a clear visual mode indicator. When live mode is active (`VITE_USE_MOCK_DATA=false`), read-only mock fallback must be made explicitly visible to operators to prevent false confidence.
2. **Strict Mutation Safety Invariant**:
   * As audited in `frontend/src/api/sensorApi.js`, failed live control mutations (`acknowledgeAlarm`, `resolveAlarm`, `dispatchControlCommand`) **never** mutate mock state to simulate success. Errors are thrown directly and rendered via `ErrorBanner.jsx`.
3. **Offline Autonomous Survivability**:
   * If WAN or CoreIOT connection drops, the Local IoT Gateway continues local telemetry aggregation, SQLite persistence, Edge AI evaluation, and local web UI operations (`local-gateway/ui/`).
   * Sensing nodes retain autonomous local alarm trip capabilities (piezo siren and relay trip) even if gateway communication is severed.
