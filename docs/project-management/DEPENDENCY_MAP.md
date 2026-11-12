# IoT-first dependency map

```text
Stage A simulator (DONE, SIMULATION)
        |
        +--> T08 Local Gateway #7 ----------------------+
        |                                               |
        +--> secure CoreIOT onboarding #3 --> T11 #33 --+--> T15 sync #35
                                             |
                                             +--> T12/T13 #34

physical hardware access --> ESP32-S3 foundation #36 --> later physical evidence
```

| Deliverable | Depends on | Blocks | Owner | Status |
|---|---|---|---|---|
| Stage A simulator | None | T08 contract work | Khánh | DONE (SIMULATION) |
| T08 gateway | Stage A | T15 | Khánh | NOT STARTED |
| CoreIOT onboarding | Authorized tenant/project access | T11–T13, T15 | Huy | BLOCKED |
| T11 native dashboard | Onboarding and telemetry | T15 evidence | Ý | NOT STARTED |
| T12/T13 rules and alarms | Onboarding and telemetry | Integrated alarm flow | Huy | NOT STARTED |
| T15 synchronization | T08, onboarding, T11–T13 | End-to-end P1 acceptance | Huy and Khánh | NOT STARTED |
| ESP32-S3 foundation | Physical board access | Physical Stage B evidence | Khánh | BLOCKED |

T10 is limited to gateway CLI/health operations and is not claimed. T01–T07, T09, T14, and N01–N07 are deferred and do not block P1.

Interface authority: [telemetry schema](../TELEMETRY_SCHEMA.md). Scope authority: [IOT_FIRST_SCOPE.md](IOT_FIRST_SCOPE.md).
