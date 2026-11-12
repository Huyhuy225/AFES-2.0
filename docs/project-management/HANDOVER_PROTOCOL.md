# AFES 2.0 – Operational Handover and Developer Onboarding Protocol

> **Document Version**: 2.0.0
> **Status**: DRAFT — pending Technical Lead approval
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Course**: Internet of Things (IoT) – Semester 261 (HCMUT)
> **Documentation Location**: `docs/project-management/HANDOVER_PROTOCOL.md`

---

## 1. Purpose and Operational Context

This Handover Protocol provides an actionable, repeatable operational standard for team members and dispatched Orca AI agents to onboard, pick up assigned work items, execute development in isolated worktrees, and hand over tasks asynchronously without lost context, race conditions, or branch contention.

---

## 2. Collaborator Activation and GitHub Access Protocol

### 2.1. Pending Invitations Activation Procedure
At dispatch baseline, repository write invitations are pending for:
* **Hoàng Khánh** ([`@tranhoangkhanh-hkt`](https://github.com/tranhoangkhanh-hkt)) – Invitation ID `343116245`
* **Ý** ([`@gutjmosnin`](https://github.com/gutjmosnin)) – Invitation ID `343093548`

**Action Required for Khánh and Ý**:
1. Log into your GitHub account.
2. Navigate directly to: [https://github.com/Huyhuy225/AFES-2.0/invitations](https://github.com/Huyhuy225/AFES-2.0/invitations).
3. Click **Accept Invitation**.
4. Notify Technical Lead Võ Quang Huy (`@Huyhuy225`) once accepted.
5. Technical Lead will formally bind issue assignment for Khánh on GitHub Issues [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6) and [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) upon acceptance. (Note: Issue #3 remains assigned to Technical Lead Huy for CoreIOT architecture and onboarding; Ý will be assigned to future frontend backlog issues upon acceptance).

---

## 3. Developer Environment Setup and Prerequisites

### 3.1. Role-Specific Toolchains

| Role | Domain | Required Software / SDKs | Verification Command |
|---|---|---|---|
| **Role 1 (Huy)** | Architecture, Backend & CoreIOT | Java 21 LTS (OpenJDK), Maven 3.9+, Docker Desktop | `java -version; mvn -v; docker version` |
| **Role 2 (Khánh)** | Firmware & Local Gateway | Python 3.12, PlatformIO Core (`pio`), Mosquitto broker | `python --version; pio --version; mosquitto -h` |
| **Role 3 (Ý)** | Frontend Engineering & UI/UX | Node.js v22.16+ LTS, npm 11+, Modern Web Browser | `node -v; npm -v` |

### 3.2. Frontend Quickstart (Verified Baseline)
To verify or extend the existing Stage A Frontend Dashboard:
```bash
# 1. Clone repository and navigate to frontend directory
git clone https://github.com/Huyhuy225/AFES-2.0.git
cd AFES-2.0/frontend

# 2. Install dependencies cleanly
npm ci

# 3. Run automated unit and component test suite
npm test

# 4. Run ESLint code style check
npm run lint

# 5. Start local Vite development server
npm run dev
# Browser opens at http://localhost:5173
```

---

## 4. End-to-End Task Pickup and PR Workflow

Every engineer or dispatched worker must execute their work following these seven steps:

```
[ Step 1: Check Issue & Branch ] --> [ Step 2: Create Feature Branch ] --> [ Step 3: Implement & Test Locally ]
                                                                                   |
                                                                                   v
[ Step 6: PR Review & Approval ] <-- [ Step 5: Open PR targeting develop ] <-- [ Step 4: Quality Gate Check ]
          |
          v
[ Step 7: Squash & Merge to develop ]
```

### Step 1: Verify Dependencies and Issue Status
* Inspect the GitHub issue and verify that all prerequisites in `docs/project-management/DEPENDENCY_MAP.md` are fulfilled.
* Ensure you are not starting a blocked task (e.g., CoreIOT tasks before Issue #3 is unblocked).

### Step 2: Create Assigned Feature Branch
* Always base your feature branch on the latest `origin/develop`:
```bash
git fetch origin develop
git checkout -b feature/<member>-<task-name> origin/develop
```
* Approved role-prefixed branch naming convention:
  * **Huy**: `feature/huy-<task-name>` (e.g., `feature/huy-coreiot-onboarding`, `feature/huy-backend-baseline`)
  * **Khánh**: `feature/khanh-<task-name>` (e.g., `feature/khanh-telemetry-simulator`, `feature/khanh-local-gateway-skeleton`)
  * **Ý**: `feature/y-<task-name>` (e.g., `feature/y-frontend-floorplan`, `feature/y-mock-fallback-banner`)
*(Note: Transitional branches during initial bootstrap used `<username>/<topic>`; all future development must strictly follow `feature/<member>-<task-name>`)*.

### Step 3: Implement Changes Adhering to Technical Contracts
* Strictly adhere to [`docs/API_SPECIFICATION.md`](../API_SPECIFICATION.md) and [`docs/TELEMETRY_SCHEMA.md`](../TELEMETRY_SCHEMA.md).
* Never bypass the Zero-Trust security boundary by placing CoreIOT tokens in frontend code.
* In live API clients, never allow failed mutations to silently fake success in mock state.

### Step 4: Execute Local Quality Gate (Gate 1)
```bash
# Whitespace and formatting hygiene
git diff --check

# Module test suite (example for frontend)
cd frontend
npm run lint
npm test
npm run build
```

### Step 5: Document Evidence and Open Pull Request
* Commit reproducible test logs to `reports/evidence/<ITEM_ID>/`.
* Push your branch to `origin`:
```bash
git push -u origin feature/<member>-<task-name>
```
* Open a pull request targeting `develop`.
* Title format: `<type>(<scope>): <short description>` (e.g., `feat(gateway): implement Stage A aggregation skeleton`).
* Body format: Include `Closes #<issue_number>` and paste the test summary and evidence path.

### Step 6: Peer Review and Resolution
* Assign CODEOWNER for review.
* Address all review feedback promptly.

### Step 7: Squash-and-Merge to `develop`
* Complete squash merge once approved and CI passes.
* Verify post-merge CI run on `develop`.

---

## 5. Asynchronous Handoff Template

When concluding an engineering session or handing over to another team member or agent, post a handover briefing using this template:

```markdown
### AFES 2.0 Task Handoff Summary
* **Author / Role**: [Your Name / Username / Role]
* **Task ID & Name**: [e.g., TASK-SIM-01 Stage A Telemetry Simulator]
* **Target Issue**: [e.g., Closes #6]
* **Branch / Commit SHA**: [e.g., feature/khanh-telemetry-simulator @ commit_sha]
* **Status**: [IMPLEMENTED / TESTED / IN_PROGRESS / BLOCKED]

#### 1. What was completed:
* [Bullet 1: Concrete accomplishments, files created or edited]
* [Bullet 2: Verification executed, commands run]

#### 2. What was discovered / validated:
* [Bullet 1: Test results, edge cases identified, logs observed]
* [Bullet 2: Dependencies or technical constraints uncovered]

#### 3. What remains to be done (Next Steps):
* [Bullet 1: Immediate next action for the incoming engineer]
* [Bullet 2: Any open questions or pending reviews]

#### 4. Evidence Location:
* [Link to file in reports/evidence/... or CI Run ID]
```

---

## 6. Incident and Blocker Escalation Protocols

| Issue Type | Symptom / Trigger | Immediate Action | Escalation Target |
|---|---|---|---|
| **CoreIOT Access Blocker** | Missing CoreIOT server credentials, tenant token, or broker host. | Do not guess or commit dummy credentials. Work strictly with mock simulator. | Technical Lead Võ Quang Huy (`@Huyhuy225`) |
| **Contract Inconsistency** | Discrepancy between `API_SPECIFICATION.md` and `TELEMETRY_SCHEMA.md`. | Stop implementation of conflicting interface; do not invent undocumented fields. | Technical Lead Võ Quang Huy (`@Huyhuy225`) |
| **CI Hygiene Failure** | GitHub Actions `Repository Hygiene CI` fails on push. | Inspect run log with `gh run view <run_id> --log`. Resolve trailing whitespace or unredacted secrets locally. | Pull Request Author |
| **Merge Conflict on develop** | Rebase conflict against incoming commits on `origin/develop`. | Fetch `origin/develop`, rebase feature branch locally (`git rebase origin/develop`), resolve conflicts, rerun test suite before force-pushing to feature branch. | Feature Branch Author |
| **Hardware Lab Access Blocker** | Physical YoloUNO board, sensor module, or lab unavailable. | Confine all development to Stage A virtual simulation. Never claim hardware verification without physical evidence. | Course Lecturer / Lab Instructor |
