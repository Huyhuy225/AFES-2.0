# IoT-first integration plan

## INT-1 — Simulator to gateway

- Producer: completed `simulation/` Stage A source.
- Consumer: T08 Local Gateway [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7).
- Contract: [telemetry schema](../TELEMETRY_SCHEMA.md).
- Tests: valid/invalid payloads, device identity, message deduplication, disconnect, bounded buffer, ordered replay.
- Evidence: `SIMULATION`.

## INT-2 — Gateway to CoreIOT

- Prerequisite: secure onboarding [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3).
- Dashboard: T11 [#33](https://github.com/Huyhuy225/AFES-2.0/issues/33).
- Rules/alarms: T12/T13 [#34](https://github.com/Huyhuy225/AFES-2.0/issues/34).
- Tests: authenticated publish, device mapping, widget updates, trigger/no-trigger branches, alarm create/acknowledge/clear, redacted notification delivery.

## INT-3 — Bidirectional synchronization

- Scope: T15 [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35).
- Tests: loss/recovery, ordered replay, duplicate suppression, gateway status, allowed command, rejected command, response correlation.
- Safety: no stale or duplicate command may energize an actuator.

## INT-4 — Physical node when available

- Scope: [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36).
- Replace the simulated producer with a flashed ESP32-S3 while preserving schema and identity rules.
- Evidence changes to `PHYSICAL HARDWARE` only for observations made on the real board.

The gateway operations surface is limited to a CLI and health/status endpoint. Deferred items do not enter these phases without explicit scope approval. See [IOT_FIRST_SCOPE.md](IOT_FIRST_SCOPE.md).
