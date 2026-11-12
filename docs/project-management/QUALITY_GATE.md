# AFES 2.0 – Quality Gates, Automated Verification and Acceptance Standards

> **Document Version**: 2.0.0
> **Status**: DRAFT — pending Technical Lead approval
> **Target Base**: `develop` branch at commit [`bb5bba7059957c5d80a02128d77961ff66af970b`](https://github.com/Huyhuy225/AFES-2.0/commit/bb5bba7059957c5d80a02128d77961ff66af970b)
> **Course**: Internet of Things (IoT) – Semester 261 (HCMUT)
> **Documentation Location**: `docs/project-management/QUALITY_GATE.md`

---

## 1. Quality Policy and Objective

The AFES 2.0 quality framework ensures that every pull request entering the `develop` baseline is verified, secure, and documented. No code is integrated based on assumption; all functional claims require concrete, reproducible evidence.

Quality enforcement operates through a progression of five mandatory gates:

```
+------------------+     +------------------+     +------------------+     +------------------+     +------------------+
|      GATE 1      |     |      GATE 2      |     |      GATE 3      |     |      GATE 4      |     |      GATE 5      |
| Local Pre-Commit | --> |  Automated CI    | --> |  Peer Review &   | --> |  Evidence &      | --> |  Protected Merge |
|  & Module Tests  |     |   Hygiene Gate   |     |    Governance    |     |  Traceability    |     |    to develop    |
+------------------+     +------------------+     +------------------+     +------------------+     +------------------+
```

---

## 2. Gate 1: Local Pre-Commit and Module-Specific Verification

Before opening a pull request or pushing to an assigned remote branch, the developer must execute and pass all validations relevant to the modified subsystem:

### 1. Repository Whitespace and Diff Hygiene
* **Command**: `git diff --check`
* **Criterion**: 0 trailing whitespace violations, 0 missing final newlines, 0 merge conflict artifacts.

### 2. Module-Specific Test Suites
The developer must execute the test suite corresponding to their modified module:
* **Frontend (`frontend/`)**:
  * Unit and Component Tests: `cd frontend && npm test` (Vitest must pass 100% of tests).
  * Linter: `cd frontend && npm run lint` (ESLint must exit with code 0, 0 errors, 0 warnings).
  * Production Build: `cd frontend && npm run build` (Vite must compile clean assets to `dist/`).
* **Microcontroller Firmware (`firmware/esp32-s3/`)** (Stage B):
  * Unit Tests: `pio test -e native` (Native Unity tests for C/C++ sensor drivers, ring buffers, CRC checks).
  * Linter: `pio check` (Cppcheck static analysis).
* **Local IoT Gateway (`local-gateway/`)**:
  * Unit and Integration Tests: `pytest tests/` (MQTT packet normalization, SQLite buffer, command router).
  * Linter: `flake8` or `black --check`.
* **Application Backend (`backend/`)**:
  * Unit and Integration Tests: `./mvnw clean test` (Spring Boot JUnit 5, MockMvc, JPA testcontainers).
  * Code Quality: `./mvnw checkstyle:check`.

### 3. Secrets Hygiene
* **Command**: Developer must review changed files to ensure zero unredacted secrets, passwords, private keys, Wi-Fi credentials, or CoreIOT access tokens exist. All configuration must reference `.env.example` placeholders.

---

## 3. Gate 2: GitHub Actions Automated CI Gate

The GitHub Actions workflow [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) validates all pushes and PRs targeting `main` and `develop`.

### Current Audited Pipeline Status:
* **Current Workflow**: `Repository Hygiene CI` (Run ID [`43188041658`](https://github.com/Huyhuy225/AFES-2.0/actions/runs/43188041658) passed on `develop`).
* **Hygiene Checks Passed**:
  1. YAML syntax parsing across all `.github/**/*.yml` files.
  2. Whitespace and text hygiene check across all repository files.
  3. Secrets hygiene scanning with base64-encoded pattern matching.
  4. Governance baseline file existence check (`CONTRIBUTING.md`, `DEVELOPMENT_GUIDE.md`, `.github/CODEOWNERS`, etc.).

### Quality Gate Enhancement Plan (Resolving RSK-01 and RSK-02):
1. **Frontend Automated CI Job**: In task `TASK-FE-02`, add a dedicated Node.js CI job running:
   ```yaml
   frontend-ci:
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v4
       - uses: actions/setup-node@v4
         with:
           node-version: 22
           cache: 'npm'
           cache-dependency-path: frontend/package-lock.json
       - run: cd frontend && npm ci
       - run: cd frontend && npm run lint
       - run: cd frontend && npm test
       - run: cd frontend && npm run build
   ```
2. **Update Stale CI Messaging**: Revise the "Application Test Notice" step to accurately report the existing frontend test suite while noting absent backend and gateway modules.

---

## 4. Gate 3: Peer Review and Governance Gate

Every pull request must meet all governance rules defined in `CONTRIBUTING.md` and `.github/CODEOWNERS`:

1. **Target Branch**: Pull requests must target `develop`. Direct PRs to `main` are rejected unless tagged as an official production release.
2. **Traceability Linkage**: The PR title must follow conventional commits (e.g., `feat(frontend): ...`, `docs(pm): ...`). The PR body must include `Closes #<issue_number>` to maintain bidirectional issue traceability.
3. **Approved Branch Naming Policy**: The branch must originate from the approved role-prefixed convention:
   * **Huy**: `feature/huy-<task-name>`
   * **Khánh**: `feature/khanh-<task-name>`
   * **Ý**: `feature/y-<task-name>`
   *(Note: Transitional branches during initial bootstrap used `<username>/<topic>`; future feature work must strictly use `feature/<member>-<task-name>`)*.
4. **Current Verified Enforcement vs. Desired Policy**:
   * **Desired Policy**: Every PR targeting `develop` must receive at least 1 peer approval and CODEOWNERS sign-off before merging:
     * Architecture, Backend, CoreIOT changes reviewed by `@Huyhuy225`.
     * Firmware and Gateway changes reviewed by `@tranhoangkhanh-hkt`.
     * Frontend changes reviewed by `@gutjmosnin`.
   * **Current Verified GitHub Enforcement**:
     * `main`: Strictly enforces `required_approving_review_count: 1` and `require_code_owner_reviews: true`.
     * `develop`: Currently configured with `required_approving_review_count: 0` and `require_code_owner_reviews: false` (while strictly enforcing Repository Hygiene CI and conversation resolution).
   * **Governance Gap & Remediation**:
     * *Gap*: PRs to `develop` can technically merge with 0 approvals on GitHub during the single-maintainer bootstrap period.
     * *Remediation Plan*: As soon as collaborator invitations for Khánh (`@tranhoangkhanh-hkt`) and Ý (`@gutjmosnin`) are accepted, Technical Lead Huy will update `develop` branch protection to require 1 approval and mandatory CODEOWNERS review. In the interim, peer review approval is a required procedural rule for all team pull requests.
5. **No Scope Creep**: PRs must modify only files directly relevant to the assigned issue. Documentation PRs must never touch application source code; application PRs must never alter governance or root contracts without explicit architectural consensus.

---

## 5. Gate 4: Evidence and Traceability Gate

To prevent unsupported completion claims, every implementation PR must commit concrete test evidence:

1. **Evidence Directory Convention**:
   * Evidence artifacts must be placed in `reports/evidence/<ITEM_ID>/` (e.g., `reports/evidence/N06/STAGE_A_BASELINE_EVIDENCE.md`).
2. **Stage A vs. Stage B Labeling**:
   * Evidence generated via simulation or contract mocks must be explicitly tagged `[SIMULATED - STAGE A]`.
   * Claims of physical hardware verification (`STAGE_B`) must include oscilloscope captures, physical serial console logs, or laboratory test photos.
3. **Standard Vocabulary Compliance**:
   * Status updates in PR descriptions and reports must adhere strictly to the vocabulary:
     * `IMPLEMENTED`: Code exists.
     * `TESTED`: Passing test logs committed.
     * `DOCUMENTED`: Specifications only (documentation-only PRs are never marked `IMPLEMENTED`).
     * `IN_PROGRESS`: Partially complete.
     * `BLOCKED`: Reason and blocker ID recorded.
     * `NOT_STARTED`: Scheduled.

---

## 6. Gate 5: Protected Branch Merge Gate

1. **Squash and Merge Only**: All PRs merged into `develop` must be squash-merged to preserve a clean, linear, and bisectable git history.
2. **Commit Message Format**: The squashed commit message must retain the PR title and `Closes #<issue_number>` metadata.
3. **Post-Merge Verification**: Following merge, the author must verify that the GitHub Actions CI run on `develop` executes cleanly.
