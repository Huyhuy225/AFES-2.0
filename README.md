# AFES 2.0 — IoT-first fire monitoring

AFES 2.0 is an IoT course project whose active delivery path is:

```text
ESP32-S3 nodes -> MQTT -> Local Gateway (PC/Raspberry Pi) -> CoreIOT
                                                        -> native dashboard
                                                        -> RuleChain and alarms
```

The active repository does not include a custom web dashboard, application server, database service, public deployment, or server-side REST contract. The earlier web-application prototype remains recoverable without history rewriting on [`archive/web-application-prototype`](https://github.com/Huyhuy225/AFES-2.0/tree/archive/web-application-prototype); it is not active course scope.

## Priority delivery path

| Order | Deliverable | Course item | Owner | Status | Evidence boundary |
|---|---|---|---|---|---|
| 1 | Stage A telemetry simulator | Foundation | Khánh (`@tranhoangkhanh-hkt`, activation pending) | DONE | Simulated evidence only; see [simulator guide](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md). |
| 2 | Local Gateway | T08, minimal T10 operations surface | Khánh | NOT STARTED — [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) | CLI plus health/status endpoint; no browser application. |
| 3 | Secure CoreIOT onboarding | Prerequisite | Huy (`@Huyhuy225`) | BLOCKED — [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3) | Tenant/project access and secrets must be supplied securely. |
| 4 | CoreIOT native dashboard | T11 | Ý (`@gutjmosnin`) | NOT STARTED — [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33) | CoreIOT configuration export plus screenshots/test record. |
| 5 | RuleChain and alerts | T12/T13 | Huy | NOT STARTED — [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34) | CoreIOT export and simulated-trigger evidence. |
| 6 | Gateway synchronization | T15 | Huy and Khánh | NOT STARTED — [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35) | Reconnect, replay, and command-routing tests. |
| 7 | Minimal ESP32-S3 PlatformIO C++ foundation | Hardware foundation | Khánh | BLOCKED by hardware access — [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) | Physical flash/serial evidence is separate from simulation. |

T01–T07, T09, T14, and N01–N07 are deferred backlog unless explicitly approved later. Generic C++ I2C work is not evidence for T01, whose requirement is Tasmota-specific.

## Evidence policy

Every result must be labelled `SIMULATION` or `PHYSICAL HARDWARE`. Simulator output can prove schema, routing, and deterministic scenarios; it cannot prove board flashing, sensors, electrical interfaces, radio behavior, or physical actuation. Detailed policy and status vocabulary live in [IoT-first scope](docs/project-management/IOT_FIRST_SCOPE.md).

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Course traceability](COURSE_REQUIREMENTS.md)
- [Telemetry and MQTT contract](docs/TELEMETRY_SCHEMA.md)
- [Development guide](DEVELOPMENT_GUIDE.md)
- [Task assignment](TASK_ASSIGNMENT.md)
- [Work tracker](WORK_TRACKER.md)
- [Project-management index and scope](docs/project-management/IOT_FIRST_SCOPE.md)

## Security

Never commit CoreIOT credentials, MQTT passwords, device tokens, certificates, or real `.env` files. Use local environment variables, least-privilege credentials, TLS where supported, and redacted evidence. CoreIOT configuration is administered through authorized platform access; device and gateway secrets must not appear in dashboard exports or screenshots.
