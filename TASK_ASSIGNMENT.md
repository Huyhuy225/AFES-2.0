# AFES 2.0 Task Assignment and Team Governance

> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Faculty**: Computer Science and Engineering, HCMUT – VNU-HCM
> **Project Title**: AFES 2.0 – Advanced Fire Emergency System
> **Group Format**: Up to 3 Students per Group + Orca Multi-Agent Pairing

---

## 1. Team Organization and Role Definitions

In alignment with the HCMUT course requirements and professional distributed engineering standards, the project team divides responsibilities across three specialized functional domains:

```
+-----------------------------------------------------------------------------+
|                          AFES 2.0 PROJECT TEAM LEAD                         |
|                               (Võ Quang Huy)                                |
+-----------------------------------------------------------------------------+
          |                                   |                              |
          v                                   v                              v
+-------------------+               +-------------------+          +-------------------+
|   ROLE 1: LEAD    |               |   ROLE 2: LEAD    |          |   ROLE 3: LEAD    |
| EMBEDDED SYSTEMS  |               |  IOT GATEWAY &    |          | FULLSTACK PLATFORM|
|   & EDGE AI       |               |  COREIOT PLATFORM |          |    & DEVOPS       |
+-------------------+               +-------------------+          +-------------------+
| - ESP32-S3 Firmware|              | - Local PC/RPi GW |          | - Spring Boot BE  |
| - Sensors (T01-03)|              | - Edge AI (T09)   |          | - React Frontend  |
| - TinyML (T04-05) |              | - Gateway UI (T10)|          | - REST & WS APIs  |
| - ESP-NOW (T06)   |              | - CoreIOT (T11-13)|          | - CI/CD & Deploy  |
| - Device Web (T07)|              | - Sync Hub (T15)  |          | - Report Synthesis|
| - Device OTA (T14)|               |                   |          |                   |
+-------------------+               +-------------------+          +-------------------+
```

### 1.1. Role 1: Embedded Systems & Edge AI Lead
* **Primary Scope**: Tier 1 ESP32-S3 firmware, physical sensor drivers, TinyML on-device inference, local wireless protocols, and OTA client.
* **Assigned Course Elements**: **T01, T02, T03, T04, T05, T06, T07, T14**, and **N03**.
* **Deliverables**: FreeRTOS firmware in PlatformIO (`firmware/esp32-s3/`), TinyML model training and export pipeline (`tools/tinyml_pipeline/`), local webserver diagnostic interface, and OTA flashing harness.

### 1.2. Role 2: IoT Gateway & CoreIOT Platform Lead
* **Primary Scope**: Tier 2 Local IoT Gateway service, edge sensor fusion AI, gateway UI, and Tier 3 CoreIOT platform integration.
* **Assigned Course Elements**: **T08, T09, T10, T11, T12, T13, T15**, and **N07**.
* **Deliverables**: Multi-protocol Local Gateway software (`gateway/`), edge anomaly detection scripts, CoreIOT device profiles, RuleChain graphs (`coreiot/rulechains/`), and bidirectional synchronization connector.

### 1.3. Role 3: Fullstack Platform & DevOps Lead
* **Primary Scope**: Tier 4 Spring Boot enterprise backend, Tier 5 React/Vite dashboard, API contracts, database architecture, CI/CD pipelines, and course report compilation.
* **Assigned Course Elements**: System Integration, **N06 (Custom Dashboard)**, **N01 (LLM Assistant)**, Technical Contracts, Repository Governance, and Report Deliverables.
* **Deliverables**: Spring Boot REST/WebSocket application (`backend/`), React web application (`frontend/`), Docker orchestration, and final course documentation/report.

---

## 2. Comprehensive Task Assignment Matrix

| Work Item / Module | Target Technology | Assigned Role | Primary Worker / Agent | Reviewer | Status | Target Milestone | Deliverable Artifact |
|---|---|---|---|---|---|---|---|
| Repository Governance & CI Baseline | DevSecOps Baseline | Fullstack Lead | Human + Codex Agent | Team Lead | `IN_PROGRESS` (Issue #1) | M1 (Week 10) | `.github/`, `CONTRIBUTING.md`, CODEOWNERS |
| Course Matrix & Technical Contracts | System Architecture | Fullstack Lead | Human + Antigravity Agent | Team Lead | `IMPLEMENTED` (Issue #2) | M1 (Week 10) | `ARCHITECTURE.md`, `COURSE_REQUIREMENTS.md`, Schemas |
| CoreIOT Project Onboarding Plan | CoreIOT Platform | Gateway Lead | Human + Codex Agent | Embedded Lead | `IN_PROGRESS` (Issue #3) | M1 (Week 11) | `docs/COREIOT_ONBOARDING.md`, Credential Guide |
| Stage A Virtual Telemetry Simulator | Tooling & Sim | Fullstack Lead | Human + Assistant | Gateway Lead | `NOT_STARTED` | M2 (Week 11) | `tools/mock_simulator/` emitting AFES v2 JSON |
| Local IoT Gateway Core Engine | **T08** (1.0 pt) | Gateway Lead | Gateway Lead | Fullstack Lead | `NOT_STARTED` | M3 (Week 12) | `gateway/src/engine/` (Python/Node Aggregator) |
| Gateway Edge AI Fusion Model | **T09** (1.0 pt) | Gateway Lead | Gateway Lead | Embedded Lead | `NOT_STARTED` | M3 (Week 12) | `gateway/src/edge_ai/` (Multi-room Anomaly Model) |
| Local Gateway Operational UI | **T10** (1.0 pt) | Gateway Lead | Gateway Lead | Fullstack Lead | `NOT_STARTED` | M3 (Week 12) | `gateway/ui/` (Standalone Local Web Dashboard) |
| CoreIOT Dashboards & Templates | **T11** (1.0 pt) | Gateway Lead | Gateway Lead | Fullstack Lead | `NOT_STARTED` | M4 (Week 13) | `coreiot/dashboards/` (ThingsBoard Widgets JSON) |
| CoreIOT Automated RuleChains | **T12** (1.0 pt) | Gateway Lead | Gateway Lead | Embedded Lead | `NOT_STARTED` | M4 (Week 13) | `coreiot/rulechains/` (Fire Alarm Evaluation Graph) |
| CoreIOT Alert Notifications | **T13** (0.5 pt) | Gateway Lead | Gateway Lead | Fullstack Lead | `NOT_STARTED` | M4 (Week 13) | `coreiot/notifications/` (Email/Webhook Alarms) |
| CoreIOT Gateway Synchronization | **T15** (2.0 pts) | Gateway Lead | Gateway Lead | Fullstack Lead | `NOT_STARTED` | M4 (Week 14) | `gateway/src/coreiot_sync/` (MQTT Gateway Sync) |
| ESP32-S3 I2C Sensor Integration | **T01** (0.5 pt) | Embedded Lead | Embedded Lead | Gateway Lead | `NOT_STARTED` | M5 (Week 14) | `firmware/esp32-s3/src/sensors/i2c/` (DHT20 driver) |
| ESP32-S3 Modbus RS485 Interface | **T02** (1.0 pt) | Embedded Lead | Embedded Lead | Gateway Lead | `NOT_STARTED` | M5 (Week 14) | `firmware/esp32-s3/src/sensors/modbus/` (MAX485 RTU) |
| ESP32-S3 BLE Client Integration | **T03** (1.5 pts) | Embedded Lead | Embedded Lead | Gateway Lead | `NOT_STARTED` | M5 (Week 14) | `firmware/esp32-s3/src/sensors/ble/` (BLE GATT Central)|
| ESP32-S3 TinyML Fire Classifier | **T04** (1.0 pt) | Embedded Lead | Embedded Lead | Fullstack Lead | `NOT_STARTED` | M5 (Week 15) | `firmware/esp32-s3/src/tinyml/` (TFLite Micro Model) |
| TinyML Training & Export Tooling | **T05** (1.0 pt) | Embedded Lead | Embedded Lead | Gateway Lead | `NOT_STARTED` | M5 (Week 15) | `tools/tinyml_pipeline/` (Colab/Python Scripts) |
| Wireless Peer Comms via ESP-NOW | **T06** (1.5 pts) | Embedded Lead | Embedded Lead | Gateway Lead | `NOT_STARTED` | M5 (Week 15) | `firmware/esp32-s3/src/comms/esp_now/` (Mesh Frame) |
| Embedded On-Device Web Server | **T07** (1.0 pt) | Embedded Lead | Embedded Lead | Fullstack Lead | `NOT_STARTED` | M5 (Week 15) | `firmware/esp32-s3/src/webserver/` (HTTP Diagnostics) |
| Over-The-Air Firmware Updates | **T14** (2.0 pts) | Embedded Lead | Embedded Lead | Gateway Lead | `NOT_STARTED` | M5 (Week 15) | `firmware/esp32-s3/src/ota/` (CoreIOT OTA Client) |
| Fullstack Event Recording App | **N06** (1.0 pt bonus) | Fullstack Lead | Fullstack Lead | Team Lead | `IN_PROGRESS` | M4 (Week 14) | `frontend/src/` & `backend/src/` (Custom Web App) |
| Measurement, Lab Testing & Demo | Course Evaluation | All Leads | Entire Team | Team Lead | `NOT_STARTED` | M6 (Week 16) | Demo Video (5–10 min) & Lab Evidence Logs |
| Final Course Report Formulation | Course Evaluation | Fullstack Lead | Entire Team | Team Lead | `NOT_STARTED` | M6 (Week 16) | `[ClassCode]_[GroupCode]_IoTReport.pdf` |

---

## 3. Project Milestones and Schedule (Weeks 10–16)

```
Week 10 ----------------- Week 12 ----------------- Week 14 ----------------- Week 16
[ M1: Architecture & Gov ]
           [ M2: Stage A Simulation ]
                      [ M3: Local Gateway & Edge AI ]
                                 [ M4: CoreIOT & Fullstack App ]
                                            [ M5: Stage B Hardware Deploy ]
                                                       [ M6: Demo & Final Report ]
```

### 3.1. Milestone Breakdown
* **Milestone 1 (Weeks 10–11): Governance and Technical Contracts**
  * Establish GitHub repository hygiene, branch protection rules, and issue templates (Issue #1).
  * Formalize AFES 2.0 system architecture, telemetry schema, API specification, and traceability matrix (Issue #2).
  * Create secure CoreIOT tenant onboarding plan without committing secrets (Issue #3).
* **Milestone 2 (Weeks 11–12): Stage A Virtual Simulation Baseline**
  * Build synthetic telemetry generator running in Docker.
  * Validate end-to-end data pipeline from virtual nodes to CoreIOT sandbox and Spring Boot backend.
  * In-person proposal presentation to course lecturer.
* **Milestone 3 (Weeks 12–13): Local IoT Gateway & Edge AI Engine**
  * Implement Local Gateway on PC/Pi aggregating sensor streams (T08).
  * Deploy edge multi-sensor anomaly detection model (T09).
  * Build local emergency monitoring and control web UI on gateway (T10).
* **Milestone 4 (Weeks 13–14): CoreIOT Platform Integration & Fullstack Web App**
  * Configure CoreIOT device templates, dashboards, and remote RPC controls (T11).
  * Implement automated alert RuleChains (T12) and threshold notifications (T13).
  * Complete Local Gateway to CoreIOT bidirectional synchronization (T15).
  * Finalize React/Vite live dashboard with interactive floorplan (N06).
* **Milestone 5 (Weeks 14–15): Stage B Physical Hardware Commissioning**
  * Flash ESP32-S3 (YoloUNO) boards with FreeRTOS PlatformIO firmware.
  * Wire and test physical I2C (T01), Modbus RS485 (T02), and BLE (T03) sensor modules.
  * Train and deploy on-device TinyML fire inference model (T04, T05).
  * Verify ESP-NOW peer-to-peer transmission (T06), local webserver (T07), and CoreIOT OTA updates (T14).
* **Milestone 6 (Week 16): Verification, Demo Video, and Report Submission**
  * Conduct full-system fire simulation tests in the laboratory.
  * Capture latency measurements, power consumption, and error rates.
  * Record 5–10 minute demonstration video showcasing all claimed technology elements.
  * Compile and submit final PDF report following the HCMUT template on LMS.

---

## 4. Code Review and Governance Protocols

1. **Branching Strategy**:
   * Protected base branches: `main` (production-ready releases) and `develop` (integration baseline).
   * Feature branches follow the pattern: `<username>/<feature-topic>` (e.g., `Huyhuy225/docs-architecture-contracts`).
   * Direct pushes to `main` and `develop` are strictly prohibited.
2. **Pull Request Requirements**:
   * Exactly one logical PR per GitHub Issue.
   * Every PR description must include `Closes #<issue_number>`.
   * PRs must pass all automated CI checks (`git diff --check`, linting, unit tests) prior to review.
   * Minimum of one peer review approval required before squash-merging to `develop`.
3. **Secret Hygiene**:
   * Zero-tolerance policy for committing passwords, private keys, Wi-Fi credentials, or cloud access tokens.
   * Environment variables (`.env`) and secret managers must be used exclusively.
