# AFES 2.0 work tracker

This owner-controlled tracker reflects the IoT-first scope approved in [Issue #32](https://github.com/Huyhuy225/AFES-2.0/issues/32). `DONE (SIMULATION)` is never physical-device evidence.

## Status legend

- `DONE`: merged deliverable with its applicable quality gate satisfied.
- `NOT STARTED`: no accepted implementation/configuration evidence.
- `BLOCKED`: an identified external dependency prevents progress.
- `DEFERRED`: outside active scope until explicitly approved.

Khánh (`@tranhoangkhanh-hkt`) is activation pending because GitHub assignment failed due account permissions. The documented ownership remains in force.

## Active P1 path

| Check | ID | Deliverable | Owner | Dependency | Status | Issue | Acceptance evidence |
|---|---|---|---|---|---|---|---|
| [x] | P1-01 | Stage A telemetry simulator | Khánh | None | DONE (SIMULATION) | [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6) | Merged `simulation/` source, fixtures, contract tests, and [guide](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md); no physical claim. |
| [ ] | P1-02 | T08 Local Gateway plus minimal operations CLI and health/status endpoint | Khánh | P1-01 | NOT STARTED | [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | Ingest, schema validation, broker integration, buffering/replay, CLI/health endpoint, automated tests. |
| [ ] | P1-03 | Secure CoreIOT onboarding | Huy | Authorized tenant/project access | BLOCKED | [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Redacted provisioning record and authenticated gateway/device connection. |
| [ ] | P1-04 | T11 CoreIOT native device template/dashboard | Ý | P1-03 and test telemetry | NOT STARTED | [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33) | Sanitized importable config, bound widgets/control, screenshots and test record labelled by evidence mode. |
| [ ] | P1-05 | T12 RuleChain and T13 alarms/notifications | Huy | P1-03, telemetry | NOT STARTED | [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) | Export, trigger/no-trigger test, alarm lifecycle, redacted delivery evidence. |
| [ ] | P1-06 | T15 gateway synchronization | Huy and Khánh | P1-02 through P1-05 | NOT STARTED | [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35) | Reconnect, ordered replay, deduplication, state sync, authorized command round trip. |
| [ ] | P1-07 | Minimal ESP32-S3 PlatformIO C++ foundation | Khánh | Physical hardware access | BLOCKED | [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) | Reproducible build and physical flash/boot/MQTT evidence. |

## Deferred backlog

| Items | Status | Evidence rule |
|---|---|---|
| T10 score claim | DEFERRED / NOT CLAIMED | The P1 gateway includes only an operations CLI and health/status endpoint. |
| T01–T07, T09, T14 | DEFERRED | Require explicit approval, dedicated acceptance tests, and item-specific evidence. Generic I2C does not prove T01 Tasmota. |
| N01–N07 | DEFERRED | Bonus scope is inactive; no implementation claim. |

## Governance completed

| Check | Deliverable | Owner | Status | Evidence |
|---|---|---|---|---|
| [x] | Architecture/contracts baseline | Huy | DONE | [#2](https://github.com/Huyhuy225/AFES-2.0/issues/2), [PR #4](https://github.com/Huyhuy225/AFES-2.0/pull/4) |
| [x] | Repository governance and hygiene CI | Huy | DONE | [#1](https://github.com/Huyhuy225/AFES-2.0/issues/1), [PR #5](https://github.com/Huyhuy225/AFES-2.0/pull/5) |
| [x] | Stabilization audit and management baseline | Huy | DONE | [#10](https://github.com/Huyhuy225/AFES-2.0/issues/10), [PR #11](https://github.com/Huyhuy225/AFES-2.0/pull/11) |
| [x] | Assignment and continuity context | Huy | DONE | [#13](https://github.com/Huyhuy225/AFES-2.0/issues/13), [PR #15](https://github.com/Huyhuy225/AFES-2.0/pull/15) |

## Update rule

Huy is the only authorized submitter for this file. Move a task to `DONE` only when its implementation/configuration, tests, evidence, and review are merged. CoreIOT screenshots, issue text, planned paths, or simulator output alone do not prove physical hardware work.

See [quality gates](docs/project-management/QUALITY_GATE.md), [task assignment](TASK_ASSIGNMENT.md), and [IoT-first scope](docs/project-management/IOT_FIRST_SCOPE.md).
