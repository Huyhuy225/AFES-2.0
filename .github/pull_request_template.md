## Linked Issue
<!-- Specify the issue closed by this PR, e.g., Closes #1 -->
Closes #

## Course Requirement ID
<!-- Specify relevant course requirement ID(s), e.g., T01 through T15, or N/A (DevOps/Governance) -->
- Course ID:

## Summary
<!-- Provide a concise summary of the changes introduced in this PR -->

### Scope of Changes
-

### Change Type
- [ ] Feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Documentation (`docs`)
- [ ] Refactoring (`refactor`)
- [ ] Test addition/update (`test`)
- [ ] Build / CI / Chore (`chore` / `ci`)

## Testing & Validation
<!-- Detail the validation performed. Explicitly separate Simulation from Physical Hardware validation. -->

### 1. Simulation Validation
- **Simulation Method/Tools**: (e.g., mock telemetry publisher, local broker, automated test runner)
- **Commands Executed**:
  ```bash
  # paste simulation command here
  ```
- **Exit Status & Results**:

### 2. Physical Hardware Validation
- **Hardware Used**: (e.g., ESP32 board, sensor models, or N/A if pure software/documentation)
- **Bench Setup**:
- **Commands & Observations**:
  ```bash
  # paste hardware test command here
  ```
- **Exit Status & Results**:

### 3. Repository Hygiene Checks
- [ ] `git diff --check` passed cleanly (no trailing whitespace or whitespace errors).
- [ ] YAML/syntax validation passed (where applicable).

## Screenshots, Diagrams, or Logs (when relevant)
<!-- Attach terminal output, serial monitor traces, diagrams, or UI captures. Ensure all credentials/keys are redacted! -->
```text

```

## Pre-Submission Checklist
- [ ] This PR strictly targets the `develop` branch.
- [ ] The branch follows naming conventions (`<type>/<issue-number>-<description>` or assigned Orca branch).
- [ ] Only authorized files within scope were modified; no unrelated files or generated artifacts were committed.
- [ ] No hardcoded secrets, production passwords, or API keys are committed (checked `.env.example` placeholders only).
- [ ] Code follows project conventions and passes repository hygiene checks.
- [ ] Appropriate CODEOWNERS are tagged for review (@Huyhuy225).
