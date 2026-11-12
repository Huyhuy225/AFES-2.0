# AFES 2.0 Work Tracker

This tracker is the English, at-a-glance execution record for AFES 2.0. It separates merged documentation and simulated Stage A work from executable integration and real Stage B hardware evidence. The baseline below reflects `develop` at `1170591` plus the linked GitHub Issues and Pull Requests reviewed on 2026-11-12.

## Status and checkbox legend

- `[x] DONE` — the deliverable is merged into `develop` and its applicable quality gate passed.
- `[-] IN PROGRESS` — implementation or evidence work is active, but the completion gate has not been met.
- `[ ] NOT STARTED` — no accepted implementation or evidence exists yet.
- `[ ] IN REVIEW` — a Pull Request is open; even a passing CI result is not completion until merge.
- `[ ] BLOCKED` — work cannot proceed until the stated external input or dependency is resolved.
- `[ ] PLANNED` — backlog scope has been identified, but no dedicated implementation Issue or accepted source exists.

Priority uses `P1` (high), `P2` (medium), and `P3` (low). Owners marked **activation pending** have a confirmed GitHub username, but their assignment must not be treated as active repository access until the collaborator invitation is accepted.

## Phase A — Governance and contracts

| Check | ID | Task | Owner | Priority | Dependency | Status | GitHub reference / plan | Note / evidence boundary |
|---|---|---|---|---|---|---|---|---|
| [x] | A-01 | Publish architecture, course mapping, API, and telemetry contracts | Huy (`@Huyhuy225`) | P1 | None | DONE | [Issue #2](https://github.com/Huyhuy225/AFES-2.0/issues/2), [PR #4](https://github.com/Huyhuy225/AFES-2.0/pull/4) | Merged documentation defines contracts; it does not prove backend, broker, CoreIOT, gateway, firmware, or hardware implementation. Issue #2 remains open as a tracking discrepancy. |
| [x] | A-02 | Establish repository governance and hygiene CI | Huy (`@Huyhuy225`) | P1 | None | DONE | [Issue #1](https://github.com/Huyhuy225/AFES-2.0/issues/1), [PR #5](https://github.com/Huyhuy225/AFES-2.0/pull/5) | Governance and repository-hygiene checks are merged. Current CI does not constitute full application testing. Issue #1 remains open as a tracking discrepancy. |
| [x] | A-03 | Publish stabilization audit and project-management baseline | Huy (`@Huyhuy225`) | P1 | A-01, A-02 | DONE | [Issue #10](https://github.com/Huyhuy225/AFES-2.0/issues/10), [PR #11](https://github.com/Huyhuy225/AFES-2.0/pull/11) | Audit and management documents are merged; their planned paths and states are not implementation evidence. |
| [x] | A-04 | Publish official assignment and continuity context | Huy (`@Huyhuy225`) | P1 | A-03 | DONE | [Issue #13](https://github.com/Huyhuy225/AFES-2.0/issues/13), [PR #15](https://github.com/Huyhuy225/AFES-2.0/pull/15) | Documentation-only PR is merged and hygiene CI passed. Khánh and Ý assignments remain activation-pending. |
| [ ] | A-05 | Maintain this evidence-based work tracker | Huy (`@Huyhuy225`) | P1 | A-03 | IN REVIEW | [Issue #16](https://github.com/Huyhuy225/AFES-2.0/issues/16), [PR #18](https://github.com/Huyhuy225/AFES-2.0/pull/18), [Issue #19](https://github.com/Huyhuy225/AFES-2.0/issues/19) | Initial tracker is merged; this root relocation and status refresh remains in review until merged. |

## Phase B — Stage A simulator and gateway

| Check | ID | Task | Owner | Priority | Dependency | Status | GitHub reference / plan | Note / evidence boundary |
|---|---|---|---|---|---|---|---|---|
| [x] | B-01 | Build the hardware-independent telemetry simulator | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P1 | A-01 | DONE | [Issue #6](https://github.com/Huyhuy225/AFES-2.0/issues/6), [PR #17](https://github.com/Huyhuy225/AFES-2.0/pull/17) | Merged Stage A virtual simulator and deterministic fixtures. All output remains explicitly simulated and is not ESP32-S3 proof. |
| [x] | B-02 | Add MQTT schema and contract tests for simulated telemetry | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P1 | B-01 | DONE | [Issue #6](https://github.com/Huyhuy225/AFES-2.0/issues/6), [PR #17](https://github.com/Huyhuy225/AFES-2.0/pull/17) | Merged offline contract tests and evidence; no live broker delivery or physical-device claim is made. |
| [ ] | B-03 | Implement local gateway aggregation, status, buffering, and safe command routing | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P1 | B-01, B-02 | NOT STARTED | [Issue #7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | Issue #7 explicitly depends on #6. No `local-gateway/` implementation or gateway test evidence is merged. |
| [ ] | B-04 | Add gateway edge-AI multi-room fusion | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P2 | B-03 | PLANNED | Planned: T09 | Architecture and roadmap scope only; no model, dataset, evaluation, or dedicated implementation Issue exists. |
| [ ] | B-05 | Add standalone local gateway monitoring and control UI | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P2 | B-03 | PLANNED | Planned: T10 | No gateway UI source or offline-operation evidence exists. |

## Phase C — Backend and CoreIOT

| Check | ID | Task | Owner | Priority | Dependency | Status | GitHub reference / plan | Note / evidence boundary |
|---|---|---|---|---|---|---|---|---|
| [ ] | C-01 | Create the Spring Boot backend foundation | Huy (`@Huyhuy225`) | P1 | A-01 | PLANNED | Planned: backend implementation Issue | No `backend/` source, build, or backend test evidence exists. |
| [ ] | C-02 | Implement persistence, migrations, and authentication | Huy (`@Huyhuy225`) | P1 | C-01 | PLANNED | Planned: persistence/auth Issue | MySQL/JPA/Flyway and JWT are specified only; no database or authentication implementation is present. |
| [ ] | C-03 | Implement REST v2 and live STOMP/WebSocket services | Huy (`@Huyhuy225`) | P1 | C-01, C-02 | PLANNED | Planned from [API specification](docs/API_SPECIFICATION.md) | The API is a contract, not an executable service; no live endpoint or stream has been verified. |
| [ ] | C-04 | Complete secure CoreIOT project onboarding | Huy (`@Huyhuy225`) | P1 | A-01; real project/tenant/platform configuration from project owner | BLOCKED | [Issue #3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Blocked on real platform configuration and secure provisioning input. No credentials belong in the repository. |
| [ ] | C-05 | Configure CoreIOT dashboards, RuleChains, alerts, and RPC | Huy (`@Huyhuy225`) | P1 | C-04 | BLOCKED | [Issue #3](https://github.com/Huyhuy225/AFES-2.0/issues/3); T11–T13 | Planned platform mappings are not actual CoreIOT configuration or execution evidence. |
| [ ] | C-06 | Synchronize the local gateway with CoreIOT | Huy and Khánh (`@Huyhuy225`, `@tranhoangkhanh-hkt`; Khánh activation pending) | P1 | B-03, C-04, C-05 | PLANNED | Planned: T15 | No bidirectional edge/cloud synchronization, reconnect, replay, or real-device evidence exists. |

## Phase D — Frontend integration

| Check | ID | Task | Owner | Priority | Dependency | Status | GitHub reference / plan | Note / evidence boundary |
|---|---|---|---|---|---|---|---|---|
| [x] | D-01 | Establish the Stage A monitoring dashboard baseline | Huy (`@Huyhuy225`) | P1 | A-01 | DONE | [Issue #8](https://github.com/Huyhuy225/AFES-2.0/issues/8), [PR #9](https://github.com/Huyhuy225/AFES-2.0/pull/9) | React/Vite source and Stage A tests are merged. Mock/simulated data, persistence, and floorplan limits remain; this is not end-to-end completion. |
| [x] | D-02 | Apply the pastel/neutral UI and explicit simulated-incident behavior | Ý (`@gutjmosnin`; activation pending) | P1 | D-01 | DONE | [Issue #12](https://github.com/Huyhuy225/AFES-2.0/issues/12), [PR #14](https://github.com/Huyhuy225/AFES-2.0/pull/14) | Merged Stage A UI refinement. It does not add backend, gateway, or hardware integration. |
| [ ] | D-03 | Connect the dashboard to live REST and STOMP services | Ý (`@gutjmosnin`; activation pending) | P1 | C-03 | PLANNED | Planned: frontend integration Issue | Current frontend behavior is Stage A/mock-oriented; no verified live backend pipeline exists. |
| [ ] | D-04 | Add persistent event history and an interactive 2D floorplan | Ý (`@gutjmosnin`; activation pending) | P2 | C-02, C-03, D-03 | PLANNED | Planned: remaining N06 scope | No persisted incident history or interactive floorplan source/evidence exists. |
| [ ] | D-05 | Make degraded mock fallback unmistakable in live mode | Ý (`@gutjmosnin`; activation pending) | P2 | D-01 | PLANNED | Planned from repository audit | Read-only API fallback can return mock data; a durable operator-facing degraded-state indicator is not implemented. |

## Phase E — Stage B hardware

| Check | ID | Task | Owner | Priority | Dependency | Status | GitHub reference / plan | Note / evidence boundary |
|---|---|---|---|---|---|---|---|---|
| [ ] | E-01 | Establish real ESP32-S3/YoloUNO firmware and board bring-up | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P1 | B-01, approved hardware access | PLANNED | Planned: firmware foundation Issue | No real firmware source, flash log, or board evidence exists. The Stage A simulator cannot satisfy this row. |
| [ ] | E-02 | Integrate and validate physical I2C, Modbus RS485, and BLE sensors | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P1 | E-01, physical sensors | PLANNED | Planned: T01–T03 | Requires wiring/serial logs and repeatable readings from real devices; contracts and synthetic fixtures are insufficient. |
| [ ] | E-03 | Build TinyML data tooling and run inference on-device | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P2 | E-01, physical dataset | PLANNED | Planned: T04–T05 | No physical dataset, trained/exported model, on-device inference, latency, or accuracy evidence exists. |
| [ ] | E-04 | Implement and validate ESP-NOW communication | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P2 | E-01, multiple physical nodes | PLANNED | Planned: T06 | No radio packet, loss, range, or latency evidence exists. |
| [ ] | E-05 | Implement the embedded diagnostic web server | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P2 | E-01 | PLANNED | Planned: T07 | No on-device page, local control, or browser-to-board evidence exists. |
| [ ] | E-06 | Implement safe OTA update and rollback | Khánh (`@tranhoangkhanh-hkt`; activation pending) | P1 | C-04, E-01 | PLANNED | Planned: T14 | No signed/checksummed update, version transition, reboot, or rollback evidence exists. |
| [ ] | E-07 | Validate physical sensing, alarms, and actuators | Huy and Khánh (`@Huyhuy225`, `@tranhoangkhanh-hkt`; Khánh activation pending) | P1 | E-02–E-06 | PLANNED | Planned: Stage B validation Issue | Completion requires real sensor/actuator observations and safety controls; simulation results must remain separately labelled. |

## Phase F — Integration, testing, deployment, and report

| Check | ID | Task | Owner | Priority | Dependency | Status | GitHub reference / plan | Note / evidence boundary |
|---|---|---|---|---|---|---|---|---|
| [ ] | F-01 | Verify the complete Stage A simulated pipeline | All leads; Huy coordinates | P1 | B-03, C-03, C-05, C-06, D-03 | PLANNED | Planned: end-to-end Stage A Issue | No simulator-to-gateway-to-CoreIOT/backend-to-frontend run is evidenced. Stage A results must remain labelled simulation. |
| [ ] | F-02 | Run integration, security, failure, and recovery tests | All leads; Huy coordinates | P1 | F-01 | PLANNED | Planned: quality Issue | No complete cross-tier authentication, authorization, offline/replay, command-safety, or recovery suite exists. |
| [ ] | F-03 | Run Stage B hardware-in-the-loop and end-to-end validation | All leads; Huy coordinates | P1 | E-07, F-02 | PLANNED | Planned: Stage B integration Issue | Requires real multi-device telemetry and control evidence; no physical validation is currently claimed. |
| [ ] | F-04 | Package and verify deployment | Huy (`@Huyhuy225`) | P1 | F-02, F-03 | PLANNED | Planned: deployment Issue | No complete container/deployment configuration or deployed environment has been verified. |
| [ ] | F-05 | Capture measured reliability and performance evidence | All leads; Huy coordinates | P1 | F-03, F-04 | PLANNED | Planned: evidence Issue | Do not invent targets or results; record reproducible measurements only after the real system runs. |
| [ ] | F-06 | Complete the demo video, final report, citations, and AI-use disclosure | All leads; Huy coordinates | P1 | F-03–F-05 | PLANNED | Planned: final delivery Issue | No final video/PDF deliverable or complete evidence package exists. Claims must trace to source, test, and physical evidence where applicable. |

## Operational update protocol

1. Update a row after its source evidence, GitHub Issue/PR state, review result, CI result, or dependency state changes; include the authoritative link.
2. Mark `DONE` only after the deliverable is merged into `develop` **and** the applicable quality gate in [QUALITY_GATE.md](docs/project-management/QUALITY_GATE.md) passes. An open PR with green CI remains `IN REVIEW`.
3. Keep `DOCUMENTED`, simulated, executable, deployed, and physically verified evidence distinct. Documentation or a passing hygiene check is not implementation proof.
4. Mark hardware, sensor, actuator, OTA, radio, TinyML, or end-to-end physical claims only when reproducible evidence from real equipment is stored and linked. Never promote Stage A simulation evidence to Stage B proof.
5. Preserve stable IDs. If scope changes, update the row or add a new ID; do not silently reuse an ID for different work.

## Next actions

| Order | Action | Unblocks / result |
|---|---|---|
| 1 | Start B-03 under [Issue #7](https://github.com/Huyhuy225/AFES-2.0/issues/7) now that #6 is merged. | Establishes the local gateway prerequisite for later edge/cloud integration. |
| 2 | Have Khánh and Ý accept their collaborator invitations, then activate only the agreed assignments. | Enables accountable ownership for B/E and D work without implying permissions before acceptance. |
| 3 | Project owner supplies the real CoreIOT project/tenant/platform configuration through a secure channel for [Issue #3](https://github.com/Huyhuy225/AFES-2.0/issues/3). | Unblocks C-04/C-05 without storing secrets in Git. |
| 4 | Create focused Issues for C-01–C-03, then implement backend/persistence/auth before D-03 live frontend integration. | Preserves the backend-to-frontend dependency order. |
| 5 | Begin E-01–E-07 only with the real board and sensors, then retain physical logs for F-03–F-06. | Creates defensible Stage B and final-report evidence. |

## Reference documents

- [System architecture](ARCHITECTURE.md)
- [Course requirements and evidence boundaries](COURSE_REQUIREMENTS.md)
- [API specification](docs/API_SPECIFICATION.md)
- [Telemetry schema](docs/TELEMETRY_SCHEMA.md)
- [Development roadmap](docs/project-management/DEVELOPMENT_ROADMAP.md)
- [Dependency map](docs/project-management/DEPENDENCY_MAP.md)
- [Task assignment matrix](docs/project-management/TASK_ASSIGNMENT.md)
- [Integration plan](docs/project-management/INTEGRATION_PLAN.md)
- [Repository audit](docs/project-management/REPOSITORY_AUDIT.md)
- [Handover protocol](docs/project-management/HANDOVER_PROTOCOL.md)
- [Quality gate](docs/project-management/QUALITY_GATE.md)
- [Stage A frontend baseline evidence](reports/evidence/N06/STAGE_A_BASELINE_EVIDENCE.md)
