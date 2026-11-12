# AFES 2.0 task assignment

## Ownership

| Person | Account | Active responsibility | Access note |
|---|---|---|---|
| Võ Quang Huy | [`@Huyhuy225`](https://github.com/Huyhuy225) | CoreIOT onboarding, RuleChain/alarms, integration, final report, repository governance | Active owner. |
| Hoàng Khánh | [`@tranhoangkhanh-hkt`](https://github.com/tranhoangkhanh-hkt) | Local Gateway and ESP32-S3 firmware foundation | Activation pending; GitHub assignment failed because account permissions/access are not yet sufficient. Ownership remains documented here. |
| Ý | [`@gutjmosnin`](https://github.com/gutjmosnin) | CoreIOT native device template/dashboard configuration and evidence | Active responsibility is limited to T11 native configuration. |

## Active tasks

| Task | Owner | Priority | Dependency | Status | Test/evidence gate |
|---|---|---|---|---|---|
| Stage A simulator | Khánh | P1 | None | DONE (SIMULATION) | Preserve merged `simulation/` source and [test guide](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md). |
| T08 Local Gateway, including minimal operations surface | Khánh | P1 | Stage A | NOT STARTED — [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | Ingest, validation, buffering/replay, CLI, health/status endpoint, tests. |
| Secure CoreIOT onboarding | Huy | P1 | Tenant/project access | BLOCKED — [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Redacted provisioning and successful authenticated connection. |
| T11 CoreIOT native dashboard | Ý | P1 | Onboarding and test telemetry | NOT STARTED — [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33) | Importable template/dashboard config and labelled evidence. |
| T12/T13 RuleChain and alerts | Huy | P1 | Onboarding and telemetry | NOT STARTED — [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) | Export, trigger/no-trigger tests, alarm lifecycle and delivery record. |
| T15 gateway synchronization | Huy and Khánh | P1 | T08, T11–T13 | NOT STARTED — [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35) | Reconnect/replay/deduplication and command round trip. |
| ESP32-S3 PlatformIO foundation | Khánh | P1 when hardware is accessible | Board access | BLOCKED — [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) | Build plus physical flash/boot/MQTT evidence. |

## Deferred ownership

T01–T07, T09, T14, and N01–N07 have no active delivery commitment. If the team approves one later, create or update a dedicated issue with owner, dependency, acceptance test, and evidence mode before implementation begins. T10 remains intentionally minimal and is not a score claim.

Use [WORK_TRACKER.md](WORK_TRACKER.md) for status and [IOT_FIRST_SCOPE.md](docs/project-management/IOT_FIRST_SCOPE.md) for policy.
