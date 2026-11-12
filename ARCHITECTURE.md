# AFES 2.0 IoT-first architecture

## Active system boundary

```text
[ESP32-S3 nodes]
        |
        | MQTT telemetry / status / events
        v
[Local Gateway on PC or Raspberry Pi]
        |  validate, normalize, buffer, replay, route commands
        |  minimal operations CLI + health/status endpoint
        v
[CoreIOT]
        |  device template + native dashboard (T11)
        |  RuleChain (T12) + alarms/notifications (T13)
        |  gateway synchronization (T15)
        v
[Operator in CoreIOT native UI]
```

CoreIOT is the active application and operations surface; layers outside the diagram are out of scope.

## Components

### ESP32-S3 nodes

Issue [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) defines a minimal PlatformIO C++ foundation when hardware becomes accessible: board configuration, safe boot, telemetry model, MQTT connectivity, and serial/flash evidence. It does not claim T01–T07 or T14. In particular, a generic I2C driver is not equivalent to the T01 Tasmota requirement.

### Local Gateway

Issue [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7) owns T08. The gateway runs on a developer PC or Raspberry Pi and:

- accepts Stage A simulator and later physical-node messages;
- validates the [telemetry schema](docs/TELEMETRY_SCHEMA.md);
- preserves the `simulation.is_simulated` evidence marker;
- buffers messages during upstream outage and replays them safely;
- exposes a CLI and small health/status endpoint for operations;
- forwards telemetry to CoreIOT and routes authorized commands back.

That CLI and endpoint are the intentionally minimal interpretation of T10; T10 is not currently claimed for scoring and must not grow into a custom browser application without explicit approval.

### CoreIOT

- [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3): secure project onboarding, credentials, device/gateway mapping.
- [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33): T11 device template, native dashboard, widgets, and remote controls.
- [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34): T12 RuleChain and T13 alarms/notifications.
- [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35): T15 synchronization, reconnect, replay, and commands.

## Data and control flows

Telemetry flows from a node or the simulator to the gateway, then to CoreIOT. CoreIOT stores platform telemetry, updates native widgets, evaluates the RuleChain, and creates alarms. Authorized remote control travels from a CoreIOT widget or RuleChain through the gateway to the target node; acknowledgements return along the same path.

The gateway must reject invalid schema versions, preserve message IDs for deduplication, use bounded retries, and avoid replaying unsafe commands. Local safety behavior on a physical node must never depend on WAN availability.

## Evidence boundary

Stage A is completed simulated contract work in `simulation/` and [its guide](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md). Stage B begins only when a physical ESP32-S3 is flashed and observed. Evidence is never promoted across that boundary: simulated MQTT proves software behavior, while physical claims require board, wiring, serial, and measurement evidence.

## Deferred architecture

T01–T07, T09, T14, and N01–N07 remain backlog. They may be designed later, but they are not active dependencies and must not be reported as implemented. See [IoT-first scope](docs/project-management/IOT_FIRST_SCOPE.md) for the authoritative decision record.
