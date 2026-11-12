# AFES 2.0 – Official Assignment Context and Continuity

> **Version**: 1.0.0 · **Issue**: [#13](https://github.com/Huyhuy225/AFES-2.0/issues/13) · **Based on**: `origin/develop` at `bbad07d`
> **Purpose**: one versioned source of truth so any later contributor or session can resume AFES 2.0 without chat history.

---

## 1. Scope and Authority

### 1.1 Official sources (kept outside Git)

| Source | Local reference path (not committed) |
|---|---|
| Course announcement – IoT course project, Semester 261, AY 2026–2027 | `D:\2026-2027\261\IOT\BTL\Project_Annoucement_IoT.pdf` |
| Official report template | `D:\2026-2027\261\IOT\BTL\IoTReport_Template.docx` |

These files are not copied into the repository. This document records only the facts needed to plan and report. Re-check the originals before submission.

### 1.2 Precedence

1. **Course announcement and report template** override every older plan, note or document if they conflict.
2. Repository contracts: [COURSE_REQUIREMENTS.md](../../COURSE_REQUIREMENTS.md), [ARCHITECTURE.md](../../ARCHITECTURE.md), [API_SPECIFICATION.md](../API_SPECIFICATION.md), [TELEMETRY_SCHEMA.md](../TELEMETRY_SCHEMA.md).
3. Project-management documents in this folder (including this file). If one of them conflicts with the sources in level 1, fix it by a PR.

### 1.3 Verified course facts

- Group of **up to three** students.
- **CoreIOT server** and **ESP32-S3 (YoloUNO)** are required. A **multi-device system** is required.
- Deliverables: PDF report **using the template**; accessible **GitHub source with README**; **demo video** (5–10 minutes recommended).
- Score = `min(8, sum of technology elements)` + report (up to 2) + `min(1, sum of advanced features)`; maximum **10**.
- A claimed element needs **evidence** in the report, demo or source. Partial work is **not** a completed claim.
- The report covers: introduction, analysis, implementation, measurement/testing, conclusion/future work, source-code user guide. It includes a **technology self-assessment table** and a **task-assignment table**.
- At least **five quality references**; cite reused sample/source projects; **disclose the scope of AI-tool use**.

---

## 2. Non-Negotiable Principles

1. **Evidence-based completion.** Nothing is "done" without reproducible evidence (tests, logs, screenshots, source, recordings). Do not optimise for the number of claimed features. Every claimed feature maps to the relevant `T01–T15` / `N01–N07` element, and its evidence is preserved (e.g. under `reports/evidence/`).
2. **Simulation is not hardware proof.** Stage A (simulation / contract verification) and physical ESP32-S3 and sensor validation (Stage B) are reported separately. Never present simulation as hardware proof.
3. **Genuine roles.** CoreIOT is the real cloud platform (device profiles, dashboards, rule chains, alerts, OTA). The local gateway does real edge work (aggregation, caching, command routing) and is not a trivial pass-through. Neither role may be faked.
4. **No secrets in Git.** Configuration comes from environment variables with placeholder-only `.env.example`. No tokens, passwords, Wi-Fi credentials or private keys.
5. **PR workflow.** Work on a branch from latest `origin/develop`; one Issue = one branch = one PR; no direct pushes to `main` or `develop`; PRs link their Issue (`Closes #N`) and pass CI. See [CONTRIBUTING.md](../../CONTRIBUTING.md) and [QUALITY_GATE.md](./QUALITY_GATE.md).
6. **Honest status vocabulary.** Use `IMPLEMENTED`, `TESTED`, `DOCUMENTED`, `IN_PROGRESS`, `BLOCKED`, `NOT_STARTED`, as defined in [REPOSITORY_AUDIT.md](./REPOSITORY_AUDIT.md). A document is never `IMPLEMENTED`.
7. **Academic integrity.** Cite reused code, disclose AI use, and keep commit history that reflects each member's real contribution.

---

## 3. Project State (kept separate by certainty)

> This section is derived from [REPOSITORY_AUDIT.md](./REPOSITORY_AUDIT.md) and the other documents linked in §6, at the base commit above. Re-verify against `develop`, Issues, PRs and CI before relying on it.

### 3.1 Verified present state

| Item | State | Where to check |
|---|---|---|
| Course requirements, architecture, API and telemetry contracts | `DOCUMENTED` | root docs, [API_SPECIFICATION.md](../API_SPECIFICATION.md), [TELEMETRY_SCHEMA.md](../TELEMETRY_SCHEMA.md) |
| Repository governance (templates, contributing, development guide) | `DOCUMENTED` | `.github/`, [CONTRIBUTING.md](../../CONTRIBUTING.md), [DEVELOPMENT_GUIDE.md](../../DEVELOPMENT_GUIDE.md) |
| CI | Hygiene checks only (YAML, whitespace, secrets scan). No frontend lint/build/tests in CI. | `.github/workflows/ci.yml`, audit §4 |
| Frontend monitoring baseline (`frontend/`) | `IN_PROGRESS`; Stage A baseline `TESTED` locally (simulated/mock data) | [Stage A evidence](../../reports/evidence/N06/STAGE_A_BASELINE_EVIDENCE.md), audit §3 |
| Project-management documents | `DOCUMENTED` | this folder |

The frontend is the only application module in the repository. No physical-hardware result exists.

### 3.2 Approved decisions (per existing project documents)

- Six-state status vocabulary (§2.6).
- Stage A before Stage B; Stage A results are labelled simulated (`is_simulated` in the telemetry schema).
- Frontend safety rule: read calls may fall back to mock data, but mutations (acknowledge, resolve, control commands) must surface failure and never fake success.
- One worktree/branch per task, branched from `origin/develop`.
- Roles, milestones and ownership: see [TASK_ASSIGNMENT.md](./TASK_ASSIGNMENT.md) and root [TASK_ASSIGNMENT.md](../../TASK_ASSIGNMENT.md).

### 3.3 Pending decisions and blockers

| Item | Note |
|---|---|
| CoreIOT tenant/device provisioning ([#3](https://github.com/Huyhuy225/AFES-2.0/issues/3)) | `BLOCKED` per the audit. No CoreIOT-dependent work until resolved. Never commit credentials. |
| Collaborator invitations and issue assignments | Pending acceptance per the audit. |
| CI coverage for frontend lint/test/build | Not yet in CI; see [QUALITY_GATE.md](./QUALITY_GATE.md). |
| Backend and database technology finalisation | Scheduled later in [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md); not decided in practice. |
| Which technology elements to claim, final demo plan, submission deadlines | Not decided here. Take deadlines only from the official announcement. |

### 3.4 Not started (no source in repository per the audit)

Mock simulator, local gateway, backend, database, CoreIOT configuration, deployment files, ESP32-S3 firmware, physical sensor/radio drivers, TinyML, and all Stage B hardware validation. Planned order and Issues: [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md), [DEPENDENCY_MAP.md](./DEPENDENCY_MAP.md).

---

## 4. Resumption Checklist

- [ ] Read this file, then [COURSE_REQUIREMENTS.md](../../COURSE_REQUIREMENTS.md), the contracts ([API](../API_SPECIFICATION.md), [telemetry](../TELEMETRY_SCHEMA.md)), [ARCHITECTURE.md](../../ARCHITECTURE.md) and [REPOSITORY_AUDIT.md](./REPOSITORY_AUDIT.md).
- [ ] `git fetch origin` and confirm your base is the latest `origin/develop`.
- [ ] Inspect open Issues, open PRs and the latest CI runs (e.g. `gh issue list`, `gh pr list`, `gh run list`).
- [ ] Check [DEPENDENCY_MAP.md](./DEPENDENCY_MAP.md) and [TASK_ASSIGNMENT.md](./TASK_ASSIGNMENT.md); choose **only an unblocked, unclaimed Issue**.
- [ ] Create one branch/worktree from `origin/develop` for that Issue.
- [ ] Do the work within the contracts. Do not change contracts silently; follow [HANDOVER_PROTOCOL.md](./HANDOVER_PROTOCOL.md).
- [ ] Capture evidence and update the status of what you touched (with the vocabulary in §2.6), including Stage A vs. hardware.
- [ ] Run the checks in [QUALITY_GATE.md](./QUALITY_GATE.md) (at minimum `git diff --check` and link validation for docs), open a PR to `develop` with `Closes #N`, and watch CI.

---

## 5. Evidence and Report Preparation Checklist

Aligned to the template's chapters. Confirm exact numbering and wording against the template itself.

- [ ] **Front matter / tables**: group and task-assignment table (who did what); technology self-assessment table listing only elements with evidence (report/demo/source location for each).
- [ ] **Introduction**: problem, objectives, scope and limits (state Stage A vs. hardware scope).
- [ ] **Analysis**: architecture, feature → `T01–T15`/`N01–N07` mapping for every claimed feature, hardware/software list.
- [ ] **Implementation**: devices/firmware, local gateway, CoreIOT configuration, any advanced feature; mark reused sample/source code separately from own work.
- [ ] **Measurement and testing**: test setup, results with real measured values, labelled simulation or hardware; raw logs/screenshots stored under `reports/evidence/`.
- [ ] **Conclusion and future work**: achieved vs. planned, honest limitations.
- [ ] **Source-code user guide**: repository link, structure, requirements, setup (no secrets), build/run steps; README matches the repository.
- [ ] **References**: at least five quality references; reused projects cited.
- [ ] **AI-use disclosure** covering the scope of AI tools used.
- [ ] **Demo video** (5–10 minutes recommended) showing each claimed element working; linked from report and README.
- [ ] Final pass: no claim without evidence; no simulation presented as hardware; no secrets or personal data that should not be public; report follows the template.

---

## 6. Related Documents

**Root and contracts**
- [COURSE_REQUIREMENTS.md](../../COURSE_REQUIREMENTS.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [TASK_ASSIGNMENT.md](../../TASK_ASSIGNMENT.md) (root)
- [API_SPECIFICATION.md](../API_SPECIFICATION.md)
- [TELEMETRY_SCHEMA.md](../TELEMETRY_SCHEMA.md)
- [ORIGINAL_AFES_ANALYSIS.md](../ORIGINAL_AFES_ANALYSIS.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md), [DEVELOPMENT_GUIDE.md](../../DEVELOPMENT_GUIDE.md), [README.md](../../README.md)

**Project management**
- [REPOSITORY_AUDIT.md](./REPOSITORY_AUDIT.md)
- [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md)
- [DEPENDENCY_MAP.md](./DEPENDENCY_MAP.md)
- [INTEGRATION_PLAN.md](./INTEGRATION_PLAN.md)
- [QUALITY_GATE.md](./QUALITY_GATE.md)
- [TASK_ASSIGNMENT.md](./TASK_ASSIGNMENT.md)
- [HANDOVER_PROTOCOL.md](./HANDOVER_PROTOCOL.md)

**Evidence**
- [N06 Stage A baseline evidence](../../reports/evidence/N06/STAGE_A_BASELINE_EVIDENCE.md)
