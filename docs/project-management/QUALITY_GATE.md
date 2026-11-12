# Quality gate

## Gate 1 — Repository

- `git diff --check` passes.
- Active Markdown links resolve.
- Repository Hygiene CI passes.
- Tracker Ownership Gate passes when `WORK_TRACKER.md` changes.
- No secrets or untracked environment files are committed.

## Gate 2 — Stage A simulator

- Deterministic tests and fixtures pass as documented in [the simulator guide](../testing/STAGE_A_TELEMETRY_SIMULATOR.md).
- Payloads conform to the [telemetry schema](../TELEMETRY_SCHEMA.md).
- Evidence is labelled `SIMULATION` and makes no board/sensor claim.

## Gate 3 — Local Gateway T08

- Valid payloads forward; invalid payloads fail safely.
- Message IDs support deduplication.
- Buffer bounds, disconnect, reconnect, and ordered replay are tested.
- CLI and health/status endpoint expose operational state without secrets.
- Command authorization and unsafe-command rejection are tested.

## Gate 4 — CoreIOT T11–T13

- Sanitized exports import into the authorized project.
- Widgets bind to the documented keys and distinguish evidence mode.
- RuleChain trigger and no-trigger cases pass.
- Alarm creation, acknowledgement, clearing, and configured notification delivery are recorded.

## Gate 5 — T15 synchronization

- Gateway/device identity remains stable across reconnect.
- Offline telemetry replays once and in order.
- Status and authorized command round trips are correlated.
- Credentials do not appear in logs, exports, or screenshots.

## Gate 6 — Physical ESP32-S3

- Reproducible PlatformIO build and physical flash succeed.
- Board model, commit, serial boot log, and live MQTT observation are recorded.
- Evidence is labelled `PHYSICAL HARDWARE`; simulation cannot substitute.

A task becomes `DONE` only after its applicable gates pass and evidence is merged. See [IOT_FIRST_SCOPE.md](IOT_FIRST_SCOPE.md).
