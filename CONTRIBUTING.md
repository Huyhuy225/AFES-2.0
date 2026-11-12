# AFES 2.0 contributing and repository governance

AFES 2.0 is an IoT-first course project. Active contributions follow this product path:

```text
ESP32-S3 nodes -> MQTT -> Local Gateway (PC/Raspberry Pi) -> CoreIOT
                                                        -> native dashboard
                                                        -> RuleChain and alarms
```

Read the authoritative [IoT-first scope](docs/project-management/IOT_FIRST_SCOPE.md), [architecture](ARCHITECTURE.md), [development guide](DEVELOPMENT_GUIDE.md), and [work tracker](WORK_TRACKER.md) before starting work.

## 1. Active and archived scope

Active contribution areas are:

- the hardware-independent Stage A simulator and telemetry contract;
- the T08 Local Gateway, including its minimal CLI and health/status endpoint;
- secure CoreIOT onboarding and native T11–T13 configuration;
- T15 gateway/CoreIOT synchronization; and
- the ESP32-S3 PlatformIO foundation when physical hardware is available.

The earlier custom web dashboard, application-server design, database-service plan, public-deployment concept, server-side REST specification, and N06 evidence are archived on [`archive/web-application-prototype`](https://github.com/Huyhuy225/AFES-2.0/tree/archive/web-application-prototype). They are not active assignments or dependencies and must not be restored to `develop` without an explicitly approved scope decision.

T10 is not currently claimed for scoring. T01–T07, T09, T14, and N01–N07 remain deferred until explicitly approved with a dedicated Issue, owner, dependency, acceptance test, and evidence mode.

## 2. Core governance principles

### Pull-request-only workflow

- Do not push directly to `main` or `develop`.
- Branch day-to-day work from the current `develop` baseline and target `develop` with the Pull Request.
- Reserve `main` for stable milestone or release Pull Requests from `develop`.
- Link every Pull Request to a tracked GitHub Issue and identify the relevant course requirement or `N/A (Governance/DevOps)`.
- Keep one well-defined task per Pull Request and change only authorized paths.

### Branch naming

Use one of these forms:

```text
<type>/<issue-number>-<short-description>
<username>/<task-slug>  # assigned Orca worktree branches
```

Approved types include `feat`, `fix`, `docs`, `chore`, `refactor`, and `test`. Use lowercase alphanumeric words separated by hyphens.

### Commit messages

Use Conventional Commits:

```text
<type>(<scope>): <short imperative description>

[optional explanation]

[optional footer, for example: Closes #7]
```

Do not commit generated build output, real `.env` files, credentials, private exports, or unrelated changes.

## 3. Pull Request lifecycle

1. Confirm the Issue, owner, dependencies, status, and acceptance evidence in [WORK_TRACKER.md](WORK_TRACKER.md) and the relevant task document.
2. Create or use the assigned branch from current `develop`.
3. Implement only the active IoT-first task and preserve the telemetry and evidence-mode contracts.
4. Run the applicable [quality gates](docs/project-management/QUALITY_GATE.md), including `git diff --check`, relevant tests, link checks, and secret hygiene.
5. Open a Pull Request targeting `develop` with `Closes #<issue-number>`, exact commands/results, limitations, and evidence labelled `SIMULATION` or `PHYSICAL HARDWARE`.
6. An independent Code Review Worker reviews the actual diff, CI, security, contracts, and evidence under the [review protocol](docs/project-management/REVIEW_PROTOCOL.md) and returns a severity-based verdict.
7. Address blocking findings on the same Pull Request and rerun the applicable checks.
8. Only `Huyhuy225`, as repository owner, decides whether to squash-merge after the verdict and required checks are acceptable; contributors and review workers must not self-merge or bypass protection.

## 4. Ownership

- Huy (`@Huyhuy225`): repository governance, CoreIOT onboarding, T12/T13, T15 integration, and final reporting.
- Khánh (`@tranhoangkhanh-hkt`): T08 Local Gateway and ESP32-S3 firmware foundation; repository activation remains pending until access is available.
- Ý (`@gutjmosnin`): T11 native CoreIOT device-template/dashboard configuration and evidence.

The authoritative reviewer mapping is `.github/CODEOWNERS`, which currently retains `@Huyhuy225` as the enforceable fallback owner while collaborator activation is pending. Do not infer repository permissions from documented technical ownership.

`WORK_TRACKER.md` is owner-controlled. Only Huy may submit changes to it, as enforced by the `Tracker Ownership Gate`; other contributors report evidence and status in their Issue or Pull Request.

## 5. Security and secrets

- Never commit CoreIOT credentials, device tokens, MQTT passwords, private keys, certificates, real `.env` files, private tenant URLs, or unredacted exports/screenshots.
- Keep only safe placeholders in `.env.example`; load real values from an untracked local environment.
- Use least-privilege credentials and TLS for non-local authenticated connections.
- Preserve `simulation.is_simulated` through every gateway and CoreIOT mapping so synthetic data cannot impersonate physical evidence.
- If a secret is exposed, notify Huy immediately, revoke and rotate it, and follow the repository incident procedure before further distribution.

## 6. Evidence and testing

- `SIMULATION` evidence may prove contracts, validation, routing, retry behavior, native dashboard bindings, and RuleChain logic using synthetic inputs.
- `PHYSICAL HARDWARE` claims require the real ESP32-S3, attached interfaces, reproducible build/flash details, and observed output.
- Simulator output cannot prove board flashing, sensors, electrical interfaces, radio behavior, or physical actuation.
- Planned paths, Issue text, configuration sketches, or screenshots alone do not make a task `DONE`.
- A task becomes `DONE` only after its implementation/configuration, applicable tests, labelled evidence, independent review, and merge satisfy the active quality gate.

Use `.github/pull_request_template.md` for the submission checklist and [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) for component-specific commands and acceptance criteria.
