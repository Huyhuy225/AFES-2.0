# Review protocol

## Required review flow

1. Confirm the change belongs to the [IoT-first scope](IOT_FIRST_SCOPE.md) and its issue.
2. Verify ownership, dependencies, and status against [WORK_TRACKER.md](../../WORK_TRACKER.md).
3. Review source/configuration and run the relevant [quality gate](QUALITY_GATE.md).
4. Check that each artifact is labelled `SIMULATION` or `PHYSICAL HARDWARE`.
5. Check links, secret hygiene, failure handling, and rollback notes.
6. Reject unsupported completion or score claims.

## Scope-specific checks

- T08: schema validation, bounded buffering, replay, CLI/health status, command safety.
- T11: native CoreIOT configuration and evidence owned by Ý.
- T12/T13: deterministic rule branches, alarm lifecycle, redacted notifications.
- T15: reconnect, deduplication, ordered replay, state/command correlation.
- Firmware: physical evidence is mandatory for physical claims; generic I2C is not T01 Tasmota.

Only Huy may submit root tracker changes. A reviewer may verify private CoreIOT or hardware evidence when granted access, but must not claim to have observed evidence they did not actually inspect.
