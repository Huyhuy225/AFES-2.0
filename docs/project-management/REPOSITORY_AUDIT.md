# AFES 2.0 – Comprehensive Repository Audit and Implementation Status Baseline

> **Audit Date**: 2026-11-12
> **Auditor Role**: Repository Analyst / Technical Project Management Documentation Specialist
> **Status**: DRAFT — pending Technical Lead approval
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Evaluation Reference**: IoT Course Semester 261 (HCMUT), Course Project Announcement (2026-10-27)
> **Repository**: [https://github.com/Huyhuy225/AFES-2.0](https://github.com/Huyhuy225/AFES-2.0)
> **Dispatched Worktree**: `D:\orca\workspaces\AFES 2..0\docs-stabilization-audit`
> **Evaluation Model**: Gemini 3.8 Flash (High)

---

## 1. Executive Summary

This repository audit provides an independent, evidence-backed evaluation of the actual source code, documentation contracts, continuous integration pipelines, and project tracking state in the **AFES 2.0** repository on the `develop` branch.

All statuses within this audit and subordinate project management documentation adhere strictly to the standardized six-state implementation vocabulary:
* `IMPLEMENTED`: Functional code written, committed, and integrated into the repository.
* `TESTED`: Code or module verified through executed, reproducible automated or laboratory test suites.
* `DOCUMENTED`: Specifications, architectural contracts, interface schemas, and procedures formalized in markdown, without constituting running software. Documentation-only components are marked strictly as `DOCUMENTED` and never as `IMPLEMENTED`.
* `IN_PROGRESS`: Active development underway with partial code or baseline artifacts present in the repository.
* `BLOCKED`: Development prevented by external dependencies, missing credentials, hardware availability, or administrative access.
* `NOT_STARTED`: Work item defined and scheduled, but no implementation commits exist in the repository.

### 1.1. Core Findings at a Glance
1. **Application Source Footprint**: The **Frontend** (`frontend/`) is currently the **only application module** present in the repository.
2. **Frontend Test Baseline**: The frontend is `IN_PROGRESS` (with its Stage A monitoring baseline `TESTED` locally via 30 passing Vitest unit/integration tests).
3. **Absent Subsystems**: Application backend (`backend/`), microcontroller firmware (`firmware/`), hardware simulator (`tools/mock_simulator/`), Local IoT Gateway (`local-gateway/`), database schema/migrations (`database/`), CoreIOT platform configuration (`coreiot/`), and container deployment configurations (`docker-compose.yml`, Kubernetes manifests) are **completely absent** from the repository source tree.
4. **CI Pipeline Gap & Stale Messaging**: GitHub Actions workflow (`.github/workflows/ci.yml`) executes Repository Hygiene checks (YAML parsing, text formatting, secrets scan, governance file check) which pass (Run ID [`43188041658`](https://github.com/Huyhuy225/AFES-2.0/actions/runs/43188041658)), but CI does **not** execute any frontend linting, build, or Vitest suites. Furthermore, step "Application Test Notice" emits stale text asserting that no application source modules exist.
5. **API Client Safety Separation**: Read-only live API client calls in `frontend/src/api/sensorApi.js` automatically fall back to an in-memory mock store (`mockStore`) when the live backend is unreachable. Conversely, state mutations (`acknowledgeAlarm`, `resolveAlarm`, `dispatchControlCommand`) were corrected to throw errors directly to the UI, strictly preventing false success indications in live mode.
6. **Collaborator Status**: Team members Khánh (`@tranhoangkhanh-hkt`) and Ý (`@gutjmosnin`) have pending repository collaborator invitations (IDs `343116245` and `343093548`). Formal GitHub issue assignments cannot be bound until invitations are accepted.
7. **Issue Tracking Inconsistencies**: Issues [#1](https://github.com/Huyhuy225/AFES-2.0/issues/1) and [#2](https://github.com/Huyhuy225/AFES-2.0/issues/2) remain `OPEN` on GitHub despite their deliverables being merged into `develop` in PR [#5](https://github.com/Huyhuy225/AFES-2.0/pull/5) and PR [#4](https://github.com/Huyhuy225/AFES-2.0/pull/4), due to GitHub default branch auto-close mechanics. Issue [#8](https://github.com/Huyhuy225/AFES-2.0/issues/8) was manually closed following PR [#9](https://github.com/Huyhuy225/AFES-2.0/pull/9).

---

## 2. Evidence-Based Module Inventory and Implementation State

The table below catalogs every subsystem, module, and contract in AFES 2.0 with direct evidence references:

| Module / Component | Path / Location | Implementation State | Evidence Reference (Commit / CI / File) | Detailed Audit Findings |
|---|---|---|---|---|
| **Architecture Contracts** | `ARCHITECTURE.md`, `COURSE_REQUIREMENTS.md` | `DOCUMENTED` | Commit `ec28aef60a227d3e2f6e91ecbad027a04b3578d0` (PR #4) | Specifications and course traceability tables formalize requirements; no executable code. Strictly `DOCUMENTED`, not `IMPLEMENTED`. |
| **API Specification** | `docs/API_SPECIFICATION.md` | `DOCUMENTED` | Commit `ec28aef60a227d3e2f6e91ecbad027a04b3578d0` (PR #4) | REST v2 endpoints (`/api/v2/*`) and WebSocket channels (`/ws/v2/stream`) fully specified; backend service not yet built. |
| **Telemetry Schema** | `docs/TELEMETRY_SCHEMA.md` | `DOCUMENTED` | Commit `ec28aef60a227d3e2f6e91ecbad027a04b3578d0` (PR #4) | Versioned MQTT topics and JSON payloads specified with dual-stage (`is_simulated`) flag; no broker or parser implemented. |
| **Legacy Analysis** | `docs/ORIGINAL_AFES_ANALYSIS.md` | `DOCUMENTED` | Commit `ec28aef60a227d3e2f6e91ecbad027a04b3578d0` (PR #4) | Comprehensive forensic breakdown of original AFES vulnerabilities and architectural deficiencies. |
| **Repository Governance** | `.github/`, `CONTRIBUTING.md`, `DEVELOPMENT_GUIDE.md` | `DOCUMENTED` | Commit `b70d366e9d26db94e14ef347206f8fe02c5716d7` (PR #5) | Branch protection rules, CODEOWNERS, issue templates, PR template, safe `.env.example`, and hygiene policies established. |
| **CI Workflow** | `.github/workflows/ci.yml` | `TESTED` (Hygiene only) | GitHub Run `43188041658` (develop push) | Runs Python hygiene checks (YAML, text formatting, secrets, governance). Passes 100%, but omits application test suites. |
| **Frontend Dashboard Baseline** | `frontend/` (Actual source) | `IN_PROGRESS` / `TESTED` (Stage A) | Commit `bb5bba7059957c5d80a02128d77961ff66af970b` (PR #9) | React 18 / Vite SPA (custom vanilla CSS in `src/index.css`). 7 test files, 30 passing Vitest tests. Full N06 is `IN_PROGRESS` pending backend DB persistence and 2D floorplan. |
| **Telemetry Simulator** | `tools/mock_simulator/` (Planned deliverable path) | `NOT_STARTED` | Open Issue [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6) | Directory does not exist. Proposed simulator deliverable; no synthetic ESP32-S3 data generator exists yet. Assignable to Khánh upon invitation acceptance. |
| **Local IoT Gateway** | `local-gateway/` (Planned deliverable path) | `NOT_STARTED` | Open Issue [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | Directory does not exist. Proposed gateway deliverable; no edge aggregation, SQLite buffering, or command router exists. Assignable to Khánh upon invitation acceptance. |
| **Application Backend** | `backend/` (Planned deliverable path) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Scheduled for Milestone 4 | Directory does not exist. Proposed backend deliverable; no Spring Boot 3 service, JPA models, or REST controllers exist. |
| **CoreIOT Onboarding** | `docs/COREIOT_ONBOARDING.md` (Planned deliverable), `coreiot/` (Planned deliverable path) | `BLOCKED` | Open Issue [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Blocked on tenant provisioning, credentials allocation, and secure onboarding procedure definition. Owned by Technical Lead Huy. |
| **Database & Migrations** | `database/` (Planned deliverable path) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Scheduled for Milestone 4 | No schema files, Liquibase/Flyway migrations, or Docker compose configs exist. |
| **ESP32-S3 Firmware** | `firmware/esp32-s3/` (Planned deliverable path) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Scheduled for Milestone 5 (Stage B) | Directory does not exist. Proposed firmware deliverable; no FreeRTOS, PlatformIO, or sensor driver code exists. |
| **Deployment / Containers** | `deploy/`, `docker-compose.yml` (Planned deliverable paths) | `NOT_STARTED (Planning Entry — GitHub Issue Pending Audit Approval)` | Scheduled for Milestones 3 & 4 | No Dockerfiles, compose specifications, or deployment scripts exist. |

---

## 3. Detailed Verification of Application Source & Testing

### 3.1. Frontend Source and Automated Test Verification
Independent verification was conducted in the `frontend/` directory using Node.js v22.16.0 and npm 11.4.1:

```bash
cd frontend
npm ci
npm test
```

#### Exact Local Vitest Execution Log:
```text
> afes-frontend@2.0.0 test
> vitest run

 RUN  v5.1.0 D:/orca/workspaces/AFES 2..0/docs-stabilization-audit/frontend

 ✓ src/tests/security.test.jsx (2 tests) 25ms
 ✓ src/tests/ZoneCard.test.jsx (2 tests) 53ms
 ✓ src/tests/apiClient.test.jsx (10 tests) 1295ms
 ✓ src/tests/AlarmTriage.test.jsx (3 tests) 71ms
 ✓ src/tests/ControlConsole.test.jsx (3 tests) 89ms
 ✓ src/tests/DeviceList.test.jsx (4 tests) 128ms
 ✓ src/tests/Dashboard.test.jsx (6 tests) 1179ms

 Test Files  7 passed (7)
      Tests  30 passed (30)
   Start at  16:25:51
   Duration  4.46s (import 39%, environment 33%, tests 16%, setup 7%, transform 5%)
```

#### Linting and Production Build Verification:
* **ESLint**: `npm run lint` executed cleanly with 0 errors and 0 warnings.
* **Vite Production Build**: `npm run build` compiled 2,018 modules into production bundle in `dist/` (assets: index CSS 22.36 kB, icons JS 23.16 kB, index JS 48.38 kB, charts JS 542.93 kB) in 3.12s.
* **Evidence Artifact**: Stage A baseline evidence is documented in [reports/evidence/N06/STAGE_A_BASELINE_EVIDENCE.md](../../reports/evidence/N06/STAGE_A_BASELINE_EVIDENCE.md).

### 3.2. Detailed Audit of API Client Behavior (`sensorApi.js`)
Inspection of `frontend/src/api/sensorApi.js` revealed a critical architectural pattern regarding live vs. mock mode:

1. **Read-Only Endpoints Fall Back to Mock**:
   Methods `getZonesSummary()`, `getDevices()`, `getDeviceHealth()`, `getTelemetryHistory()`, and `getActiveAlarms()` execute HTTP requests against `VITE_API_URL` when `VITE_USE_MOCK_DATA=false`. However, when the live network request fails (e.g., backend server down), they catch the error, emit a `console.warn`, and return fallback data from `mockStore`:
   ```javascript
   // frontend/src/api/sensorApi.js (Lines 304-309)
   try {
     return await this._fetch('/zones/summary');
   } catch (err) {
     console.warn('Backend unavailable, falling back to mock zones summary', err.message);
     return mockStore.getZonesSummary();
   }
   ```
   *Operational Risk*: Operators or automated integration tests querying a live system could unknowingly receive synthetic mock data if the backend becomes unavailable.

2. **State Mutation Endpoints Propagate Errors**:
   Mutations modifying safety state—`acknowledgeAlarm(alarmId, note)`, `resolveAlarm(alarmId)`, and `dispatchControlCommand(payload)`—enforce a strict safety invariant:
   ```javascript
   // frontend/src/api/sensorApi.js (Lines 370-376)
   // Explicit live mode: invoke backend REST directly.
   // Safety Invariant: NEVER fall back to mockStore on mutation failure; propagate error directly.
   return await this._fetch(`/alarms/${alarmId}/acknowledge`, {
     method: 'POST',
     body: JSON.stringify({ note: note || 'Acknowledged by operator' }),
   });
   ```
   *Verification*: Confirmed by `src/tests/apiClient.test.jsx` and `src/tests/Dashboard.test.jsx`. When live mutation requests fail, the client propagates the error directly, triggering the UI `ErrorBanner` rather than mutating `mockStore` to fake success.

---

## 4. GitHub Actions CI Audit

### 4.1. Current Execution Status
The current workflow `.github/workflows/ci.yml` triggers on pushes and pull requests to `main` and `develop`.
* **Latest Run**: Run ID [`43188041658`](https://github.com/Huyhuy225/AFES-2.0/actions/runs/43188041658) on branch `develop` (Commit `bb5bba7059957c5d80a02128d77961ff66af970b`).
* **Result**: Passed (Duration: 12 seconds).
* **Steps Executed**:
  1. `actions/checkout@v4.2.2`
  2. `actions/setup-python@v5.4.0` (Python 3.12)
  3. Install dependencies (`pip install pyyaml`)
  4. Validate YAML syntax across `.github/**/*.yml` (all valid)
  5. Validate repository whitespace and text hygiene
  6. Verify secrets hygiene (base64-encoded pattern scanning across 66 files)
  7. Verify governance baseline files exist
  8. Application Test Notice

### 4.2. CI Gaps and Deficiencies
1. **Total Absence of Frontend CI Checks**: The workflow does not set up Node.js, does not run `npm ci`, does not execute Vitest tests, and does not execute ESLint. As a result, regressions in frontend source code or broken tests are not caught in GitHub Actions CI.
2. **Stale CI Step Output**: Step "Application Test Notice" outputs:
   ```text
   ==============================================================================
   APPLICATION TEST STATUS NOTICE:
   This repository is currently in the initial architecture and governance baseline.
   No application source modules (backend, firmware, gateway, frontend) exist yet.
   Per repository governance, application test suites are intentionally not run,
   and no absent application tests are claimed to pass.
   ==============================================================================
   ```
   This message is stale; `frontend/` was merged in PR #9 and is actively maintained in the repository.

---

## 5. GitHub Issues and Pull Requests Tracking Audit

### 5.1. Comprehensive Status Matrix

| Number | Type | Title | GitHub State | Assignee | Actual Technical State | Discrepancy / Root Cause Analysis |
|---|---|---|---|---|---|---|
| **#1** | Issue | Establish repository governance and contribution baseline | `OPEN` | `@Huyhuy225` | `DOCUMENTED` / Merged | **Tracking Inconsistency**: Closed in commit `b70d366` via PR #5, but PR was merged into `develop`. GitHub auto-close keywords only close issues on default branch (`main`). |
| **#2** | Issue | Publish AFES 2.0 course matrix, architecture, telemetry and API contracts | `OPEN` | `@Huyhuy225` | `DOCUMENTED` / Merged | **Tracking Inconsistency**: Closed in commit `ec28aef` via PR #4 into `develop`. GitHub auto-close did not fire. Remains open on GitHub. |
| **#3** | Issue | Prepare secure CoreIOT project onboarding plan | `OPEN` | `@Huyhuy225` | `BLOCKED` / In Planning | Genuine open work item. Blocked on tenant onboarding and credentials provisioning. Owned exclusively by Technical Lead Huy (`@Huyhuy225`); not assignable to Khánh or Ý. |
| **#4** | PR | docs(architecture): publish requirements, contracts, architecture, and original analysis | `MERGED` | `@Huyhuy225` | Merged into `develop` | Closed commit `ec28aef60a227d3e2f6e91ecbad027a04b3578d0`. Established architectural foundation. |
| **#5** | PR | docs(governance): establish repository governance and contribution baseline | `MERGED` | `@Huyhuy225` | Merged into `develop` | Closed commit `b70d366e9d26db94e14ef347206f8fe02c5716d7`. Established CI hygiene and governance. |
| **#6** | Issue | Stage A: build ESP32-S3 telemetry simulator and MQTT contract tests | `OPEN` | Unassigned | `NOT_STARTED` | Genuine open work item for Milestone 2. Assigned to Khánh in planning, pending invitation acceptance. |
| **#7** | Issue | Stage A: implement Local Gateway aggregation and command-routing skeleton | `OPEN` | Unassigned | `NOT_STARTED` | Genuine open work item for Milestone 2. Assigned to Khánh in planning, pending invitation acceptance. |
| **#8** | Issue | Frontend: establish AFES monitoring dashboard baseline | `CLOSED` | Unassigned | `IN_PROGRESS` (Stage A Baseline `TESTED`) | Merged in PR #9 (commit `bb5bba7`). Owner manually closed issue with comment detailing Stage A completion and remaining M4 scope. |
| **#9** | PR | feat(frontend): establish AFES monitoring dashboard baseline | `MERGED` | `@Huyhuy225` | Merged into `develop` | Closed commit `bb5bba7059957c5d80a02128d77961ff66af970b`. Delivered React dashboard and Vitest baseline. |
| **#10** | Issue | Stabilization: audit develop and publish repository management baseline | `OPEN` | `@Huyhuy225` | `IN_PROGRESS` | Current active stabilization task delivering `docs/project-management/`. |

*Note*: In strict accordance with audit constraints, no GitHub issues have been modified or closed.

---

## 6. Team Collaborator and Permissions Audit

Inspection of repository invitations via GitHub API (`/repos/Huyhuy225/AFES-2.0/invitations`):

| Team Member | GitHub Username | Role Assignment | Invitation Status | Permissions | Actual Assignment Status |
|---|---|---|---|---|---|
| **Võ Quang Huy** | `@Huyhuy225` | Technical Lead / Architecture, Backend & CoreIOT | Owner | Admin | Active & Assigned (Owns Issues #1, #2, #3, #10) |
| **Hoàng Khánh** | `@tranhoangkhanh-hkt` | Firmware & Local Gateway Lead (Role 2) | Invitation #`343116245` sent | Write | **Pending Acceptance** (Assignable to Issues #6 and #7 only after acceptance; does not own #3) |
| **Ý** | `@gutjmosnin` | Frontend Engineering & UI/UX Lead (Role 3) | Invitation #`343093548` sent | Write | **Pending Acceptance** (Assignable to future frontend issues only after acceptance; does not own #3) |

*Mandatory Audit Note*: Neither collaborator invitation has been accepted as of this audit. All project management documents represent team assignments as planned and pending acceptance, without claiming accepted status.

### 6.1. Verified Branch Protection Enforcement Audit
Inspection of branch protection rules via GitHub API (`/repos/Huyhuy225/AFES-2.0/branches/{branch}/protection`):
* **`main` Branch**:
  * Status Checks: `strict: true`, requires context `Repository Hygiene`.
  * Pull Request Reviews: `required_approving_review_count: 1`, `require_code_owner_reviews: true`, `require_last_push_approval: true`, `dismiss_stale_reviews: true`.
  * Conversation Resolution: `required_conversation_resolution: true`.
  * Admin Enforcement: `enforce_admins: true`.
* **`develop` Branch**:
  * Status Checks: `strict: true`, requires context `Repository Hygiene`.
  * Pull Request Reviews: `required_approving_review_count: 0`, `require_code_owner_reviews: false`, `require_last_push_approval: false`.
  * Conversation Resolution: `required_conversation_resolution: true`.
  * Admin Enforcement: `enforce_admins: true`.

*Key Finding on Branch Protection*: While `main` enforces 1 approving review and mandatory CODEOWNERS review, `develop` currently enforces 0 approvals and no codeowner reviews. This difference accommodated initial single-maintainer bootstrapping. As team members accept invitations, `develop` must be remediated to require 1 approval and CODEOWNERS reviews.

---

## 7. Comprehensive Risk and Blocker Register

| Risk ID | Category | Description | Severity | Impact | Mitigation Strategy | Owner |
|---|---|---|---|---|---|---|
| **RSK-01** | CI / Quality | CI executes only hygiene checks; frontend tests and builds are unmonitored in GitHub Actions. | High | Regression risks in frontend code unnoticed until manual testing. | Introduce Node.js 22 test job to `.github/workflows/ci.yml` in next DevOps update. | Huy (`@Huyhuy225`) |
| **RSK-02** | CI / Governance | Stale CI messaging claims "No application source modules exist", contradicting reality. | Low | Confusion during grading review and automated audit logs. | Update CI notice text to reflect existing frontend and pending backend/gateway modules. | Huy (`@Huyhuy225`) |
| **RSK-03** | Safety / Architecture | Read-only API calls silently fall back to mock data when backend network requests fail. | High | Operator or automated verification could mistake synthetic mock data for live sensor telemetry. | Introduce explicit UI warning indicator ("DEGRADED: RUNNING ON MOCK FALLBACK") when fallback occurs. | Ý (`@gutjmosnin`, pending) |
| **RSK-04** | Architecture / Delivery | Backend (`backend/`), Local Gateway (`local-gateway/`), and Firmware (`firmware/`) are 100% absent. | High | AFES 2.0 is currently a frontend-only repository; end-to-end integration cannot occur. | Execute Milestone 2 (Simulator & Gateway) and Milestone 4 (Spring Boot Backend) as prioritized. | Huy & Khánh |
| **RSK-05** | Governance / Team | Collaborator invitations for Khánh and Ý are pending acceptance. | Medium | GitHub PR review and issue assignment cannot be enforced on-platform. | Coordinate with team members to accept invitations at `https://github.com/Huyhuy225/AFES-2.0/invitations`. | Huy (`@Huyhuy225`) |
| **RSK-06** | Platform / Access | CoreIOT tenant credentials and server access are unprovisioned (Issue #3). | High | Blocks course elements T11, T12, T13, T15 from entering implementation. | Complete Issue #3 onboarding procedure and configure tenant environment safely. | Huy (`@Huyhuy225`) |
| **RSK-07** | Tracking / Hygiene | Issues #1 and #2 remain open despite merged PRs due to base branch target. | Low | Project board metrics and open issue count appear inaccurate. | Reconcile issue state manually or configure GitHub Project automation. | Huy (`@Huyhuy225`) |
| **RSK-08** | Governance / Security | `develop` branch protection currently requires 0 approving reviews and no CODEOWNERS check. | Medium | Potential for unreviewed merges to `develop` once multiple contributors have push/PR access. | Update `develop` branch protection to require 1 approval and CODEOWNERS review once collaborators accept invitations. | Huy (`@Huyhuy225`) |

---

## 8. Audit Conclusion and Recommendations

The AFES 2.0 repository has successfully established its architectural foundation, contract specifications, and frontend Stage A monitoring baseline. To achieve full stabilization and advance through the course milestones, the team should execute the following actions:
1. Accept collaborator invitations for `@tranhoangkhanh-hkt` and `@gutjmosnin`.
2. Expand `.github/workflows/ci.yml` to include automated testing of `frontend/` (Vitest, lint, build).
3. Resolve CoreIOT onboarding (Issue #3) to unblock cloud integration.
4. Execute Stage A simulator (Issue #6) and Local Gateway skeleton (Issue #7) to establish the edge telemetry pipeline.
