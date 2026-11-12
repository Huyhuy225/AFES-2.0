# Operational task assignment

This operational view mirrors [the root assignment](../../TASK_ASSIGNMENT.md) and [work tracker](../../WORK_TRACKER.md).

| Task | Owner | Dependency | Status | Evidence |
|---|---|---|---|---|
| Stage A simulator | Khánh (`@tranhoangkhanh-hkt`, activation pending) | None | DONE (SIMULATION) | `simulation/` plus [guide](../testing/STAGE_A_TELEMETRY_SIMULATOR.md). |
| T08 gateway and minimal CLI/health surface | Khánh | Stage A | NOT STARTED — [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | Gateway automated/integration tests. |
| Secure CoreIOT onboarding | Huy (`@Huyhuy225`) | Authorized access | BLOCKED — [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Redacted connection/provisioning record. |
| T11 native CoreIOT dashboard | Ý (`@gutjmosnin`) | Onboarding, telemetry | NOT STARTED — [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33) | Sanitized config export and labelled UI evidence. |
| T12/T13 RuleChain and alarms | Huy | Onboarding, telemetry | NOT STARTED — [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) | Export, branch tests, alarm lifecycle. |
| T15 synchronization | Huy and Khánh | Gateway, T11–T13 | NOT STARTED — [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35) | Reconnect/replay/deduplication/command tests. |
| ESP32-S3 foundation | Khánh | Hardware access | BLOCKED — [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) | Physical build/flash/boot/MQTT record. |

Khánh’s GitHub activation is pending because assignment failed due account permissions. Ý’s active responsibility is limited to T11 native configuration. Deferred items require explicit approval before assignment or implementation.
