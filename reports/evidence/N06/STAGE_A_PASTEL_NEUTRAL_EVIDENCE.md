# AFES 2.0 – Requirement N06 Evidence Report: Calm Pastel Theme & Neutral Stage A Baseline

> **Requirement ID**: Advanced Bonus Feature **N06** (Custom-designed dashboard able to detect and record events)
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Responsible Lead**: Ý ([@gutjmosnin](https://github.com/gutjmosnin)) – Role 3: Frontend Engineering
> **GitHub Issue**: [Issue #12](https://github.com/Huyhuy225/AFES-2.0/issues/12)
> **Verification Stage**: **Stage A (Virtual Simulation & Contract Verification Only)**
> **Date**: 2026-11-12
> **Status**: IN_PROGRESS (Stage A Simulation Refinement Verified)

---

## 1. Executive Summary & Scope

In response to operator design feedback, this iteration refines the Stage A frontend monitoring baseline:
1. **Neutral Default Stage A Mock State**:
   - Initial load starts with zero active alarms (`alarms = []`).
   - All 4 facility zones (`ZONE-101`, `ZONE-102`, `ZONE-103`, `ZONE-104`) start in `SYSTEM_STATES.NORMAL` with safe environmental metrics (temperature ~21–24°C, humidity ~44–52%, smoke 18–45 PPM, flame detection clear, TinyML fire confidence ≤0.05).
   - Global system safety status displays `NORMAL` ("All monitored sectors nominal").
   - Actuators start in safe standby (`pump_active: false`, `buzzer_active: false`).
2. **Intentional, Labellable Simulation Scenarios**:
   - Explicit controls in the Actuator Controls tab allow operators to inject simulated incidents on demand:
     - `WARNING_SMOKE_ZONE_102`: Injects a smoke threshold warning into Zone 102 (535 PPM) with `[SIMULATED - STAGE A]` metadata.
     - `FIRE_SPIKE_ZONE_101`: Injects a critical multi-sensor fire alarm into Zone 101 (75°C + flame detected + 885 PPM smoke).
   - Prominent, non-intrusive scenario banner displays `[SIMULATED - STAGE A] Active Scenario: ...` across tabs.
   - 100% reversible: An instant "Reset to Neutral Baseline" control returns the entire state store back to neutral.
3. **Calm, Light, Pastel, Low-Glare Visual System**:
   - Replaced dark glassmorphism, heavy neon glows, and dark backgrounds with a soft Slate-50 background (`#f8fafc`), clean white card panels (`#ffffff`), and gentle border definitions (`#e2e8f0`).
   - Accessible, semantic safety indicators (not color-only):
     - **NORMAL**: Pastel Sage/Emerald (`#ecfdf5` background, `#a7f3d0` border, `#065f46` text) with `CheckCircle2` icon and "NORMAL" label.
     - **WARNING**: Pastel Amber (`#fffbeb` background, `#fde68a` border, `#92400e` text) with `AlertTriangle` icon and "WARNING" label.
     - **CRITICAL**: Pastel Rose/Coral (`#fef2f2` background, `#fecaca` border, `#991b1b` text) with `Flame` icon and "CRITICAL / FIRE ALARM" label.
   - High text contrast complying with WCAG AA/AAA standards.
4. **Safety Invariant on Mutations Preserved**:
   - In explicit live mode (`VITE_USE_MOCK_DATA=false`), failed live mutations (`acknowledgeAlarm`, `resolveAlarm`, `dispatchControlCommand`) propagate errors directly and strictly never mutate mock state to simulate false success.

---

## 2. Automated Test Suite Execution Evidence

All 33 unit and component integration tests execute cleanly with a 100% pass rate:

```text
> afes-frontend@2.0.0 test
> vitest run

 RUN  v5.1.0 D:/orca/workspaces/AFES 2..0/feature-y-pastel-neutral-simulation/frontend

 ✓ src/tests/security.test.jsx (2 tests) 16ms
 ✓ src/tests/ControlConsole.test.jsx (3 tests) 96ms
 ✓ src/tests/ZoneCard.test.jsx (2 tests) 62ms
 ✓ src/tests/AlarmTriage.test.jsx (3 tests) 70ms
 ✓ src/tests/DeviceList.test.jsx (4 tests) 132ms
 ✓ src/tests/apiClient.test.jsx (11 tests) 1638ms
 ✓ src/tests/Dashboard.test.jsx (8 tests) 1178ms

 Test Files  7 passed (7)
      Tests  33 passed (33)
   Duration  4.52s
```

### 2.1. Coverage of Added & Updated Tests
* `Dashboard.test.jsx`:
  - `renders calm neutral default Stage A state with no active alarm/warning and all normal zones`: Verifies that initial render displays 0 active alarms, global status `NORMAL` ("All monitored sectors nominal"), all 4 zone cards marked `NORMAL`, and empty alarm triage state ("All Systems Nominal").
  - `injects deliberate simulation incident with visible [SIMULATED - STAGE A] tag and reversible reset`: Verifies control console injection of simulated critical fire, appearance of `[SIMULATED - STAGE A]` scenario banner, transition of KPI status to `CRITICAL`, and reversible reset back to neutral baseline.
  - `handles alarm acknowledgment workflow cleanly`: Verifies operator acknowledgment and resolution flow on an injected alarm.
  - `displays error banner when live alarm acknowledgment fails without simulating success`: Verifies safety invariant under mutation error conditions.
* `apiClient.test.jsx`:
  - `verifies neutral default alarm state and acknowledges an injected alarm`: Verifies `getActiveAlarms()` initially returns 0 items, then acknowledges a simulated alarm.
  - `triggers simulation warning scenario and verifies warning state in zone 102`: Verifies warning injection and clean reversible reset.
  - Strict live-mode mutation safety tests: Confirms failed `acknowledgeAlarm`, `resolveAlarm`, and `dispatchControlCommand` calls never fake success in mock store.
* `ControlConsole.test.jsx`:
  - Tests simulated warning and critical scenario start buttons and reset callback.

---

## 3. Linter, Production Build, and Git Cleanliness Evidence

### 3.1. ESLint Check
```text
> afes-frontend@2.0.0 lint
> eslint .

Exit code: 0 (0 errors, 0 warnings)
```

### 3.2. Vite Production Build
```text
> afes-frontend@2.0.0 build
> vite build

vite v6.4.6 building for production...
transforming...
✓ 2018 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.98 kB │ gzip:   0.51 kB
dist/assets/index-Zc5nJKhC.css   26.33 kB │ gzip:   4.79 kB
dist/assets/vendor-l0sNRNKZ.js    0.00 kB │ gzip:   0.02 kB
dist/assets/icons-B4zFa6DJ.js    23.16 kB │ gzip:   6.65 kB
dist/assets/index-CWETnOj6.js    49.95 kB │ gzip:  13.21 kB
dist/assets/charts-CqdnxUHx.js  542.93 kB │ gzip: 155.33 kB
✓ built in 6.75s
Exit code: 0
```

### 3.3. Git Whitespace Hygiene
```text
$ git diff --check
Exit code: 0 (no whitespace errors or merge markers)
```

### 3.4. Local Preview Verification
* Preview server started on port 4173 (`npx vite preview --port 4173`).
* HTTP GET `http://localhost:4173/` returned HTTP 200 OK with correct application shell.

---

## 4. Architectural Boundaries & Traceability Notice

* **Simulation Only**: All validations in this PR are Stage A simulation-only. No live CoreIOT hardware, MQTT brokers, or production credentials were used.
* **No Contract Mutations**: Telemetry contracts (`docs/TELEMETRY_SCHEMA.md`), REST API specification (`docs/API_SPECIFICATION.md`), backend gateway code, and root governance documents remain unmodified.
