# AFES 2.0 – Frontend Monitoring Dashboard Baseline

> **Module**: Tier 5 User Presentation Layer
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Institution**: Ho Chi Minh City University of Technology (HCMUT), VNU-HCM
> **Responsible Lead**: Ý ([@gutjmosnin](https://github.com/gutjmosnin)) – Role 3: Frontend Engineering
> **Course Requirement**: Advanced Bonus Feature **N06** (Custom-designed dashboard able to detect and record events)
> **Target Base**: React 18 + Vite + Vitest

---

## 1. Architectural Scope and Tenets

The **AFES 2.0 Monitoring Dashboard Baseline** implements the Tier 5 presentation layer for real-time sensing, spatial zone safety mapping, hardware device telemetry, emergency alarm triage, and manual actuator overrides.

### 1.1. Core Architectural Tenets
1. **Zero-Trust CoreIOT Credential Boundary**:
   * Web browsers **never** communicate directly with the CoreIOT server using administrative tokens, device access tokens, or platform credentials.
   * All dashboard operations are mediated through the Spring Boot application backend (`/api/v2`).
2. **Preservation of Platform Boundary (N06 vs T11)**:
   * This module fulfills **N06** (Custom-designed dashboard able to detect and record events).
   * It **does not substitute or claim** the separate CoreIOT Platform Dashboard requirement (**T11**), which is configured natively on the CoreIOT tenant.
3. **Dual-Stage Lifecycle (Stage A Virtual Simulation)**:
   * During Stage A, all metrics, edge node health states, and synthetic alerts carry the visual badge `[SIMULATED - STAGE A]` to prevent premature claims of physical hardware integration.
4. **Dual Data Mode & Edge Autonomy**:
   * Operates against live Spring Boot `/api/v2` endpoints when available.
   * Provides an integrated in-browser Stage A mock simulator fallback for standalone testing, emergency drill demonstrations, and offline verification.

---

## 2. Component Hierarchy and Features

```
frontend/
├── index.html                   # HTML entry point with fonts and metadata
├── vite.config.js               # Vite config with manual chunk splitting & Vitest jsdom setup
├── eslint.config.js             # ESLint 9 configuration with React rules
├── package.json                 # Dependencies (React 18, Recharts, Lucide React, Vitest)
├── .env.example                 # Safe environment template with placeholders
└── src/
    ├── contracts/
    │   └── afesContracts.js     # AFES 2.0 system states, thresholds, and event contracts
    ├── api/
    │   ├── sensorApi.js         # Unified REST client with automatic mock fallback
    │   └── mockData.js          # In-memory Stage A synthetic telemetry and scenario store
    ├── components/
    │   ├── Header.jsx           # Global status, Stage A simulation tag, data mode toggle
    │   ├── StatsSummary.jsx     # High-level KPIs: safety status, active alarms, fleet health
    │   ├── ZoneCard.jsx         # Spatial zone card (NORMAL/WARNING/CRITICAL, readings, actuators)
    │   ├── DeviceList.jsx       # Sensing fleet list, RSSI signal, uptime, TinyML latency
    │   ├── AlarmTriage.jsx      # Active alarm triage feed, severity badges, operator Acknowledge
    │   ├── TelemetryChart.jsx   # Interactive time-series trends (Temp °C, Smoke PPM, thresholds)
    │   ├── ControlConsole.jsx   # Actuator command dispatch, safety confirmation, sim injector
    │   ├── LoadingSkeleton.jsx  # Shimmer loading skeleton
    │   ├── EmptyState.jsx       # Clean empty state display
    │   └── ErrorBanner.jsx      # Network error notice with retry action
    ├── pages/
    │   └── Dashboard.jsx        # Main dashboard shell coordinating 5 functional navigation tabs
    ├── tests/
    │   ├── Dashboard.test.jsx   # End-to-end integration test of navigation, states, and polling
    │   ├── ZoneCard.test.jsx    # Unit test of zone safety states and actuator status
    │   ├── DeviceList.test.jsx  # Device filtering, search, and simulation badge assertions
    │   ├── AlarmTriage.test.jsx # Alarm triage workflow, acknowledge and resolve callbacks
    │   ├── ControlConsole.test.jsx # Actuator command dispatch and confirmation modal tests
    │   ├── apiClient.test.jsx   # Unit tests of apiService methods and mock state store
    │   └── security.test.jsx    # Invariant assertion verifying zero CoreIOT secrets
    └── index.css                # Dark slate glassmorphism NOC styling & responsive layout
```

---

## 3. API Contract Endpoints Handled

The dashboard communicates exclusively with the backend REST endpoints defined in [`docs/API_SPECIFICATION.md`](../docs/API_SPECIFICATION.md):

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v2/zones/summary` | `GET` | Real-time safety status, latest readings, and actuator states for all zones |
| `/api/v2/devices` | `GET` | List registered ESP32-S3 sensing nodes with status and zone references |
| `/api/v2/devices/{id}/health` | `GET` | Detailed self-diagnostic metrics (RSSI, uptime, TinyML latency) |
| `/api/v2/telemetry/history` | `GET` | Historical time-series environmental readings for trends chart |
| `/api/v2/alarms/active` | `GET` | Unacknowledged active fire and smoke threshold alarms |
| `/api/v2/alarms/{id}/acknowledge` | `POST` | Operator acknowledgment of active emergency alarm |
| `/api/v2/alarms/{id}/resolve` | `POST` | Resolution of cleared alarms |
| `/api/v2/control/command` | `POST` | Actuator override command dispatch (`PUMP_ON`, `PUMP_OFF`, `TEST_ALARM`, `RESET_ALERTS`, `EMERGENCY_SHUTDOWN`) |

---

## 4. Local Development and Validation

### 4.1. Prerequisites
* Node.js v18+ (tested on v22.16.0)
* npm v9+ (tested on 11.4.1)

### 4.2. Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env
```

### 4.3. Development Server
```bash
npm run dev
# Server starts at http://localhost:3000
```

### 4.4. Quality Checks and Testing
```bash
# Run ESLint validation (0 errors, 0 warnings)
npm run lint

# Run all unit and integration tests with Vitest (26/26 passing)
npm test

# Build production bundle
npm run build
```

---

## 5. Security & Credential Hygiene
* **Zero Secrets Committed**: All environment variables use placeholders in `.env.example`.
* **Zero CoreIOT Credentials**: The browser client does not contain or request CoreIOT admin tokens or MQTT keys.
* **Security Verification**: Automated in `src/tests/security.test.jsx`, which scans the frontend tree to verify no forbidden secret patterns or platform tokens exist.
