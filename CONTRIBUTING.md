# AFES 2.0 Contributing & Repository Governance Guidelines

Welcome to the **AFES 2.0 (Advanced Fire Emergency System – Multi-Node IoT Monitoring and Emergency Response)** project. This document outlines our repository governance policies, branch management, pull request workflows, code ownership rules, and contribution standards.

All contributors—whether working on embedded firmware, local gateways, CoreIOT integration, backend services, or frontend dashboards—must adhere to these guidelines.

---

## 1. Core Governance Principles

### 1.1 PR-Only Workflow
- **No Direct Pushes**: Direct pushes to `main` and `develop` are strictly prohibited.
- **Base Integration Branch**: All day-to-day development branches must be branched from and merged into **`develop`**.
- **Production / Milestone Releases**: `main` is reserved exclusively for stable milestone tags and production releases, merged only from `develop` via dedicated release pull requests.
- **Traceability**: Every pull request must be linked to a tracked GitHub Issue and declare corresponding Course Requirement IDs.

### 1.2 Single Responsibility & Scoped Work
- Each pull request must focus on a single, well-defined task or issue.
- Contributors must edit only the authorized files designated for their assigned task or worktree. Never modify unrelated modules, dependency manifests, or other workers' active files without coordination.

---

## 2. Branch Naming Conventions

All feature, fix, or documentation branches must branch off `develop` and follow this standardized naming convention:

```text
<type>/<issue-number>-<short-description>
```

Or, when working within an Orca multi-agent worktree:
```text
<username>/<task-slug>
```

### 2.1 Standard Branch Types
| Prefix | Purpose | Example |
|---|---|---|
| `feat/` | New features, sensors, or functional capabilities | `feat/12-flame-sensor-driver` |
| `fix/` | Bug fixes in firmware, gateway, backend, or UI | `fix/45-mqtt-reconnect-backoff` |
| `docs/` | Documentation, contracts, architecture, or governance | `docs/1-governance-baseline` |
| `chore/` | Tooling, CI/CD, build setup, dependency updates | `chore/ci-hygiene-baseline` |
| `refactor/` | Code reorganization without functional changes | `refactor/telemetry-serializer` |
| `test/` | Adding or updating simulation/hardware tests | `test/mock-node-harness` |

### 2.2 Rules for Branch Names
- Use lowercase alphanumeric characters and hyphens only (no spaces, underscores, or uppercase).
- Always include the linked issue number when applicable.
- Keep descriptions brief and meaningful (2 to 5 words).

---

## 3. Commit Message Guidelines

We follow the **Conventional Commits** specification to ensure clear and automated changelog generation:

```text
<type>(<scope>): <short imperative description>

[optional body explaining motivation and details]

[optional footer(s), e.g., Closes #1, Course-ID: T01]
```

### 3.1 Allowed Commit Types
- `feat`: A new feature or capability.
- `fix`: A bug fix.
- `docs`: Documentation changes only.
- `chore`: Repository maintenance, CI, build configurations.
- `refactor`: Code changes that neither fix a bug nor add a feature.
- `test`: Adding missing tests or correcting existing tests.

### 3.2 Commit Quality Rules
- Write commit subjects in the imperative mood (e.g., `feat(gateway): add MQTT payload validation` rather than `added MQTT payload validation`).
- Do not commit generated build outputs, binary blobs, `.env` files, or temporary editor files.
- Keep commits atomic and logically coherent.

---

## 4. Pull Request Lifecycle & Review Process

To land any code or documentation into `develop`, follow this step-by-step lifecycle:

```
[GitHub Issue] -> [Branch from develop] -> [Local Development & Validation]
      -> [Open PR with Template] -> [CI Hygiene & CODEOWNERS Review] -> [Squash & Merge]
```

### Step 1: Issue Linkage & Course Traceability
- An open GitHub Issue must exist before opening a PR.
- The PR description must include `Closes #<issue_number>` to automatically resolve the issue upon merge.
- Identify the relevant **Course Requirement ID** (`T01` through `T15`). If the PR does not relate to a specific course requirement (e.g., repository governance or CI), specify `N/A (General Governance/DevOps)`.

### Step 2: Local Verification
Before submitting a pull request, you must execute:
1. `git diff --check` to ensure there are no trailing whitespace errors or conflict markers.
2. Syntax and schema validations (YAML, JSON, Python, C++, etc.).
3. Simulation validation or physical hardware tests as outlined in [`DEVELOPMENT_GUIDE.md`](DEVELOPMENT_GUIDE.md).

### Step 3: Open Pull Request with the Required Template
Fill out all sections of `.github/pull_request_template.md`:
- **Linked Issue**: Must clearly state `Closes #<id>`.
- **Course Requirement ID**: Required traceability identifier (`T01`–`T15` or `N/A`).
- **Summary**: Concise bullet points explaining changes and motivation.
- **Testing & Validation**: Explicitly distinguish between **Simulation Validation** and **Physical Hardware Validation**. Record exact commands executed and actual exit codes.
- **Screenshots / Logs**: Attach sanitized terminal output, serial monitor logs, or screenshots when relevant.
- **Pre-Submission Checklist**: Confirm all compliance checkboxes.

### Step 4: Code Ownership & Review
- Pull requests automatically request review from designated code owners in `.github/CODEOWNERS`.
- Current primary code owner: **`@Huyhuy225`**.
- Pending co-maintainers (**Khánh** and **Ý**) will be added as code owners once their official GitHub accounts are provisioned.
- At least one code owner approval is required before merging.

### Step 5: Merge Strategy
- Pull requests are merged into `develop` using **Squash and Merge** to maintain a clean, linear git history.
- The branch must be deleted immediately after a successful merge.

---

## 5. Code Ownership & Responsibilities

The repository maintains an authoritative `.github/CODEOWNERS` file:

- **Lead Maintainer**: `@Huyhuy225` (reviews architecture, governance, CoreIOT platform integration, and backend services).
- **Frontend Maintainer**: `@gutjmosnin` (reviews frontend dashboards, UI components, and presentation layer).
- **Pending Maintainer (Firmware & Local Gateway)**: **Khánh** (assigned to ESP32 firmware, physical sensor drivers, and local-gateway integration; handle pending confirmation).

All contributors must respect code ownership boundaries. Do not bypass or self-merge pull requests.

---

## 6. Security, Secrets, and Zero-Credential Policy

### 6.1 Absolute Zero-Secrets Rule
- **Never commit real credentials**: No production passwords, API tokens, MQTT credentials, private keys (`.pem`, `.key`), or SSH keys may ever be committed to the repository.
- **Use `.env.example`**: All configuration variables must have safe placeholder entries documented in `.env.example`.
- **Local Configuration**: Developers must copy `.env.example` to `.env` locally. The `.env` file is ignored by `.gitignore` and must never be staged.

### 6.2 Pre-Commit Secret Scanning
Before staging files, verify that no secrets or sensitive data exist:
```bash
git diff --staged | grep -E "(PASSWORD|SECRET|TOKEN|KEY|PRIVATE)"
```

### 6.3 Incident Response
If a real secret is accidentally committed:
1. Immediately notify the repository administrator (`@Huyhuy225`).
2. Revoke and rotate the exposed credential immediately in the external service.
3. Rewrite the git history to eliminate the secret artifact before pushing upstream.

---

## 7. Development & Testing Standards

All contributors must review and follow [`DEVELOPMENT_GUIDE.md`](DEVELOPMENT_GUIDE.md) for detailed instructions on:
- Setting up the local development environment.
- Running simulation suites without physical hardware.
- Conducting bench-level physical hardware validation on ESP32 boards and sensors.
- Formatting, linting, and automated checks.
