# AFES 2.0 Code Review Worker Protocol

## Purpose

Every Pull Request is reviewed before its owner decides whether to merge. The review worker is an independent quality gate: it inspects the actual diff, relevant tests, CI evidence, architecture and security boundaries. It does not replace the repository owner's decision or grant itself merge authority.

## Required review flow

1. A contributor or implementation worker opens one Pull Request for one linked GitHub Issue.
2. The coordinator assigns a dedicated Code Review Worker before requesting a merge decision.
3. The review worker records findings by severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `INFORMATIONAL`.
4. The implementation worker addresses blocking findings on the same Pull Request and reruns the relevant checks.
5. The review worker verifies the final diff, CI status, Issue linkage, scope, tests, secret hygiene and evidence claims.
6. Only `Huyhuy225`, as repository owner, decides whether to merge after the review result is acceptable and branch protection requirements are met or an owner bypass is deliberately used.

## Work tracker ownership rule

`WORK_TRACKER.md` is the canonical execution record. The `Tracker Ownership Gate` verifies that a Pull Request changing this file was opened by `Huyhuy225`.

- Other team members and workers must report status, evidence and blockers in their assigned Issue or Pull Request.
- They must not include `WORK_TRACKER.md` in their implementation Pull Requests.
- After review is accepted, `Huyhuy225` opens or updates a focused tracker Pull Request with the evidence links and accurate status.
- An open Pull Request or passing CI is not `DONE`; the tracker is updated only after merge and applicable quality gates pass.

## Review evidence checklist

- Linked Issue, correct target branch and bounded scope.
- Actual source/diff review, not README-only claims.
- Relevant automated tests, build/lint output and CI result.
- No secrets, credentials, unsafe defaults or unauthorized dependency changes.
- Simulation, deployment and physical-hardware evidence labelled accurately.
- Documentation and contract compatibility where the change affects them.

## Limits

The review worker can identify risk and recommend changes, but it cannot certify untested hardware, validate private CoreIOT configuration, or approve a merge on behalf of the owner.
