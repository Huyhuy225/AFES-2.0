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
|                         Võ Quang Huy (@Huyhuy225)                           |
+-----------------------------------------------------------------------------+
          |                                   |                              |
          v                                   v                              v
+-------------------+               +-------------------+          +-------------------+
|   ROLE 1: LEAD    |               |   ROLE 2: LEAD    |          |   ROLE 3: LEAD    |
| ARCHITECTURE,     |               | FIRMWARE & LOCAL  |          | FRONTEND          |
| COREIOT & BACKEND |               |      GATEWAY      |          | ENGINEERING       |
|  (Võ Quang Huy)   |               |     (Khánh)       |          |  (Ý @gutjmosnin)  |
+-------------------+               +-------------------+          +-------------------+
| - System Architect|               | - ESP32-S3 Firmware|         | - React Dashboard |
| - Technical Specs |               | - Sensors (T01-03)|          | - Floorplan UX    |
| - CoreIOT (T11-13)|               | - TinyML (T04-05) |          | - Custom UI (N06) |
| - Backend Spring  |               | - ESP-NOW (T06)   |          | - LLM UI (N01)    |
| - REST & WS APIs  |               | - Web Server (T07)|          | - Telemetry Views |
| - Gateway Sync Hub|               | - Local GW (T08)  |          | - Control Console |
| - CI/CD & Deploy  |               | - Edge AI (T09)   |          | - Alarm Triage UI |
| - DevSecOps & QA  |               | - Gateway UI (T10)|          |                   |
| - Report Lead     |               | - OTA Client (T14)|          |                   |
+-------------------+               +-------------------+          +-------------------+
```

### 1.1. Role 1: Architecture, CoreIOT, Backend & Integration Lead – Võ Quang Huy (@Huyhuy225)
* **Primary Scope**: Overall system architecture, technical contracts, CoreIOT platform integration (device profiles, rulechains, threshold alarms, gateway synchronization hub), Spring Boot 3 enterprise application backend, REST and WebSocket APIs, database modeling, DevSecOps baseline, and final report synthesis.
* **Assigned Course Elements**: System Architecture, **T11, T12, T13, T15** (CoreIOT platform hub side), Issue #1, Issue #2, Issue #3, and **N07** (optional local ThingsBoard bonus evaluation).
* **Deliverables**: Technical contracts (`ARCHITECTURE.md`, `COURSE_REQUIREMENTS.md`, `docs/TELEMETRY_SCHEMA.md`, `docs/API_SPECIFICATION.md`), CoreIOT configuration assets (`coreiot/rulechains/`, `coreiot/notifications/`), Spring Boot service (`backend/`), Docker orchestration, and system integration.

### 1.2. Role 2: Firmware & Local Gateway Lead – Khánh (@pending-khanh-user)
* **Primary Scope**: Tier 1 ESP32-S3 microcontroller firmware, hardware sensor integration (I2C, Modbus RS485, BLE), on-device TinyML fire inference, ESP-NOW wireless communication, on-device diagnostic webserver, remote OTA client, and Tier 2 Local IoT Gateway software implementation (`local-gateway/`) including edge aggregation, edge AI multi-room fusion, and local gateway UI.
* **Assigned Course Elements**: **T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T14**, and **N03**.
* **Deliverables**: PlatformIO FreeRTOS firmware (`firmware/esp32-s3/`), TinyML pipeline (`tools/tinyml_pipeline/`), Local IoT Gateway service (`local-gateway/src/`), edge AI fusion model (`local-gateway/src/edge_ai/`), and local gateway operations UI (`local-gateway/ui/`).

### 1.3. Role 3: Frontend Engineering & UI/UX Lead – Ý (@gutjmosnin)
* **Primary Scope**: Tier 5 User Presentation Layer, React 18 / Vite real-time operations dashboard, facility floorplan status mapping, interactive sensor analytics charts, alarm triage interface, manual control actions panel, custom event recording web application, and operator assistant interface.
* **Assigned Course Elements**: **N06 (Custom Dashboard)**, **N01 (LLM Assistant Interface)**, and frontend integration of all telemetry/control contracts.
* **Deliverables**: React web application (`frontend/src/`), real-time STOMP/WebSocket telemetry consumers, visual alarm triage components, and responsive mobile/desktop dashboard views.

---

## 2. Comprehensive Task Assignment Matrix

| Work Item / Module | Target Technology | Assigned Role | Primary Worker | Reviewer | Status | Target Milestone | Deliverable Artifact |
|---|---|---|---|---|---|---|---|
| Repository Governance & CI Baseline | DevSecOps Baseline | Arch & Backend Lead (Huy) | Huy | Khánh | `IN_PROGRESS` (Issue #1) | M1 (Timing TBD) | `.github/`, `CONTRIBUTING.md`, CODEOWNERS |
| Course Matrix & Technical Contracts | System Architecture | Arch & Backend Lead (Huy) | Huy | Ý | `IMPLEMENTED` (Issue #2) | M1 (Timing TBD) | `ARCHITECTURE.md`, `COURSE_REQUIREMENTS.md`, Schemas |
| CoreIOT Project Onboarding Plan | CoreIOT Platform | Arch & Backend Lead (Huy) | Huy | Khánh | `IN_PROGRESS` (Issue #3) | M1 (Timing TBD) | `docs/COREIOT_ONBOARDING.md`, Credential Guide |
| Stage A Virtual Telemetry Simulator | Tooling & Sim | Arch & Backend Lead (Huy) | Huy | Khánh | `NOT_STARTED` | M2 (Timing TBD) | `tools/mock_simulator/` emitting AFES v2 JSON |
| Local IoT Gateway Core Engine | **T08** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M3 (Timing TBD) | `local-gateway/src/engine/` (Python/Node Aggregator) |
| Gateway Edge AI Fusion Model | **T09** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M3 (Timing TBD) | `local-gateway/src/edge_ai/` (Multi-room Anomaly Model) |
| Local Gateway Operational UI | **T10** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Ý | `NOT_STARTED` | M3 (Timing TBD) | `local-gateway/ui/` (Standalone Local Web Dashboard) |
| CoreIOT Dashboards & Templates | **T11** (1.0 pt) | Arch & Backend Lead (Huy) | Huy | Ý | `NOT_STARTED` | M4 (Timing TBD) | `coreiot/dashboards/` (CoreIOT Dashboard Widgets JSON) |
| CoreIOT Automated RuleChains | **T12** (1.0 pt) | Arch & Backend Lead (Huy) | Huy | Khánh | `NOT_STARTED` | M4 (Timing TBD) | `coreiot/rulechains/` (Fire Alarm Evaluation Graph) |
| CoreIOT Alert Notifications | **T13** (0.5 pt) | Arch & Backend Lead (Huy) | Huy | Ý | `NOT_STARTED` | M4 (Timing TBD) | `coreiot/notifications/` (Email/Webhook Alarms) |
| CoreIOT Gateway Synchronization | **T15** (2.0 pts) | Arch & Backend Lead (Huy) | Huy & Khánh | Team | `NOT_STARTED` | M4 (Timing TBD) | `local-gateway/src/coreiot_sync/` (MQTT Gateway Sync) |
| ESP32-S3 I2C Sensor Integration | **T01** (0.5 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/sensors/i2c/` (DHT20 driver) |
| ESP32-S3 Modbus RS485 Interface | **T02** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/sensors/modbus/` (MAX485 RTU) |
| ESP32-S3 BLE Client Integration | **T03** (1.5 pts) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/sensors/ble/` (BLE GATT Central)|
| ESP32-S3 TinyML Fire Classifier | **T04** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/tinyml/` (TFLite Micro Model) |
| TinyML Training & Export Tooling | **T05** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `tools/tinyml_pipeline/` (Colab/Python Scripts) |
| Wireless Peer Comms via ESP-NOW | **T06** (1.5 pts) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/comms/esp_now/` (Mesh Frame) |
| Embedded On-Device Web Server | **T07** (1.0 pt) | Firmware & Gateway Lead (Khánh) | Khánh | Ý | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/webserver/` (HTTP Diagnostics) |
| Over-The-Air Firmware Updates | **T14** (2.0 pts) | Firmware & Gateway Lead (Khánh) | Khánh | Huy | `NOT_STARTED` | M5 (Timing TBD) | `firmware/esp32-s3/src/ota/` (CoreIOT OTA Client) |
| Fullstack Event Recording App | **N06** (1.0 pt bonus) | Frontend Lead (Ý @gutjmosnin) | Ý | Huy | `DOCUMENTED` | M4 (Timing TBD) | `frontend/src/` (Custom Web Dashboard) |
| Local ThingsBoard Instance (Optional) | **N07** (1.0 pt bonus) | Arch & Backend Lead (Huy) | Huy | Khánh | `NOT_STARTED` | M4 (Timing TBD) | `docker-compose.thingsboard.yml` (Explicitly optional bonus item; not an assumed CoreIOT implementation) |
| Measurement, Lab Testing & Demo | Course Evaluation | All Leads | Entire Team | Huy | `NOT_STARTED` | M6 (Timing TBD) | Demo Video (5–10 min) & Lab Evidence Logs |
| Final Course Report Formulation | Course Evaluation | Arch & Backend Lead (Huy) | Entire Team | Huy | `NOT_STARTED` | M6 (Timing TBD) | `[ClassCode]_[GroupCode]_IoTReport.pdf` |

---

## 3. Project Milestones and Phased Roadmap (Timing TBD)

The project executes through six distinct delivery milestones. Exact calendar dates and completion deadlines are marked **TBD** pending course lecturer announcements and scheduling:

```
[ Milestone 1 ] ----> [ Milestone 2 ] ----> [ Milestone 3 ] ----> [ Milestone 4 ] ----> [ Milestone 5 ] ----> [ Milestone 6 ]
  Architecture           Stage A Sim          Local Gateway        CoreIOT Platform       Stage B Physical       Verification,
  & Governance           & Proposal           & Edge AI            & Fullstack UI         Commissioning          Demo & Report
```

### 3.1. Milestone Descriptions
* **Milestone 1 (Timing TBD): Governance and Technical Contracts**
  * Establish GitHub repository hygiene, branch protection rules, and issue templates (Issue #1).
  * Formalize AFES 2.0 system architecture, telemetry schema, API specification, and traceability matrix (Issue #2).
  * Create secure CoreIOT tenant onboarding plan without committing secrets (Issue #3).
* **Milestone 2 (Timing TBD): Stage A Virtual Simulation Baseline & Proposal Presentation**
  * Build synthetic telemetry generator running in Docker.
  * Validate end-to-end data pipeline from virtual nodes through Local Gateway to CoreIOT sandbox and Spring Boot backend.
  * Prepare proposal presentation for course lecturer.
* **Milestone 3 (Timing TBD): Local IoT Gateway & Edge AI Engine**
  * Implement Local Gateway on PC/Pi aggregating sensor streams (`local-gateway/src/`, T08).
  * Deploy edge multi-sensor anomaly detection model (`local-gateway/src/edge_ai/`, T09).
  * Build local emergency monitoring and control web UI on gateway (`local-gateway/ui/`, T10).
* **Milestone 4 (Timing TBD): CoreIOT Platform Integration & Fullstack Web App**
  * Configure CoreIOT device templates, dashboards, and remote RPC controls (T11; onboarding deferred to Issue #3).
  * Implement automated alert RuleChains (T12) and threshold notifications (T13).
  * Complete Local Gateway to CoreIOT bidirectional synchronization (T15).
  * Finalize React/Vite live dashboard with interactive floorplan (N06, led by Ý @gutjmosnin).
* **Milestone 5 (Timing TBD): Stage B Physical Hardware Commissioning**
  * Flash ESP32-S3 (YoloUNO) boards with FreeRTOS PlatformIO firmware.
  * Wire and test physical I2C (T01), Modbus RS485 (T02), and BLE (T03) sensor modules.
  * Train and deploy on-device TinyML fire inference model (T04, T05).
  * Verify ESP-NOW peer-to-peer transmission (T06), local webserver (T07), and CoreIOT OTA updates (T14).
* **Milestone 6 (Timing TBD): Verification, Demo Video, and Report Submission**
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
