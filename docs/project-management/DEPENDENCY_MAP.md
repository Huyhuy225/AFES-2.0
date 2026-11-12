# AFES 2.0 – Technical Dependency and Interface Contract Map

> **Document Version**: 2.0.0
> **Status**: DRAFT — pending Technical Lead approval
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Course**: Internet of Things (IoT) – Semester 261 (HCMUT)
> **Documentation Location**: `docs/project-management/DEPENDENCY_MAP.md`

---

## 1. Cross-Module Architectural Dependency Graph

The AFES 2.0 system is architected in a five-tier hierarchy. Dependencies flow strictly through versioned contract boundaries to isolate failure domains and enable decoupled development across the team.

```
+-----------------------------------------------------------------------------+
| TIER 0: TECHNICAL CONTRACTS & GOVERNANCE (DOCUMENTED)                       |
| - docs/TELEMETRY_SCHEMA.md | docs/API_SPECIFICATION.md | ARCHITECTURE.md    |
+-----------------------------------------------------------------------------+
         |                                                 |
         | Telemetry Schema Contract                       | REST & WebSocket Contracts
         v                                                 v
+-----------------------------+                   +---------------------------+
| TIER 1: SENSING NODES       |                   | TIER 4: APPLICATION SERVER|
| [Stage A] tools/mock_sim/   |                   | backend/ (Spring Boot 3)  |
| (Planned deliverable path)  |                   | (Planned deliverable path)|
| [Stage B] firmware/esp32-s3/|                   | (NOT_STARTED)             |
| (Planned deliverable path)  |                   |                           |
+-----------------------------+                   +---------------------------+
         |                                                 ^             ^
         | MQTT Telemetry & Events                         |             |
         v                                                 | REST v2     | STOMP
+-----------------------------+                            | APIs        | WebSockets
| TIER 2: LOCAL IOT GATEWAY   |                            |             |
| local-gateway/src/          |                            |             |
| (Planned deliverable path)  |                            |             |
| (NOT_STARTED - Issue #7)    |                            |             |
+-----------------------------+                            |             |
         |                                                 |             |
         | CoreIOT Sync Protocol (T15)                     |             |
         v                                                 |             |
+-----------------------------+       Spring Mediation     |             |
| TIER 3: COREIOT PLATFORM    | ---------------------------+             |
| coreiot/ (Planned path)     |   (Zero Browser Access)                  |
| (BLOCKED - Issue #3)        |                                          |
+-----------------------------+                                          |
                                                                         v
                                                  +---------------------------+
                                                  | TIER 5: PRESENTATION LAYER|
                                                  | frontend/ (React 18 SPA)  |
                                                  | (IN_PROGRESS - Baseline   |
                                                  |  TESTED locally)          |
                                                  +---------------------------+
```

---

## 2. Interface Contracts and Boundaries

### 2.1. Telemetry and Event Stream Boundary (Tier 1 $\to$ Tier 2)
* **Contract Specification**: [`docs/TELEMETRY_SCHEMA.md`](../TELEMETRY_SCHEMA.md) (`DOCUMENTED`)
* **Transport**: MQTT QoS 1 (telemetry) / QoS 2 (critical fire events).
* **Topic Pattern**: `afes/v2/{tenant_id}/devices/{device_id}/telemetry`
* **Producer Modules**:
  * Stage A: `tools/mock_simulator/` (Open Issue #6; planned deliverable path, `simulation.is_simulated = true`).
  * Stage B: `firmware/esp32-s3/` (Planned deliverable path; physical sensor drivers).
* **Consumer Module**: `local-gateway/src/engine/` (Open Issue #7; planned deliverable path).
* **Dependency Requirement**: Local Gateway cannot validate its aggregation engine until the Stage A simulator emits schema-compliant payloads.

### 2.2. Gateway-to-CoreIOT Synchronization Boundary (Tier 2 $\to$ Tier 3)
* **Contract Specification**: [`docs/TELEMETRY_SCHEMA.md`](../TELEMETRY_SCHEMA.md) Section 2.2 & Course Element **T15** (`DOCUMENTED`)
* **Transport**: CoreIOT Gateway MQTT Protocol.
* **Topic Pattern**: `afes/v2/{tenant_id}/gateways/{gateway_id}/telemetry`
* **Producer Module**: `local-gateway/src/coreiot_sync/` (Planned deliverable path)
* **Consumer Module**: CoreIOT Cloud Server (platform-neutral ThingsBoard instance).
* **Dependency Requirement**: Blocked on CoreIOT tenant provisioning and gateway credential allocation (Open Issue #3, owned by Technical Lead Huy).

### 2.3. Zero-Trust Frontend Security Boundary (Tier 4 $\leftrightarrow$ Tier 5)
* **Mandatory Security Invariant**: Web browser clients **MUST NEVER** communicate directly with CoreIOT or store CoreIOT tokens. All presentation tier traffic is mediated by the Spring Boot Application Server.
* **Contract Specification**: [`docs/API_SPECIFICATION.md`](../API_SPECIFICATION.md) (`DOCUMENTED`)
* **Transport**: HTTPS REST v2 (`/api/v2/*`) and WSS STOMP (`/ws/v2/stream`).
* **Producer Module**: `backend/src/main/java/` (Planned deliverable path; Spring Boot REST controllers).
* **Consumer Module**: `frontend/src/api/sensorApi.js` (Actual React client source).
* **Dependency Requirement**: Frontend fullstack operation (N06) is blocked on Spring Boot backend availability. Frontend currently operates in Stage A mock fallback mode.

---

## 3. Detailed Work Item Dependency Matrix

The table below catalogs exact predecessor-successor relationships across all project tasks:

| Work Item ID | Name | Current State | Strict Predecessors (Must Complete First) | Direct Successors (Blocked Until This Completes) | Critical Path Item? |
|---|---|---|---|---|---|
| **TASK-PM-01** | Stabilization Audit & PM Baseline | `IN_PROGRESS` (Active PR #11, Closes #10) | Commit `bb5bba7` (develop HEAD) | TASK-PM-02, TASK-FE-02 | **Yes** (P0) |
| **TASK-SIM-01** | Stage A ESP32-S3 Simulator (Issue #6) | `NOT_STARTED` (Open Issue #6) | Issue #2 (`DOCUMENTED` contracts) | TASK-GW-01 (Gateway Engine) | **Yes** (Stage A Path) |
| **TASK-GW-01** | Local Gateway Skeleton (Issue #7) | `NOT_STARTED` (Open Issue #7) | TASK-SIM-01 | TASK-GW-02, TASK-GW-03, TASK-GW-04 | **Yes** (Stage A Path) |
| **TASK-IOT-01** | CoreIOT Onboarding Plan (Issue #3) | `BLOCKED` (Open Issue #3; owned by Huy) | Issue #2 (`DOCUMENTED` contracts) | TASK-IOT-02, TASK-IOT-03, TASK-IOT-04, TASK-GW-04 | **Yes** (Cloud Path) |
| **TASK-GW-02** | Gateway Edge AI Fusion (T09) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-GW-01 | Full Gateway Sign-off | No |
| **TASK-GW-03** | Gateway Standalone UI (T10) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-GW-01 | Full Gateway Sign-off | No |
| **TASK-GW-04** | Gateway CoreIOT Sync (T15) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-GW-01, TASK-IOT-01 | Stage A End-to-End Test | **Yes** (Cloud Path) |
| **TASK-BE-01** | Spring Boot 3 Skeleton | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Issue #2, TASK-IOT-01 | TASK-BE-02 | **Yes** (App Path) |
| **TASK-BE-02** | Spring Boot REST/STOMP APIs | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-BE-01 | TASK-FE-04 (Full N06) | **Yes** (App Path) |
| **TASK-FE-01** | Stage A Frontend Baseline | `TESTED` (Merged PR #9, Closed #8) | PR #4, PR #5 | TASK-FE-02, TASK-FE-03 | Completed (Baseline) |
| **TASK-FE-02** | Frontend CI Automation Job | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-FE-01, TASK-PM-01 | Continuous Regression Gate | **Yes** (DevOps Path) |
| **TASK-FE-03** | Degraded Fallback UI Banner | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-FE-01 | Frontend Safety Polish | No |
| **TASK-FE-04** | Persistent Event History & 2D Floorplan | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-FE-01, TASK-BE-02 | Final N06 Sign-off | No (Bonus Feature) |
| **TASK-FW-01** | Stage B ESP32-S3 I2C Driver (T01) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Physical Hardware, Lab Access | Stage B Lab Demo | **Yes** (Stage B Path) |
| **TASK-FW-02** | Stage B Modbus RS485 (T02) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Physical MAX485, Lab Access | Stage B Lab Demo | **Yes** (Stage B Path) |
| **TASK-FW-03** | Stage B BLE Central Client (T03) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | BLE Sensor Beacon, Lab Access | Stage B Lab Demo | **Yes** (Stage B Path) |
| **TASK-FW-04** | Stage B TinyML On-Device (T04/T05) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Dataset Collection, Lab Access | Stage B Lab Demo | **Yes** (Stage B Path) |
| **TASK-FW-05** | Stage B ESP-NOW Mesh (T06) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | 2x ESP32-S3 Boards, Lab Access | Stage B Lab Demo | **Yes** (Stage B Path) |
| **TASK-FW-06** | Stage B Embedded Web Server (T07) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Physical ESP32-S3, Lab Access | Stage B Lab Demo | No |
| **TASK-FW-07** | Stage B CoreIOT OTA Updates (T14) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | TASK-IOT-01, Physical Board | Stage B Lab Demo | **Yes** (Stage B Path) |
| **TASK-QA-01** | Lab Verification, Video & Final Report | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | All Milestones Complete | Course Final Submission | **Yes** (Final Milestone) |

---

## 4. Critical Path and Operational Bottleneck Analysis

Inspection of the dependency graph reveals four critical path bottlenecks:

1. **Bottleneck 1: Collaborator Invitation Acceptance**
   * *Status*: Pending acceptance for Khánh (`@tranhoangkhanh-hkt`) and Ý (`@gutjmosnin`).
   * *Impact*: Issue assignment and formal GitHub PR reviews cannot be completed on GitHub until invitations are accepted. Once accepted, Issues #6 and #7 become assignable to Khánh; future frontend backlog issues become assignable to Ý. Issue #3 remains assigned to Technical Lead Huy (`@Huyhuy225`).
2. **Bottleneck 2: CoreIOT Onboarding & Tenant Credentials (Issue #3)**
   * *Status*: `BLOCKED`. Owned by Technical Lead Huy (`@Huyhuy225`).
   * *Impact*: Completely halts progress on CoreIOT Dashboards (T11), RuleChains (T12), Notification triggers (T13), Gateway Synchronization (T15), and OTA updates (T14).
3. **Bottleneck 3: Stage A Telemetry Simulator (Issue #6)**
   * *Status*: `NOT_STARTED`.
   * *Impact*: Blocks automated testing of Local Gateway aggregation (Issue #7, T08) and end-to-end telemetry pipeline verification.
4. **Bottleneck 4: Spring Boot Backend Implementation**
   * *Status*: `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)`.
   * *Impact*: Traps the React frontend in mock-only fallback mode, preventing full verification of live REST v2 APIs and STOMP WebSocket streams.
