# AFES 2.0 code review worker protocol

## Purpose and authority

Every Pull Request is reviewed before the repository owner decides whether to merge. The independent Code Review Worker inspects the actual diff, relevant tests and CI, architecture and contracts, security boundaries, evidence, and issue scope; it does not replace the owner's decision or grant itself approval or merge authority.

Only `Huyhuy225`, as repository owner, decides whether to merge after the review verdict is acceptable and all required checks pass. The review worker must not approve, merge, bypass branch protection, or claim evidence it did not inspect.

## Required review flow

1. Confirm one linked Issue, the correct target branch, and a bounded change that belongs to the [IoT-first scope](IOT_FIRST_SCOPE.md).
2. Inspect the actual changed paths and diff, not only the Pull Request description or README claims.
3. Verify ownership, dependencies, and status against [WORK_TRACKER.md](../../WORK_TRACKER.md), including the simulation-versus-physical evidence boundary.
4. Review source and configuration against the active architecture, telemetry contract, failure handling, rollback expectations, and security rules.
5. Run or independently verify the applicable [quality gates](QUALITY_GATE.md), tests, builds, link checks, secret checks, and exact-head CI results.
6. Record findings as `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `INFORMATIONAL`, with affected paths and a concrete reason.
7. Return one verdict: `APPROVE`, `APPROVE_WITH_NOTES`, or `REQUEST_CHANGES`; the verdict informs but does not replace Huy's merge decision.
8. If blocking findings are fixed, review the new exact head and fresh CI before returning an updated verdict.

## Work tracker ownership rule

`WORK_TRACKER.md` is the canonical execution record. The `Tracker Ownership Gate` verifies that a Pull Request changing it was opened by `Huyhuy225`.

- Other contributors and workers report status, evidence, and blockers in their assigned Issue or Pull Request; they do not submit root tracker changes.
- Passing CI or an open Pull Request is not `DONE`; status changes only after implementation/configuration, tests, evidence, review, and merge satisfy the applicable gate.
- The gate's complete-file-list safeguard remains part of the ownership enforcement and must not be weakened or bypassed.

## Scope-specific checks

- T08: schema validation, bounded buffering, replay, CLI/health status, and command safety.
- T11: native CoreIOT configuration and evidence owned by Ý; planned widgets are not implementation evidence.
- T12/T13: deterministic RuleChain branches, alarm lifecycle, and redacted notification evidence.
- T15: reconnect, deduplication, ordered replay, and state/command correlation.
- Firmware: physical evidence is mandatory for physical claims; generic I2C is not T01 Tasmota.
- Archived web prototype: active changes must not restore custom-web, application-server, database, public-deployment, or server-side REST dependencies without an approved scope decision.

A reviewer may inspect private CoreIOT or hardware evidence only when granted authorized access and must describe the evidence boundary accurately.
