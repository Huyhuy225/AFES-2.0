# Handover protocol

Every handover must identify the issue, owner, dependency state, commit/configuration version, evidence mode, commands/tests run, results, known limitations, and next safe action.

## Required package

1. Link the active issue and pull request.
2. List changed source/configuration paths.
3. State `SIMULATION` or `PHYSICAL HARDWARE` for every evidence artifact.
4. Provide sanitized configuration exports and reproducible commands.
5. Record failures and blockers; do not convert plans into completion claims.
6. Confirm no credentials, tokens, private URLs, or unredacted tenant data are present.

## Component notes

- Gateway handovers include broker assumptions, schema version, buffer format, replay semantics, CLI/health contract, and unsafe-command behavior.
- CoreIOT handovers include tenant-neutral names, device/gateway mapping, dashboard/RuleChain import steps, alarm thresholds, and rollback steps.
- Firmware handovers include board model, PlatformIO environment, build/flash command, pin map, serial log, and actual hardware used.

Khánh’s GitHub activation remains pending; if assignment automation fails, record ownership explicitly rather than reassigning the technical work. See [IOT_FIRST_SCOPE.md](IOT_FIRST_SCOPE.md) and [QUALITY_GATE.md](QUALITY_GATE.md).
