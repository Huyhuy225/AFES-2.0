# AFES 2.0 – Requirement N06 Evidence Report: Frontend Monitoring Baseline

> **Requirement ID**: Advanced Bonus Feature **N06** (Custom-designed dashboard able to detect and record events)
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Lead**: Ý ([@gutjmosnin](https://github.com/gutjmosnin)) – Role 3: Frontend Engineering
> **Verification Stage**: **Stage A (Virtual Simulation & Contract Verification)**
> **Date**: 2026-11-12
> **Status**: IN_PROGRESS (Stage A Monitoring Baseline Verified)

---

## 1. Executive Summary & Traceability Status

This evidence artifact documents the implementation and automated verification of the **AFES 2.0 React + Vite Monitoring Dashboard Baseline** for Issue #8.

### 1.1. Traceability Status: `IN_PROGRESS`
In strict alignment with course project evaluation rules and PR #9 review findings:
* **Current Status**: `IN_PROGRESS` (advancing from `DOCUMENTED`).
* **Completed in this Stage A Baseline**:
  1. Responsive React 18 + Vite monitoring dashboard shell adhering to AFES 2.0 contracts and dark NOC theme.
  2. Spatial zone safety cards with real-time status (`NORMAL`, `WARNING`, `CRITICAL`), environmental readings, and actuator indicators.
  3. Sensing fleet diagnostic view with status filtering (`ALL`, `ONLINE`, `OFFLINE`, `FAULT`), RSSI signal, uptime, and TinyML latency.
  4. Real-time and historical time-series environmental telemetry chart (temperature, smoke PPM, warning thresholds).
  5. Emergency alarm triage interface with severity badges, trigger parameters, and operator acknowledgment (`POST /api/v2/alarms/{id}/acknowledge`).
  6. Actuator override console (`PUMP_ON`, `PUMP_OFF`, `TEST_ALARM`, `RESET_ALERTS`, `EMERGENCY_SHUTDOWN`) with confirmation modal and Stage A simulation injector (`FIRE_SPIKE_ZONE_101`).
  7. **Safety Invariant on Mutations**: In explicit live mode (`VITE_USE_MOCK_DATA=false`), failed alarm acknowledgments, resolutions, and control commands never fake success in the in-memory mock store; errors are propagated directly to the UI.
  8. Zero-Trust CoreIOT Credential Boundary: Zero CoreIOT administrative credentials, tokens, or MQTT credentials exist in browser code.
* **Remaining Work for Full N06 Sign-Off (Deferred to Milestone 4)**:
  1. **Persistent Event Recording**: Integration with persistent MySQL event store via Spring Boot backend (`/api/v2/alarms`) and STOMP WebSocket stream (`/topic/alarms`) to record, audit, and correlate historical incidents across sessions.
  2. **Interactive 2D Floorplan Canvas**: Visual 2D floorplan layout with SVG/Canvas spatial room coordinates and zone status glow.
  3. **Backend Fullstack Integration**: Connecting the React dashboard to the live Spring Boot containerized service.

---

## 2. Automated Test Execution Evidence

All 30 unit and component integration tests execute cleanly with a 100% pass rate:

```text
> afes-frontend@2.0.0 test
> vitest run

 RUN  v5.1.0 D:/orca/workspaces/AFES 2..0/feature-frontend-monitoring-baseline/frontend

 ✓ src/tests/security.test.jsx (2 tests) 13ms
 ✓ src/tests/apiClient.test.jsx (10 tests) 1304ms
 ✓ src/tests/ZoneCard.test.jsx (2 tests) 62ms
 ✓ src/tests/AlarmTriage.test.jsx (3 tests) 69ms
 ✓ src/tests/ControlConsole.test.jsx (3 tests) 92ms
 ✓ src/tests/DeviceList.test.jsx (4 tests) 138ms
 ✓ src/tests/Dashboard.test.jsx (6 tests) 697ms

 Test Files  7 passed (7)
      Tests  30 passed (30)
   Duration  3.93s
```

### 2.1. Test Coverage Scope
* `Dashboard.test.jsx`: Header, branding, `[SIMULATED - STAGE A]` tag, KPI metric summary, tab switching, live/mock toggle, and live mutation error handling banner.
* `ZoneCard.test.jsx`: Dynamic zone status mapping (`NORMAL`, `WARNING`, `CRITICAL`), threshold warnings, and actuator state chips.
* `DeviceList.test.jsx`: Fleet filtering (`ALL`, `ONLINE`, `OFFLINE`, `FAULT`), search queries, and empty states.
* `AlarmTriage.test.jsx`: Alarm severity tagging, trigger parameter extraction, and operator acknowledgment flow.
* `ControlConsole.test.jsx`: Manual command dispatch, confirmation modal, and simulation scenario injector.
* `apiClient.test.jsx`: REST client data handling, in-memory mock store reactivity, and **explicit live-mode safety tests ensuring failed mutations (`acknowledgeAlarm`, `resolveAlarm`, `dispatchControlCommand`) throw errors and never mutate mock state to fake success**.
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
Generated an empty chunk: "vendor".
rendering chunks...
computing gzip size...
dist/index.html                   0.96 kB │ gzip:   0.50 kB
dist/assets/index-CVp3i49v.css   22.36 kB │ gzip:   4.65 kB
dist/assets/vendor-l0sNRNKZ.js    0.00 kB │ gzip:   0.02 kB
dist/assets/icons-B4zFa6DJ.js    23.16 kB │ gzip:   6.65 kB
dist/assets/index-CId-oyw9.js    48.38 kB │ gzip:  12.97 kB
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
   * Verified in `ErrorBanner.jsx`. Displayed when network connection fails or live REST mutations reject, presenting an explanatory notice with error code and a one-click "Retry" button.

---

## 5. Security & Boundary Verification

* **Zero Committed Secrets**: Verified in `.env.example` (uses safe placeholders only).
* **Zero CoreIOT Credentials**: Verified that no CoreIOT platform credentials or admin tokens reside in frontend source code. All browser traffic is mediated strictly by Spring Boot `/api/v2`.
* **Platform Independence**: Fulfills N06 Stage A baseline without implementing or claiming CoreIOT platform dashboards (T11).
