# AFES 2.0 – Operational Task Assignment and Ownership Matrix

> **Baseline Version**: 2.0.0
> **Status**: DRAFT — pending Technical Lead approval
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027), HCMUT
> **Faculty**: Computer Science and Engineering, HCMUT – VNU-HCM
> **Documentation Location**: `docs/project-management/TASK_ASSIGNMENT.md`

---

## 1. Team Organization and Verified GitHub Mapping

Responsibilities in AFES 2.0 are partitioned strictly across three specialized roles to prevent scope overlap, race conditions in worktrees, and merge conflicts.

```
+-----------------------------------------------------------------------------+
|                          AFES 2.0 TECHNICAL LEAD                            |
|                         Võ Quang Huy (@Huyhuy225)                           |
+-----------------------------------------------------------------------------+
          |                                   |                              |
          v                                   v                              v
+-------------------+               +-------------------+          +-------------------+
|   ROLE 1: LEAD    |               |   ROLE 2: LEAD    |          |   ROLE 3: LEAD    |
| ARCHITECTURE,     |               | FIRMWARE & LOCAL  |          | FRONTEND          |
| COREIOT & BACKEND |               |      GATEWAY      |          | ENGINEERING       |
|  (Võ Quang Huy)   |               |     (Khánh)       |          |      (Ý)          |
+-------------------+               +-------------------+          +-------------------+
| GitHub:           |               | GitHub:           |          | GitHub:           |
| @Huyhuy225        |               | @tranhoangkhanh-  |          | @gutjmosnin       |
| Status: Active    |               |  hkt              |          | Status: Invitation|
|                   |               | Status: Invitation|          |  Pending (#34309  |
|                   |               |  Pending (#34311  |          |   3548)           |
|                   |               |   6245)           |          |                   |
+-------------------+               +-------------------+          +-------------------+
```

### 1.1. Role 1: Architecture, CoreIOT, Backend & DevSecOps Lead
* **Primary Engineer**: Võ Quang Huy ([`@Huyhuy225`](https://github.com/Huyhuy225))
* **GitHub Membership**: Active Repository Owner / Admin
* **Functional Scope**: Overall system architecture, technical contract definition, CoreIOT platform provisioning, rulechain definition, Spring Boot 3 enterprise application server, REST v2 and WebSocket APIs, database modeling, and DevSecOps / CI coordination.
* **Relevant Course Elements**: Architecture, **T11, T12, T13, T15** (CoreIOT cloud side), **N07** (optional local ThingsBoard bonus), Issues [#1](https://github.com/Huyhuy225/AFES-2.0/issues/1), [#2](https://github.com/Huyhuy225/AFES-2.0/issues/2), [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3), [#10](https://github.com/Huyhuy225/AFES-2.0/issues/10).

### 1.2. Role 2: Firmware & Local IoT Gateway Lead
* **Primary Engineer**: Hoàng Khánh ([`@tranhoangkhanh-hkt`](https://github.com/tranhoangkhanh-hkt))
* **GitHub Membership**: **Pending Invitation Acceptance** (Invitation ID `343116245`, Write access)
* **Functional Scope**: Tier 1 ESP32-S3 microcontroller firmware (PlatformIO, FreeRTOS), physical and mock sensor drivers (I2C DHT20, Modbus RS485, BLE), on-device TinyML fire inference, ESP-NOW wireless communication, on-device diagnostic web server, remote OTA client, and Tier 2 Local IoT Gateway software implementation (`local-gateway/`) including edge aggregation, multi-room spatial AI fusion, and local gateway web UI.
* **Relevant Course Elements**: **T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T14**, **N03**, Issues [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6), [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) (assignable to Khánh upon invitation acceptance; does not own Issue #3).

### 1.3. Role 3: Frontend Engineering & UI/UX Lead
* **Primary Engineer**: Ý ([`@gutjmosnin`](https://github.com/gutjmosnin))
* **GitHub Membership**: **Pending Invitation Acceptance** (Invitation ID `343093548`, Write access)
* **Functional Scope**: Tier 5 User Presentation Layer, React 18 / Vite real-time operations dashboard, facility floorplan status mapping, interactive sensor analytics charts, alarm triage interface, manual control console, custom event recording web application, and operator assistant interface.
* **Relevant Course Elements**: **N06** (Custom Dashboard, 1.0 pt bonus), **N01** (LLM Assistant Interface, 1.0 pt bonus), Issues [#8](https://github.com/Huyhuy225/AFES-2.0/issues/8) (merged baseline), remaining M4 fullstack integration (assignable to Ý upon invitation acceptance; does not own Issue #3).

---

## 2. Implementation-State Vocabulary Standard

Every task and deliverable in this project management suite uses strictly one of the six standard status values:
* `IMPLEMENTED`: Functional code written, committed, and integrated into the repository.
* `TESTED`: Code or module verified through executed, reproducible automated or laboratory test suites.
* `DOCUMENTED`: Specifications, architectural contracts, interface schemas, and procedures formalized in markdown, without constituting running software. Documentation-only components are marked strictly as `DOCUMENTED` and never as `IMPLEMENTED`.
* `IN_PROGRESS`: Active development underway with partial code or baseline artifacts present in the repository.
* `BLOCKED`: Development prevented by external dependencies, missing credentials, hardware availability, or administrative access.
* `NOT_STARTED`: Work item defined and scheduled, but no implementation commits exist in the repository.

---

## 3. Granular, Non-Overlapping Task Assignment Matrix

| Task ID | Work Item Name | Assigned Owner (GitHub Username) | Priority | Status | Dependency | Acceptance Criteria | Primary Deliverable Artifact |
|---|---|---|---|---|---|---|---|
| **TASK-PM-01** | Stabilization Audit & PM Baseline | Võ Quang Huy (`@Huyhuy225`) | P0 (Blocker) | `IN_PROGRESS` | None | Publish 7 evidence-based PM files under `docs/project-management/`; clean `git diff --check`. | `docs/project-management/*` (PR linked `Closes #10`) |
| **TASK-PM-02** | Issue Tracking & Project Board Reconciliation | Võ Quang Huy (`@Huyhuy225`) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-PM-01 | Reconcile GitHub Issues #1 and #2 metadata; track milestones without altering closed code. | GitHub Issue tracking documentation (Planned deliverable) |
| **TASK-FE-01** | Stage A Frontend Monitoring Baseline | Ý (`@gutjmosnin`, pending acceptance) | P1 (High) | `TESTED` | PR #4, PR #5 | React 18 / Vite dashboard shell, zone cards, alarm triage, control console, 30 passing Vitest tests. | `frontend/` (Merged in PR #9, Commit `bb5bba7`) |
| **TASK-FE-02** | Frontend CI Automation Job | Võ Quang Huy (`@Huyhuy225`) | P1 (High) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-FE-01 | Add Node.js 22, `npm ci`, `npm test`, and `npm run lint` steps to `.github/workflows/ci.yml`. | `.github/workflows/ci.yml` (Planned deliverable update) |
| **TASK-FE-03** | Visual Indicator for Degraded Mock Fallback | Ý (`@gutjmosnin`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-FE-01 | Render visible persistent alert banner when read-only API falls back to mock store. | `frontend/src/components/ErrorBanner.jsx` (Planned update) |
| **TASK-FE-04** | Persistent Event History & Interactive 2D Floorplan | Ý (`@gutjmosnin`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-BE-02 | Complete full N06 scope: SVG/Canvas floorplan, incident correlation, backend event query integration. | `frontend/src/components/FloorPlan/` (Planned deliverable path) |
| **TASK-FE-05** | Natural Language Fire Assistant UI (N01) | Ý (`@gutjmosnin`, pending acceptance) | P3 (Low) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-FE-04 | Conversational query box for safety protocols and sensor incident diagnosis. | `frontend/src/components/Assistant/` (Planned deliverable path) |
| **TASK-SIM-01** | Stage A ESP32-S3 Telemetry Simulator & Contract Tests | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P1 (High) | `NOT_STARTED` | Issue #2 | Hardware-free Python/Node simulator publishing valid AFES v2 JSON; automated MQTT contract tests. | `tools/mock_simulator/` (Open Issue #6; planned deliverable path) |
| **TASK-GW-01** | Local Gateway Aggregation & Command Skeleton | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P1 (High) | `NOT_STARTED` | TASK-SIM-01 | Ingest simulated telemetry, normalize schema, buffer offline records in SQLite, route commands. | `local-gateway/src/engine/` (Open Issue #7; planned deliverable path) |
| **TASK-GW-02** | Local Gateway Edge AI Multi-Room Fusion (T09) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-GW-01 | Train and embed spatial fire anomaly detection model across multi-zone inputs. | `local-gateway/src/edge_ai/` (Planned deliverable path) |
| **TASK-GW-03** | Local Gateway Standalone Operational UI (T10) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-GW-01 | Lightweight local web dashboard functional during total cloud WAN outage. | `local-gateway/ui/` (Planned deliverable path) |
| **TASK-GW-04** | Local Gateway to CoreIOT Sync Protocol (T15) | Huy & Khánh (Joint) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-GW-01, TASK-IOT-01 | Synchronize edge buffer to CoreIOT Gateway API; handle reconnect and replay. | `local-gateway/src/coreiot_sync/` (Planned deliverable path) |
| **TASK-IOT-01** | Secure CoreIOT Project Onboarding Plan | Võ Quang Huy (`@Huyhuy225`) | P1 (High) | `BLOCKED` | Issue #2 | Document tenant credentials procedure, device profiles, access tokens without committing secrets. | `docs/COREIOT_ONBOARDING.md` (Open Issue #3; planned deliverable) |
| **TASK-IOT-02** | CoreIOT Dashboards & Remote Control (T11) | Võ Quang Huy (`@Huyhuy225`) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-IOT-01 | Design CoreIOT dashboard template with multi-node telemetry widgets and RPC switches. | `coreiot/dashboards/` (Planned deliverable path) |
| **TASK-IOT-03** | CoreIOT Automated RuleChains (T12) | Võ Quang Huy (`@Huyhuy225`) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-IOT-01 | Export RuleChain graph triggering autonomous water pump RPC on temperature/smoke spike. | `coreiot/rulechains/` (Planned deliverable path) |
| **TASK-IOT-04** | CoreIOT Alert Notification Rules (T13) | Võ Quang Huy (`@Huyhuy225`) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-IOT-01 | Configure email/webhook notifications for critical threshold breaches. | `coreiot/notifications/` (Planned deliverable path) |
| **TASK-BE-01** | Spring Boot 3 Backend Foundation & JPA Entities | Võ Quang Huy (`@Huyhuy225`) | P1 (High) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Issue #2 | Initialize Java 21 / Spring Boot 3 skeleton, MySQL JPA entities, Flyway migrations, Dockerfile. | `backend/` (Planned deliverable path) |
| **TASK-BE-02** | Spring Boot REST v2 Controllers & STOMP WebSocket | Võ Quang Huy (`@Huyhuy225`) | P1 (High) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-BE-01 | Implement `/api/v2/*` endpoints, JWT security filter, STOMP `/topic/telemetry` and `/topic/alarms`. | `backend/src/main/java/` (Planned deliverable path) |
| **TASK-FW-01** | ESP32-S3 I2C Sensor Integration (T01) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | Wire physical DHT20/SHT30 on I2C bus; periodic telemetry reading over serial/MQTT. | `firmware/esp32-s3/src/sensors/i2c/` (Planned deliverable path) |
| **TASK-FW-02** | ESP32-S3 Modbus RS485 Interface (T02) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | Connect MAX485 transceiver; query industrial RS485 sensor; CRC verification. | `firmware/esp32-s3/src/sensors/modbus/` (Planned deliverable path) |
| **TASK-FW-03** | ESP32-S3 BLE Central Client (T03) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | Scan and pair with peripheral BLE sensor beacon; receive environmental GATT notifications. | `firmware/esp32-s3/src/sensors/ble/` (Planned deliverable path) |
| **TASK-FW-04** | On-Device TinyML Classifier & Tooling (T04/T05) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | Python data collection/training pipeline; export quantized TFLite Micro model for ESP32-S3. | `firmware/esp32-s3/src/tinyml/`, `tools/` (Planned deliverable paths) |
| **TASK-FW-05** | ESP-NOW Wireless Mesh Communication (T06) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | Direct peer-to-peer transmission of emergency frames between sensing nodes and gateway. | `firmware/esp32-s3/src/comms/esp_now/` (Planned deliverable path) |
| **TASK-FW-06** | Embedded Diagnostic Web Server (T07) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | SoftAP/LAN embedded HTTP server for local browser sensor inspection and manual relay control. | `firmware/esp32-s3/src/webserver/` (Planned deliverable path) |
| **TASK-FW-07** | Over-The-Air (OTA) Remote Update Client (T14) | Hoàng Khánh (`@tranhoangkhanh-hkt`, pending acceptance) | P2 (Medium) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Lab Stage B | CoreIOT / HTTP firmware binary download, checksum verification, and partition rollback. | `firmware/esp32-s3/src/ota/` (Planned deliverable path) |
| **TASK-QA-01** | Stage B Lab Verification, Demo Video & Final Report | All Leads (Huy coordinating) | P1 (High) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | All Milestones | Lab fire simulation test, demo video, final PDF report conforming to HCMUT template. | `reports/final_report.pdf`, Demo Video (Planned deliverables) |

---

## 4. Worktree and Branch Governance Rules

To guarantee zero branch contention and zero file collisions:
1. **Approved Future Feature Branch Policy**:
   * All future feature branches must strictly follow the approved role-prefixed convention:
     * **Huy**: `feature/huy-<task-name>` (e.g., `feature/huy-coreiot-onboarding`, `feature/huy-backend-baseline`)
     * **Khánh**: `feature/khanh-<task-name>` (e.g., `feature/khanh-telemetry-simulator`, `feature/khanh-local-gateway-skeleton`)
     * **Ý**: `feature/y-<task-name>` (e.g., `feature/y-frontend-floorplan`, `feature/y-mock-fallback-banner`)
   * *Policy Note*: Previous branch naming patterns (such as `<username>/<feature-topic>`) were transitional bootstrap branches used during initial setup. Future development must strictly conform to `feature/<member>-<task-name>`.
2. **Worktree Directory Isolation**: Each developer and dispatched agent operates strictly within an isolated worktree path. No developer modifies files assigned to another role without explicit review coordination.
3. **Linear Integration onto `develop`**: All pull requests target `develop` with a single squash commit.
