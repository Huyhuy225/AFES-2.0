# AFES 2.0: Advanced Fire Emergency System

> **Multi-Node IoT Monitoring, Distributed Edge Intelligence, and Automated Emergency Response**
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Institution**: Ho Chi Minh City University of Technology (HCMUT), VNU-HCM
> **Faculty**: Computer Science and Engineering
> **Lecturer**: Dr. Nguyễn Hòa Hưng

---

## 1. Project Overview

**AFES 2.0 (Advanced Fire Emergency System 2.0)** is a distributed, multi-node emergency sensing, monitoring, and automated suppression platform engineered for modern commercial and institutional facilities.

Building upon an exhaustive baseline audit of the legacy monolithic prototype ([ORIGINAL_AFES_ANALYSIS.md](docs/ORIGINAL_AFES_ANALYSIS.md)), AFES 2.0 introduces an enterprise-grade five-tier architecture. The system combines low-power microcontroller nodes, a resilient edge Local IoT Gateway (as the primary ingestion and control path), the platform-neutral CoreIOT platform, a secure Spring Boot enterprise backend, and a real-time React web operations dashboard.

```
+=============================================================================+
|                      TIER 5: USER PRESENTATION LAYER                         |
|  React 18 + Vite | Tailwind CSS | Chart.js | Real-Time Dashboard UI (N06)   |
+=============================================================================+
        ^                                                    ^
        | REST / JSON (JWT)                                  | WebSocket / STOMP
        v                                                    v
+=============================================================================+
|                 TIER 4: APPLICATION BACKEND (SECURITY FACADE)                |
|  Spring Boot 3.x | Spring Security (RBAC) | MySQL 8.4 | JPA / Hibernate     |
+=============================================================================+
        ^                                                    |
        | REST / WebSocket                                   | MQTT RPC Control
        v                                                    v
+=============================================================================+
|                  TIER 3: COREIOT PLATFORM (PLATFORM-NEUTRAL)                |
|  CoreIOT Cloud / Server (T11 - T15)                                         |
|  - Entity Profiles & Dashboards (T11)  - Automated RuleChain Logic (T12)    |
|  - Threshold Alerts & Alarms (T13)     - Device OTA Package Repo (T14)      |
|  - Gateway Synchronization Hub (T15)   - Mappings Deferred to Issue #3      |
+=============================================================================+
        ^                                                    |
        | MQTT Gateway Telemetry (Primary Path)              | MQTT RPC Downlink
        v                                                    v
+=============================================================================+
|                      TIER 2: LOCAL IOT GATEWAY LAYER                         |
|  Edge Gateway on PC / Raspberry Pi (T08)                                    |
|  - Protocol Adapter (MQTT, ESP-NOW, Modbus, BLE)                            |
|  - Edge AI Event Detection & Sensor Fusion (T09)                            |
|  - Local Monitoring and Control Dashboard UI (T10)                          |
|  - Offline Telemetry SQLite Buffer & CoreIOT Gateway Sync (T15)             |
+=============================================================================+
        ^                      ^                         ^              ^
        | ESP-NOW (T06)        | Modbus RS485 (T02)      | BLE (T03)    | I2C (T01)
        v                      v                         v              v
+=============================================================================+
|                    TIER 1: ESP32-S3 SENSING & ACTUATION NODES               |
|  ESP32-S3 (YoloUNO) FreeRTOS Firmware                                        |
|  - Sensor Interfaces: I2C (T01), Modbus RS485 (T02), BLE (T03)               |
|  - On-Device TinyML Fire Inference Engine (T04)                             |
|  - Local Web Server for Direct Browser Diagnostics (T07)                    |
|  - Actuators: Water Pump Relay, Warning Siren, LED Beacon, Panic Button     |
+=============================================================================+
```

---

## 2. Documentation Index and Architecture Contracts

All technical specifications, contracts, and requirement matrices are fully documented in the following root and `/docs` artifacts:

* **[COURSE_REQUIREMENTS.md](COURSE_REQUIREMENTS.md)**: Official HCMUT Course Project traceability matrix covering all required technology elements (**T01–T15**) and bonus features (**N01–N07**), with points, statuses, owners, test procedures, and completion criteria.
* **[ARCHITECTURE.md](ARCHITECTURE.md)**: Granular architectural blueprint detailing the five system tiers, fail-safe edge autonomy loops, bidirectional RPC command sequences, and Stage A / Stage B separation.
* **[TASK_ASSIGNMENT.md](TASK_ASSIGNMENT.md)**: Team organization, role responsibilities, milestone schedules (timing TBD), multi-agent pairing workflows, and contribution policies.
* **[docs/ORIGINAL_AFES_ANALYSIS.md](docs/ORIGINAL_AFES_ANALYSIS.md)**: Factual technical audit of the original AFES legacy codebase, identifying protocol mismatches, symmetric encryption overhead, reset command defects, and absent course components.
* **[docs/TELEMETRY_SCHEMA.md](docs/TELEMETRY_SCHEMA.md)**: Formal, versioned (v2.0.0) JSON Schema and MQTT topic specifications covering payload envelopes, sensor readings, alarm events, RPC downlinks, simulation markers, and the primary Local Gateway path, with CoreIOT vendor mappings deferred to Issue #3.
* **[docs/API_SPECIFICATION.md](docs/API_SPECIFICATION.md)**: Backend REST and WebSocket API specification defining RBAC expectations, error contracts, spatial zone management, and strict browser isolation from CoreIOT credentials.

---

## 3. Two-Stage Execution Lifecycle

To guarantee rigorous engineering standards and eliminate unverified assumptions, AFES 2.0 enforces a strict two-stage implementation lifecycle (timing TBD):

### Stage A: Virtual Simulation & Contract Validation (Timing TBD)
* **Goal**: Validate end-to-end data pipelines, API contracts, CoreIOT RuleChains, and gateway aggregation using software-simulated sensor nodes.
* **Telemetry Marker**: All Stage A data packets carry `simulation.is_simulated = true`.
* **Verification**: Unit tests, schema validators, mock MQTT brokers, and synthetic fire progression scenarios. No physical hardware claims are made in Stage A.

### Stage B: Physical Deployment & Hardware Verification (Timing TBD)
* **Goal**: Commission physical ESP32-S3 (YoloUNO) boards, wire Modbus RS485 and I2C sensors, deploy Local Gateways on physical PC/Raspberry Pi hardware (`local-gateway/`), and perform live lab measurements.
* **Telemetry Marker**: Real-time production packets carry `simulation.is_simulated = false`.
* **Verification**: Serial console traces, oscilloscope/logic analyzer logs, laboratory smoke chamber tests, and a recorded 5–10 minute demonstration video.

---

## 4. Course Technology Elements Coverage (T01–T15)

The project architecture natively accommodates the full spectrum of required course technology elements, assigned across team members:

| Category | Elements | Target Implementation Tier | Assigned Lead |
|---|---|---|---|
| **Group 1: Sensors** | **T01** (I2C / Tasmota), **T02** (Modbus RS485), **T03** (BLE) | Tier 1 (ESP32-S3 Nodes) | Khánh (Firmware & Local Gateway Lead) |
| **Group 2: TinyML** | **T04** (On-Device Inference), **T05** (Training Tooling Pipeline) | Tier 1 (ESP32-S3) & `tools/` | Khánh (Firmware & Local Gateway Lead) |
| **Group 3: Local Comms** | **T06** (ESP-NOW Wireless), **T07** (On-Device Web Server) | Tier 1 (ESP32-S3 Nodes) | Khánh (Firmware & Local Gateway Lead) |
| **Group 4: Local Gateway** | **T08** (PC/Pi Gateway), **T09** (Edge AI), **T10** (Gateway UI) | Tier 2 (`local-gateway/`) | Khánh (Firmware & Local Gateway Lead) |
| **Group 5: CoreIOT Platform** | **T11** (Templates/Dashboards), **T12** (RuleChains), **T13** (Alerts), **T14** (OTA), **T15** (Gateway Sync) | Tier 3 (CoreIOT Platform) | Huy (Arch & Backend Lead) [Issue #3] |
| **Bonus Features** | **N01** (LLM Assistant), **N06** (Custom Event Dashboard), **N07** (Optional Local ThingsBoard) | Tiers 3, 4, 5 | Ý (@gutjmosnin) for UI; Huy for N07 optional bonus |

---

## 5. Security Invariants and Credential Protection

1. **Browser Credential Isolation**: Web browsers and mobile clients communicate exclusively with the Spring Boot backend via JWT tokens. CoreIOT device tokens, gateway tokens, and administrative credentials are never exposed to browser clients.
2. **Zero-Committed Secrets**: Database credentials, private encryption keys, Wi-Fi passwords, and platform tokens are managed exclusively via environment variables and local secret stores. No secrets exist in the git history.
3. **Transport Encryption**: All network communication across untrusted boundaries utilizes TLS 1.3 (HTTPS and MQTTS).

---

## 6. Academic Integrity and Licensing

AFES 2.0 is developed as a course project for Semester 261 at HCMUT.
* The original monolithic prototype code was audited in [ORIGINAL_AFES_ANALYSIS.md](docs/ORIGINAL_AFES_ANALYSIS.md) and attributed in compliance with academic honesty requirements.
* All new contracts, architectural schemas, gateway components, simulation harnesses, and CoreIOT configurations are the original work of the project group.
