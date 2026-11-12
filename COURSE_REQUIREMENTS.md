# AFES 2.0 course requirements and evidence map

Statuses describe accepted evidence on active `develop`, not intent. `DONE (SIMULATION)` never implies physical hardware completion.

## Active P1 path

| Item | Active interpretation | Owner | Status | Dependency | Required acceptance evidence |
|---|---|---|---|---|---|
| Stage A | Deterministic telemetry simulator and schema checks | Khánh (`@tranhoangkhanh-hkt`, activation pending) | DONE (SIMULATION) | None | Merged `simulation/` source, tests, fixtures, and [guide](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md). |
| T08 | Local Gateway on PC/Raspberry Pi | Khánh | NOT STARTED ([#7](https://github.com/Huyhuy225/AFES-2.0/issues/7)) | Stage A | Automated ingest/validation tests, broker test, buffering/replay record, CLI and health/status endpoint. |
| Onboarding | Secure CoreIOT project setup | Huy (`@Huyhuy225`) | BLOCKED ([#3](https://github.com/Huyhuy225/AFES-2.0/issues/3)) | Authorized tenant/project access | Redacted setup record, credential-handling procedure, device/gateway mapping, successful secure connection. |
| T11 | CoreIOT native device template and dashboard | Ý (`@gutjmosnin`) | NOT STARTED ([#33](https://github.com/Huyhuy225/AFES-2.0/issues/33)) | Onboarding, gateway test feed | Importable configuration, bound widgets, telemetry/history display, remote-control test, screenshots labelled by evidence mode. |
| T12 | CoreIOT RuleChain smart features | Huy | NOT STARTED ([#34](https://github.com/Huyhuy225/AFES-2.0/issues/34)) | Onboarding, T11 telemetry | Exported RuleChain, reviewed thresholds, deterministic trigger/no-trigger tests. |
| T13 | CoreIOT alarms and notifications | Huy | NOT STARTED ([#34](https://github.com/Huyhuy225/AFES-2.0/issues/34)) | T12 | Alarm create/clear/acknowledge record and redacted notification delivery evidence. |
| T15 | Local Gateway/CoreIOT synchronization | Huy and Khánh | NOT STARTED ([#35](https://github.com/Huyhuy225/AFES-2.0/issues/35)) | T08, onboarding, T11–T13 | Reconnect, ordered replay, deduplication, status synchronization, and authorized command round-trip tests. |
| Hardware foundation | Minimal ESP32-S3 PlatformIO C++ project | Khánh | BLOCKED by hardware access ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) | Board access | Reproducible build, physical flash/boot log, safe defaults, physical MQTT telemetry record. |

## Not currently claimed

| Items | Status | Rule |
|---|---|---|
| T10 | NOT CLAIMED | Only a minimal gateway CLI and health/status endpoint are planned for operations. This is not presented as a scored monitoring/control interface. |
| T01–T07, T09, T14 | DEFERRED | Backlog until explicitly approved. No `IMPLEMENTED` label without task-specific source and evidence. T01 specifically requires Tasmota; generic I2C is insufficient. |
| N01–N07 | DEFERRED | Bonus backlog; none is active scope or an active score claim. |

## Evidence rules

1. Label every test artifact `SIMULATION` or `PHYSICAL HARDWARE`.
2. A CoreIOT screenshot must identify the configuration version, test time, device/gateway identity, and evidence mode, with secrets redacted.
3. Physical requirements need real board/sensor/interface evidence; screenshots of synthetic telemetry cannot satisfy them.
4. A task is `DONE` only after source/configuration, tests, evidence, and review are merged.
5. Planned directories and issue descriptions are not implementation evidence.

The authoritative scope decision is [IOT_FIRST_SCOPE.md](docs/project-management/IOT_FIRST_SCOPE.md).
