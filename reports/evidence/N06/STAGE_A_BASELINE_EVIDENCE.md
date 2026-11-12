# AFES 2.0 – Requirement N06 Evidence Report: Frontend Monitoring Baseline

> **Requirement ID**: Advanced Bonus Feature **N06** (Custom-designed dashboard able to detect and record events)
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Lead**: Ý ([@gutjmosnin](https://github.com/gutjmosnin)) – Role 3: Frontend Engineering
> **Verification Stage**: **Stage A (Virtual Simulation & Contract Verification)**
> **Date**: 2026-11-12
> **Status**: Verified & Tested Baseline

---

## 1. Executive Summary

This evidence artifact documents the implementation and automated verification of the **AFES 2.0 React + Vite Monitoring Dashboard Baseline** for Issue #8.

The dashboard fulfills HCMUT course requirement **N06** by providing:
1. An interactive spatial overview of facility zones with real-time fire safety status (`NORMAL`, `WARNING`, `CRITICAL`).
2. Edge sensing fleet telemetry and node diagnostic metrics (RSSI, uptime, TinyML inference latency, sensor health).
3. Live and historical time-series environmental trends (temperature, smoke PPM, humidity).
4. An emergency alarm triage interface with operator acknowledgment (`POST /api/v2/alarms/{id}/acknowledge`) and resolution tracking.
5. An emergency actuator override console (`PUMP_ON`, `PUMP_OFF`, `TEST_ALARM`, `RESET_ALERTS`, `EMERGENCY_SHUTDOWN`) with confirmation safety gates.
6. A Stage A Simulation Scenario injector (`FIRE_SPIKE_ZONE_101`) for interactive verification of fire bursts and dashboard responsiveness without physical fire risk.
7. Strict preservation of the backend API boundary (`/api/v2`) and the Zero-Trust CoreIOT Credential Boundary (zero credentials or direct CoreIOT access tokens in browser code).

---

## 2. Automated Test Execution Evidence

All 26 unit and component integration tests execute cleanly with 100% pass rate:

```text
> afes-frontend@2.0.0 test
> vitest run

 RUN  v5.1.0 D:/orca/workspaces/AFES 2..0/feature-frontend-monitoring-baseline/frontend

 ✓ src/tests/security.test.jsx (2 tests) 14ms
 ✓ src/tests/apiClient.test.jsx (7 tests) 1099ms
 ✓ src/tests/ZoneCard.test.jsx (2 tests) 59ms
 ✓ src/tests/AlarmTriage.test.jsx (3 tests) 71ms
 ✓ src/tests/ControlConsole.test.jsx (3 tests) 90ms
 ✓ src/tests/DeviceList.test.jsx (4 tests) 130ms
 ✓ src/tests/Dashboard.test.jsx (5 tests) 586ms

 Test Files  7 passed (7)
      Tests  26 passed (26)
   Start at  13:22:15
   Duration  3.97s
```

### 2.1. Test Coverage Scope
* `Dashboard.test.jsx`: Header, branding, `[SIMULATED - STAGE A]` tag, KPI metric summary, tab switching, and live/mock toggle.
* `ZoneCard.test.jsx`: Dynamic zone status mapping (`NORMAL`, `WARNING`, `CRITICAL`), threshold warnings, and actuator state chips.
* `DeviceList.test.jsx`: Fleet filtering (`ALL`, `ONLINE`, `OFFLINE`, `FAULT`), search queries, and empty states.
* `AlarmTriage.test.jsx`: Alarm severity tagging, trigger parameter extraction, and operator acknowledgment flow.
* `ControlConsole.test.jsx`: Manual command dispatch, confirmation modal, and simulation scenario injector.
* `apiClient.test.jsx`: REST client data handling, in-memory mock store reactivity, and side-effect updates.
* `security.test.jsx`: Zero-Trust CoreIOT invariant test: rejects illegal CoreIOT token headers and verifies that no credentials exist in source files.

---

## 3. Linter and Production Build Evidence

### 3.1. ESLint Hygiene Check
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
dist/index.html                   0.96 kB │ gzip:   0.50 kB
dist/assets/index-CdR9BjvO.css   22.13 kB │ gzip:   4.61 kB
dist/assets/icons-B4zFa6DJ.js    23.16 kB │ gzip:   6.65 kB
dist/assets/index-G_WiWLOQ.js    48.41 kB │ gzip:  12.93 kB
dist/assets/charts-CqdnxUHx.js  542.93 kB │ gzip: 155.33 kB
✓ built in 3.17s
```

---

## 4. UI State Verification (Loading, Empty, Error)

1. **Loading State**:
   * Verified in `LoadingSkeleton.jsx`. Renders dynamic shimmer card placeholders during asynchronous API loading.
2. **Empty States**:
   * Verified in `EmptyState.jsx`. Rendered when:
     * There are zero active alarms ("All Systems Nominal").
     * Device search returns 0 matching results ("No Devices Found").
     * Telemetry stream has no recorded points ("Waiting for Telemetry Feed").
3. **Error State**:
   * Verified in `ErrorBanner.jsx`. Displayed when network connection fails, presenting an explanatory notice with error code and a one-click "Retry" button.

---

## 5. Security & Boundary Verification

* **Zero Committed Secrets**: Verified in `.env.example` (uses safe placeholders only).
* **Zero CoreIOT Credentials**: Verified that no CoreIOT platform credentials or admin tokens reside in frontend source code. All browser traffic is mediated strictly by Spring Boot `/api/v2`.
* **Platform Independence**: Fulfills N06 without implementing CoreIOT platform dashboards (T11).
