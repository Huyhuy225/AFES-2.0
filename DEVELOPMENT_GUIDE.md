# AFES 2.0 development guide

## Start here

Read [the IoT-first scope](docs/project-management/IOT_FIRST_SCOPE.md), [architecture](ARCHITECTURE.md), [telemetry schema](docs/TELEMETRY_SCHEMA.md), and [work tracker](WORK_TRACKER.md) before opening an implementation change.

The active path is ESP32-S3 nodes → MQTT → Local Gateway → CoreIOT native dashboard/RuleChain/alerts. Do not add layers outside that path unless a later approved scope decision explicitly restores them.

## Local setup

1. Copy `.env.example` to an untracked `.env`.
2. Use placeholder/local-only broker credentials and never commit secrets.
3. Run the Stage A simulator according to [STAGE_A_TELEMETRY_SIMULATOR.md](docs/testing/STAGE_A_TELEMETRY_SIMULATOR.md).
4. Preserve the `simulation.is_simulated` flag through every gateway and CoreIOT mapping.

## Branch and pull request rules

- Branch from current `origin/develop`.
- Keep one issue per pull request where practical.
- Describe scope, dependencies, tests, evidence mode, and remaining limitations.
- Update [WORK_TRACKER.md](WORK_TRACKER.md) only through Huy (`@Huyhuy225`), as enforced by the Tracker Ownership Gate.
- Do not commit real CoreIOT exports containing tokens, `.env` files, broker credentials, certificates, or unredacted screenshots.

## Component gates

### Stage A simulator

Keep the completed `simulation/` implementation hardware-independent and deterministic. Simulator work is labelled `SIMULATION`; it cannot close a physical requirement.

### Local Gateway (T08)

Implement against [#7](https://github.com/Huyhuy225/AFES-2.0/issues/7). Required behaviors are schema validation, stable message IDs, safe buffering/replay, MQTT forwarding, command routing, a CLI, and a small health/status endpoint. Automated tests must cover invalid payloads, duplicates, disconnect/reconnect, and unsafe commands. The operations surface is intentionally minimal and is not a T10 score claim.

### CoreIOT configuration (T11–T13)

Use authorized tenant access from [#3](https://github.com/Huyhuy225/AFES-2.0/issues/3). Export only sanitized configuration. Record imports, widget bindings, RuleChain branches, alarm lifecycle, and notification results. Ý owns T11 configuration evidence; Huy owns onboarding and T12/T13.

### Synchronization (T15)

Implement against [#35](https://github.com/Huyhuy225/AFES-2.0/issues/35). Verify reconnect, ordered replay, deduplication, gateway health, and authorized command round trips without exposing credentials.

### ESP32-S3 foundation

Implement against [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36) only when hardware is available. A reproducible PlatformIO build is necessary but not sufficient: physical completion requires flash, boot, and live MQTT evidence. This foundation does not automatically satisfy T01–T07 or T14.

## Required validation

- Run relevant unit and integration tests.
- Run `git diff --check`.
- Verify all changed internal Markdown links.
- Scan active scope documents for removed architecture claims.
- Keep Repository Hygiene CI and the Tracker Ownership Gate green.

Evidence filenames or reports should state `SIMULATION` or `PHYSICAL_HARDWARE`, identify the commit/configuration under test, record commands and results, and describe limitations.
