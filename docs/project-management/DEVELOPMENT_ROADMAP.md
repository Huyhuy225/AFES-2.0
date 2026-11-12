# AFES 2.0 – Phased Development Roadmap and Stage Boundaries

> **Document Version**: 2.0.0
> **Status**: Approved Project Management Baseline
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Course**: Internet of Things (IoT) – Semester 261 (HCMUT)
> **Documentation Location**: `docs/project-management/DEVELOPMENT_ROADMAP.md`

---

## 1. Roadmap Architecture and Dual-Stage Boundary

The AFES 2.0 development lifecycle enforces a strict separation between **Stage A (Virtual Simulation & Contract Verification)** and **Stage B (Physical Hardware Commissioning)**. This dual-stage methodology ensures that all cloud, backend, gateway, and frontend integration contracts are validated deterministically before physical electronics and sensors are powered in the laboratory.

```
====================================================================================================
STAGE A: VIRTUAL SIMULATION & CONTRACT VERIFICATION (Zero Hardware Required)
====================================================================================================
[ Milestone 1: Governance & Specs ]  -->  [ Milestone 2: Sim & Gateway ]  -->  [ Milestone 3 & 4: CoreIOT & Fullstack ]
* Architecture & Contracts (DOCUMENTED)   * ESP32-S3 Mock Sim (NOT_STARTED)    * CoreIOT Onboarding (BLOCKED)
* CI & DevSecOps (TESTED/Hygiene)         * Local Gateway Skeleton (NOT_STARTED)* Spring Boot Backend (NOT_STARTED)
* Frontend Baseline (TESTED/Stage A)      * MQTT Schema Validation             * Live REST/STOMP Integration
====================================================================================================
STAGE B: PHYSICAL HARDWARE COMMISSIONING & LAB EVALUATION (Physical Hardware Required)
====================================================================================================
                                      -->  [ Milestone 5: Hardware Commissioning ] --> [ Milestone 6: Demo & Report ]
                                           * ESP32-S3 YoloUNO Flash & Sensors       * Lab Fire Evacuation Test
                                           * I2C (T01), Modbus (T02), BLE (T03)     * Latency & Metrics Logs
                                           * On-device TinyML (T04), ESP-NOW (T06)  * 5-10 min Video & PDF Report
====================================================================================================
```

### 1.1. Explicit Stage A vs. Stage B Differentiation Matrix

| Dimension | Stage A: Virtual Simulation & Verification | Stage B: Physical Hardware Commissioning |
|---|---|---|
| **Primary Objective** | Validate schemas, APIs, business logic, UI, and fail-safes without hardware. | Wire, flash, calibrate, and verify physical sensors, microcontrollers, and actuators. |
| **Execution Environment** | Developer PCs, Docker containers, Node.js runtime, Vitest/pytest runners. | Physical electronics lab, breadboards, ESP32-S3 (YoloUNO), sensors, relays. |
| **Data Source** | Synthetic JSON generators emitting payloads flagged with `simulation.is_simulated = true`. | Real physical ADC pins, I2C bus (DHT20), UART RS485 (MAX485), and BLE GATT radio. |
| **Transport Medium** | Localhost loopback, virtual MQTT brokers (Mosquitto), WebSocket streams. | Physical Wi-Fi 802.11 b/g/n, ESP-NOW 2.4GHz RF, physical RS485 twisted pair wire. |
| **Actuator Action** | Simulated state flag toggles, virtual console logs, in-memory state store updates. | Physical 5V relay energization, solenoid water valve activation, piezoelectric siren sound. |
| **Course Grading Boundary** | Satisfies contract verification, automated tests, and simulation deliverables. | Strictly required for physical technology element claims (**T01–T07, T14**). |

---

## 2. Phased Milestone Breakdown

### Milestone 1: Repository Governance, Technical Contracts & Baseline Stabilization
* **Stage**: Stage A
* **Overall State**: `DOCUMENTED` / `IN_PROGRESS`
* **Lead**: Võ Quang Huy ([`@Huyhuy225`](https://github.com/Huyhuy225))
* **Target Objectives**:
  1. Establish repository governance, issue/PR templates, and CI hygiene baseline. *(Completed in PR #5, Commit `b70d366`, `DOCUMENTED`)*
  2. Formalize system architecture, API specifications, and telemetry schemas. *(Completed in PR #4, Commit `ec28aef`, `DOCUMENTED`)*
  3. Publish Stage A Frontend Monitoring Dashboard baseline with automated tests. *(Completed in PR #9, Commit `bb5bba7`, `TESTED`)*
  4. Perform evidence-based repository audit and establish project management stabilization suite under `docs/project-management/`. *(Current Task, `IN_PROGRESS`)*
* **Deliverables**: `ARCHITECTURE.md`, `COURSE_REQUIREMENTS.md`, `docs/API_SPECIFICATION.md`, `docs/TELEMETRY_SCHEMA.md`, `frontend/`, `docs/project-management/*`.
* **Exit Criteria**: All 7 project management documents approved; `git diff --check` passes; single documentation-only PR merged to `develop` linked `Closes #10`.

---

### Milestone 2: Stage A Virtual Simulation & Local Gateway Skeleton
* **Stage**: Stage A (Virtual Simulation)
* **Overall State**: `IN_PROGRESS` (Tracked in open Issues #6 and #7)
* **Lead**: Hoàng Khánh ([`@tranhoangkhanh-hkt`](https://github.com/tranhoangkhanh-hkt), assignment pending acceptance)
* **Target Objectives**:
  1. **ESP32-S3 Telemetry Simulator (`tools/mock_simulator/`)** (Issue #6):
     * Pure software generator emitting AFES 2.0 telemetry JSON payloads matching `docs/TELEMETRY_SCHEMA.md`.
     * Strict flag: `simulation.is_simulated = true`.
     * Automated MQTT contract tests validating topic routing and payload serialization against local Mosquitto broker.
  2. **Local IoT Gateway Skeleton (`local-gateway/src/engine/`)** (Issue #7, Course T08 Stage A):
     * Telemetry ingestion engine accepting MQTT feeds from multiple virtual nodes.
     * Offline resilient caching via local SQLite database.
     * Safe bidirectional command routing (`cmd/req` and `cmd/res`).
* **Deliverables**: `tools/mock_simulator/`, `local-gateway/src/engine/`, `reports/evidence/T08/STAGE_A_GATEWAY_EVIDENCE.md`.
* **Exit Criteria**: 100% automated contract pass rate; simulator and gateway run cleanly in local Docker environment without hardware dependencies.

---

### Milestone 3: Local Gateway Edge Intelligence & Standalone UI
* **Stage**: Stage A (Virtual Simulation)
* **Overall State**: `NOT_STARTED`
* **Lead**: Hoàng Khánh ([`@tranhoangkhanh-hkt`](https://github.com/tranhoangkhanh-hkt), assignment pending acceptance)
* **Target Objectives**:
  1. **Gateway Edge AI Fusion Model (Course T09)**:
     * Implement spatial multi-room anomaly detection script in Python/Node.js.
     * Evaluate thermal rise and smoke diffusion patterns across adjacent virtual zones.
  2. **Standalone Gateway Operations UI (Course T10)**:
     * Implement lightweight local web dashboard (`local-gateway/ui/`) served directly by the gateway.
     * Ensure 100% monitoring and manual override functionality during total WAN / Internet outage.
* **Deliverables**: `local-gateway/src/edge_ai/`, `local-gateway/ui/`, `reports/evidence/T09/`, `reports/evidence/T10/`.
* **Exit Criteria**: Local gateway web UI operates independently with zero external cloud dependencies.

---

### Milestone 4: CoreIOT Cloud Integration & Fullstack Application
* **Stage**: Stage A (Virtual Simulation / Cloud Sandbox)
* **Overall State**: `NOT_STARTED` (CoreIOT Onboarding `BLOCKED` in Issue #3)
* **Leads**: Võ Quang Huy ([`@Huyhuy225`](https://github.com/Huyhuy225)) & Ý ([`@gutjmosnin`](https://github.com/gutjmosnin), pending acceptance)
* **Target Objectives**:
  1. **CoreIOT Tenant Provisioning & Onboarding (Issue #3)**:
     * Unblock CoreIOT access; document safe credential management.
  2. **CoreIOT Platform Dashboards & Remote Control (Course T11)**:
     * Configure CoreIOT device profiles, visual widgets, and RPC switches.
  3. **CoreIOT RuleChains & Alerts (Course T12, T13)**:
     * Deploy automated fire evaluation rulechain and notification triggers (email/webhook).
  4. **Gateway-to-CoreIOT Synchronization (Course T15)**:
     * Bidirectional edge-to-cloud synchronization protocol.
  5. **Spring Boot 3 Enterprise Backend (`backend/`)**:
     * Implement `/api/v2/*` REST endpoints, JWT authentication, MySQL persistence, and STOMP WebSocket streams.
  6. **Frontend Fullstack Completion (Course N06)**:
     * Connect React dashboard to Spring Boot live endpoints; implement persistent event logging and 2D floorplan canvas.
* **Deliverables**: `coreiot/`, `backend/`, `frontend/src/components/FloorPlan/`, `reports/evidence/N06/`.
* **Exit Criteria**: End-to-end telemetry flow from simulator $\to$ gateway $\to$ CoreIOT $\to$ backend $\to$ browser dashboard.

---

### Milestone 5: Stage B Physical Hardware Commissioning
* **Stage**: **Stage B (Physical Hardware Integration)**
* **Overall State**: `NOT_STARTED`
* **Lead**: Hoàng Khánh ([`@tranhoangkhanh-hkt`](https://github.com/tranhoangkhanh-hkt), assignment pending acceptance)
* **Target Objectives**:
  1. **ESP32-S3 Physical Firmware Baseline**: PlatformIO / FreeRTOS firmware flashed onto physical YoloUNO boards.
  2. **I2C Sensor Integration (Course T01)**: DHT20/SHT30 sensor wired to I2C bus; periodic readings logged to serial and MQTT.
  3. **Modbus RS485 Interface (Course T02)**: MAX485 transceiver querying industrial sensor with CRC error checking.
  4. **BLE Sensor Client (Course T03)**: ESP32-S3 BLE central scanning and receiving GATT environmental notifications.
  5. **On-Device TinyML Classifier & Training (Course T04, T05)**: Quantized TFLite Micro binary flashed to ESP32-S3; real-time smoke/fire inference with latency profiling.
  6. **ESP-NOW Peer-to-Peer Communication (Course T06)**: Wireless frame transmission between edge node and gateway receiver.
  7. **Embedded Web Server (Course T07)**: ESP32-S3 on-device diagnostic HTTP server for direct local control.
  8. **CoreIOT OTA Remote Updates (Course T14)**: Firmware update package deployed via CoreIOT OTA service.
* **Deliverables**: `firmware/esp32-s3/`, `reports/evidence/T01/` through `reports/evidence/T07/`, `reports/evidence/T14/`.
* **Exit Criteria**: Hardware demonstrator operates in physical laboratory; oscilloscope/serial logs confirm sensor and radio operation.

---

### Milestone 6: Full-System Verification, Demo Video & Final Report
* **Stage**: Stage B Verification
* **Overall State**: `NOT_STARTED`
* **Lead**: Võ Quang Huy ([`@Huyhuy225`](https://github.com/Huyhuy225)) with entire team
* **Target Objectives**:
  1. Full-system live fire simulation in lab with automated actuator triggers (buzzer, water pump).
  2. Metric collection: sub-500ms edge detection, sub-2s cloud synchronization, 100% offline buffer replay.
  3. Production of high-definition 5–10 minute demonstration video showcasing all claimed technology elements.
  4. Formulation and submission of final PDF report adhering to HCMUT CSE official guidelines.
* **Deliverables**: `reports/final_report.pdf`, demonstration video URL, archived lab datasets.
* **Exit Criteria**: Final project package submitted to course portal before academic deadline.
