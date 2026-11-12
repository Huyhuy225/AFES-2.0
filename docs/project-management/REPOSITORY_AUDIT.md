# Repository audit — IoT-first baseline

## Active inventory

| Asset | State | Evidence meaning |
|---|---|---|
| `simulation/` | PRESENT, DONE | Stage A simulated telemetry and contract behavior only. |
| [Stage A simulator guide](../testing/STAGE_A_TELEMETRY_SIMULATOR.md) | PRESENT | Reproduction and evidence boundary. |
| [Telemetry schema](../TELEMETRY_SCHEMA.md) | PRESENT | MQTT/payload contract; not runtime implementation. |
| Local Gateway | NOT STARTED | Tracked by [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7). |
| CoreIOT onboarding/configuration | BLOCKED / NOT STARTED | Tracked by [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3), [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33), and [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34). |
| Gateway synchronization | NOT STARTED | Tracked by [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35). |
| ESP32-S3 PlatformIO foundation | BLOCKED by hardware access | Tracked by [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36). |

## Scope findings

The active architecture is ESP32-S3 → MQTT → Local Gateway → CoreIOT native dashboard/RuleChain/alerts. T10 is limited to a gateway CLI and health/status endpoint and is not claimed for scoring. T01–T07, T09, T14, and N01–N07 are deferred; generic I2C cannot be counted as T01 Tasmota.

## Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| CoreIOT access unavailable | Blocks T11–T13/T15 | Resolve secure onboarding without committing secrets. | Huy |
| Khánh account activation pending | Assignment cannot be applied in GitHub | Keep documented owner and retry only after permissions change. | Huy |
| Hardware unavailable | Blocks physical evidence | Continue simulator/gateway integration; keep claims explicitly simulated. | Khánh |
| Evidence-mode confusion | Inflated completion claims | Require the quality gate and `simulation.is_simulated` propagation. | All reviewers |

This audit supersedes earlier active-scope inventories. See [IOT_FIRST_SCOPE.md](IOT_FIRST_SCOPE.md).
