# IoT-first scope and evidence policy

This document is the single authoritative scope decision for active AFES 2.0 development. It implements [Issue #32](https://github.com/Huyhuy225/AFES-2.0/issues/32).

## Active product

```text
ESP32-S3 nodes -> MQTT -> Local Gateway (PC/Raspberry Pi) -> CoreIOT
                                                        -> native dashboard (T11)
                                                        -> RuleChain (T12)
                                                        -> alarms (T13)
```

The Local Gateway provides T08 aggregation and a deliberately minimal CLI plus health/status endpoint for operations. That surface is not a current T10 score claim. T15 adds tested synchronization between the gateway and CoreIOT.

## Archived prototype

The earlier React custom dashboard, Spring Boot-oriented application design, database-service plan, Vercel/public-deployment concept, backend REST specification, and related N06 evidence are not active scope. They are preserved for future reference on [`archive/web-application-prototype`](https://github.com/Huyhuy225/AFES-2.0/tree/archive/web-application-prototype). The archive branch must not be deleted or rewritten.

## Active P1 path

| Check | ID | Deliverable | Owner | Dependency | Status | Issue | Acceptance evidence | Technology element(s) |
|---|---|---|---|---|---|---|---|---|
| [x] | P1-01 | Stage A telemetry simulator | Khánh | None | DONE (SIMULATION) | [#6](https://github.com/Huyhuy225/AFES-2.0/issues/6) | Merged `simulation/` source, fixtures, contract tests, and [guide](../testing/STAGE_A_TELEMETRY_SIMULATOR.md); no physical claim. | Support only (Stage A; no scored claim) |
| [ ] | P1-02 | T08 Local Gateway plus minimal operations CLI and health/status endpoint | Khánh | P1-01 | NOT STARTED | [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | Ingest, schema validation, broker integration, buffering/replay, CLI/health endpoint, automated tests. | T08 |
| [ ] | P1-03 | Secure CoreIOT onboarding | Huy | Authorized tenant/project access | BLOCKED | [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Redacted provisioning record and authenticated gateway/device connection. | Prerequisite for T11–T13, T15 |
| [ ] | P1-04 | T11 CoreIOT native device template/dashboard | Ý | P1-03 and test telemetry | NOT STARTED | [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33) | Sanitized importable config, bound widgets/control, screenshots and test record labelled by evidence mode. | T11 |
| [ ] | P1-05 | T12 RuleChain and T13 alarms/notifications | Huy | P1-03, telemetry | NOT STARTED | [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) | Export, trigger/no-trigger test, alarm lifecycle, redacted delivery evidence. | T12, T13 |
| [ ] | P1-06 | T15 gateway synchronization | Huy and Khánh | P1-02 through P1-05 | NOT STARTED | [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35) | Reconnect, ordered replay, deduplication, state sync, authorized command round trip. | T15 |
| [ ] | P1-07 | Minimal ESP32-S3 PlatformIO C++ foundation | Khánh | Physical hardware access | BLOCKED | [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) | Reproducible build and physical flash/boot evidence. | Foundation only (no scored claim yet) |

T01–T07, T09, T14, and N01–N07 are deferred. They must not be labelled `IMPLEMENTED` unless later explicitly approved and supported by item-specific evidence. Generic I2C work does not satisfy the T01 Tasmota requirement.

## Ownership

- Huy (`@Huyhuy225`): CoreIOT onboarding, RuleChain/alarms, integration, final report, governance.
- Khánh (`@tranhoangkhanh-hkt`): gateway and firmware. Activation is pending because GitHub assignment failed due account permissions.
- Ý (`@gutjmosnin`): CoreIOT native dashboard/configuration evidence; no active custom-dashboard responsibility.

## Evidence policy

Every artifact must declare one evidence mode:

- `SIMULATION`: virtual nodes, fixtures, synthetic telemetry, local broker, or simulated CoreIOT triggers.
- `PHYSICAL HARDWARE`: a real ESP32-S3 and attached interfaces, with reproducible build/flash details and observed output.

Simulation can prove contracts, validation, routing, retry logic, dashboard bindings, and RuleChain behavior. It cannot prove flashing, electrical interfaces, radio performance, sensor accuracy, or physical actuation. A status becomes `DONE` only after source/configuration, applicable automated tests, labelled evidence, and review are merged.

## Active documentation map

- [Architecture](../../ARCHITECTURE.md)
- [Course requirements](../../COURSE_REQUIREMENTS.md)
- [Task assignment](../../TASK_ASSIGNMENT.md)
- [Work tracker](../../WORK_TRACKER.md)
- [Development guide](../../DEVELOPMENT_GUIDE.md)
- [Telemetry schema](../TELEMETRY_SCHEMA.md)
- [Roadmap](DEVELOPMENT_ROADMAP.md)
- [Dependency map](DEPENDENCY_MAP.md)
- [Integration plan](INTEGRATION_PLAN.md)
- [Quality gate](QUALITY_GATE.md)
- [Handover protocol](HANDOVER_PROTOCOL.md)
- [Review protocol](REVIEW_PROTOCOL.md)
- [Repository audit](REPOSITORY_AUDIT.md)
