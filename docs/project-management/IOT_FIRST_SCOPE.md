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

## Active P1 sequence

1. Stage A simulator — DONE, simulation evidence only.
2. Local Gateway T08 — [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7).
3. Secure CoreIOT onboarding — [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3).
4. CoreIOT native dashboard T11 — [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33).
5. RuleChain and alerts T12/T13 — [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34).
6. Gateway synchronization T15 — [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35).
7. Minimal ESP32-S3 PlatformIO C++ foundation when hardware is accessible — [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36).

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
