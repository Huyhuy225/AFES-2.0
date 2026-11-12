# AFES 2.0 course requirements and evidence map

Statuses describe accepted evidence on active `develop`, not intent. `DONE (SIMULATION)` never implies physical hardware completion.

## Active P1 path

| Item | Active interpretation | Owner | Status | Dependency | Required acceptance evidence | Task / notes |
|---|---|---|---|---|---|---|
| Stage A | Deterministic telemetry simulator and schema checks | Khánh (`@tranhoangkhanh-hkt`, activation pending) | DONE (SIMULATION) | None | Merged `simulation/` source, tests, fixtures, and [guide](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md). | P1-01 / [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6) (Stage A support only, simulation only; not a scored physical element, no physical ESP32 proof) |
| T08 | Local Gateway on PC/Raspberry Pi | Khánh | NOT STARTED ([#7](https://github.com/Huyhuy225/AFES-2.0/issues/7)) | Stage A | Automated ingest/validation tests, broker test, buffering/replay record, CLI and health/status endpoint. | P1-02 / [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) (Local Gateway T08; no React/Spring backend) |
| Onboarding | Secure CoreIOT project setup | Huy (`@Huyhuy225`) | BLOCKED ([#3](https://github.com/Huyhuy225/AFES-2.0/issues/3)) | Authorized tenant/project access | Redacted setup record, credential-handling procedure, device/gateway mapping, successful secure connection. | P1-03 / [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) (CoreIOT onboarding precondition; blocked on authorized tenant access, no secrets) |
| T11 | CoreIOT native device template and dashboard | Ý (`@gutjmosnin`) | NOT STARTED ([#33](https://github.com/Huyhuy225/AFES-2.0/issues/33)) | Onboarding, gateway test feed | Importable configuration, bound widgets, telemetry/history display, remote-control test, screenshots labelled by evidence mode. | P1-04 / [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33) (native CoreIOT dashboard target configuration, not completed) |
| T12 | CoreIOT RuleChain smart features | Huy | NOT STARTED ([#34](https://github.com/Huyhuy225/AFES-2.0/issues/34)) | Onboarding, T11 telemetry | Exported RuleChain, reviewed thresholds, deterministic trigger/no-trigger tests. | P1-05 / [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) (native CoreIOT RuleChain target configuration, not completed) |
| T13 | CoreIOT alarms and notifications | Huy | NOT STARTED ([#34](https://github.com/Huyhuy225/AFES-2.0/issues/34)) | T12 | Alarm create/clear/acknowledge record and redacted notification delivery evidence. | P1-05 / [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) (native CoreIOT alarms/notifications target configuration, not completed) |
| T15 | Local Gateway/CoreIOT synchronization | Huy and Khánh | NOT STARTED ([#35](https://github.com/Huyhuy225/AFES-2.0/issues/35)) | T08, onboarding, T11–T13 | Reconnect, ordered replay, deduplication, status synchronization, and authorized command round-trip tests. | P1-06 / [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35) (waits on Gateway plus CoreIOT tasks) |
| Hardware foundation | Minimal ESP32-S3 PlatformIO C++ project | Khánh | BLOCKED by hardware access ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) | Board access | Reproducible build, physical flash/boot log, safe defaults, physical MQTT telemetry record. | P1-07 / [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) (PlatformIO foundation only; waits on physical hardware, not proof of T01–T07 live sensor behavior or scored items) |

## Course technology elements

| ID | Technology element | Pts | Current scope / status | Task / notes |
|---|---|---|---|---|
| T01 | Sensor using the I2C interface on Tasmota | 0.5 | DEFERRED | Deferred / not current scope; P1-07 ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) PlatformIO foundation is not proof of T01, and generic I2C is not a T01 claim because Tasmota is required. |
| T02 | Sensor using the Modbus RS485 interface | 1.0 | DEFERRED | Deferred / not current scope; P1-07 ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) PlatformIO foundation does not prove T02. |
| T03 | Sensor connected to another device via BLE | 1.5 | DEFERRED | Deferred / not current scope; P1-07 ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) PlatformIO foundation does not prove T03. |
| T04 | Information inferred by AI (TinyML running on the device) | 1.0 | DEFERRED | Deferred / not current scope; P1-07 ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) PlatformIO foundation does not prove T04. |
| T05 | Tooling for data collection, training and exporting a TinyML model | 1.0 | DEFERRED | Deferred / not current scope; backlog until explicitly approved and supported by item-specific evidence. |
| T06 | Wireless communication using ESP-NOW | 1.5 | DEFERRED | Deferred / not current scope; P1-07 ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) PlatformIO foundation does not prove T06. |
| T07 | Self-implemented on-device Web Server | 1.0 | DEFERRED | Deferred / not current scope; P1-07 ([#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)) PlatformIO foundation does not prove T07. |
| T08 | PC/Raspberry Pi Local Gateway | 1.0 | NOT STARTED | P1-02 / [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7); Local Gateway aggregation, validation, CLI/health endpoint (no React/Spring backend). |
| T09 | AI on Local Gateway | 1.0 | DEFERRED | Deferred / not current scope; backlog until explicitly approved and supported by item-specific evidence. |
| T10 | Local Gateway monitoring and control interface | 1.0 | NOT CLAIMED | NOT CLAIMED; minimal operations CLI and health/status endpoint only, not presented as a scored monitoring/control interface. |
| T11 | CoreIOT templates, dashboard, remote monitoring and control | 1.0 | NOT STARTED | P1-04 / [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33); native CoreIOT device template and dashboard configuration, waits on P1-03 onboarding. |
| T12 | CoreIOT RuleChain | 1.0 | NOT STARTED | P1-05 / [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34); native CoreIOT RuleChain smart logic, paired with T13 alarms. |
| T13 | Alerts when thresholds are exceeded | 0.5 | NOT STARTED | P1-05 / [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34); CoreIOT alarms lifecycle and notification delivery evidence. |
| T14 | OTA firmware updates | 2.0 | DEFERRED | Deferred / not current scope; backlog until explicitly approved and supported by item-specific evidence. |
| T15 | CoreIOT Gateway synchronized with Local Gateway | 2.0 | NOT STARTED | P1-06 / [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35); Local Gateway/CoreIOT state sync, deduplication, replay, and RPC command round trip. |

## Not currently claimed

| Items | Status | Rule | Task / notes |
|---|---|---|---|
| T10 | NOT CLAIMED | Only a minimal gateway CLI and health/status endpoint are planned for operations. This is not presented as a scored monitoring/control interface. | Deferred / not current scope (minimal operations CLI and health endpoint only) |
| T01–T07, T09, T14 | DEFERRED | Backlog until explicitly approved. No `IMPLEMENTED` label without task-specific source and evidence. T01 specifically requires Tasmota; generic I2C is insufficient. | Deferred / not current scope; backlog until explicitly approved and supported by item-specific evidence |
| N01–N07 | DEFERRED | Bonus backlog; none is active scope or an active score claim. | Deferred / not current scope; bonus backlog, no active score claim |

## Evidence rules

1. Label every test artifact `SIMULATION` or `PHYSICAL HARDWARE`.
2. A CoreIOT screenshot must identify the configuration version, test time, device/gateway identity, and evidence mode, with secrets redacted.
3. Physical requirements need real board/sensor/interface evidence; screenshots of synthetic telemetry cannot satisfy them.
4. A task is `DONE` only after source/configuration, tests, evidence, and review are merged.
5. Planned directories and issue descriptions are not implementation evidence.

The authoritative scope decision is [IOT_FIRST_SCOPE.md](docs/project-management/IOT_FIRST_SCOPE.md).
