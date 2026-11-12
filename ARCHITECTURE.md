# AFES 2.0 System Architecture Specification

> **Document Version**: 2.0.0
> **Status**: Approved Architecture Baseline
> **Course Project**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Target Platform**: CoreIOT Server and ESP32-S3 (YoloUNO)
> **Classification**: Multi-Tier Distributed IoT System Architecture

---

## 1. Architectural Vision and Goals

**AFES 2.0 (Advanced Fire Emergency System 2.0)** is an enterprise-grade, multi-node emergency sensing, monitoring, and automated response platform. Evolving from the monolithic legacy prototype audited in [ORIGINAL_AFES_ANALYSIS.md](docs/ORIGINAL_AFES_ANALYSIS.md), AFES 2.0 establishes a robust, highly resilient five-tier architecture designed to meet all technology requirements (T01–T15) of the HCMUT IoT Course Project.

### 1.1. Core Architectural Tenets
1. **Multi-Tier Separation of Concerns**: Strict boundary definition between low-power sensing nodes, edge gateways, cloud IoT platforms, enterprise business logic, and user visualization.
2. **Dual-Stage Lifecycle (Stage A / Stage B)**:
   * **Stage A (Virtual Simulation & Contract Verification)**: Comprehensive end-to-end validation using software-simulated sensor nodes, mock telemetry injectors, virtual CoreIOT rule chains, and containerized gateways before hardware commitment.
   * **Stage B (Physical Deployment & Hardware Verification)**: Deployment to physical ESP32-S3 (YoloUNO) boards, Modbus RS485 and I2C sensors, BLE peripherals, PC/Raspberry Pi Local Gateways, and live lab testing.
3. **Fail-Safe Edge Autonomy**: Local safety loops operate independently at Tier 1 (ESP32) and Tier 2 (Local Gateway), guaranteeing that fire suppression and siren activation execute autonomously even during complete cloud or network disconnections.
4. **Zero-Trust CoreIOT Credential Boundary**: Web browsers never interact directly with CoreIOT using administrative or platform credentials; all client interactions are mediated by the Spring Boot application backend.

---

## 2. Five-Tier System Architecture

The following diagram illustrates the five structural tiers of AFES 2.0 and their inter-tier protocols:

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
|  - Zone / Room Topology Management     - Actuator RPC Command Mediation     |
|  - Audit Log & Event Store             - CoreIOT Ingestion Bridge           |
+=============================================================================+
        ^                                                    |
        | REST / WebSocket                                   | MQTT RPC Control
        v                                                    v
+=============================================================================+
|                  TIER 3: COREIOT PLATFORM (THINGSBOARD ENGINE)              |
|  CoreIOT Cloud / Server (T11 - T15)                                         |
|  - Entity Profiles & Dashboards (T11)  - Automated RuleChain Logic (T12)    |
|  - Threshold Alerts & Alarms (T13)     - Device OTA Package Repo (T14)      |
|  - Gateway Synchronization Hub (T15)                                        |
+=============================================================================+
        ^                                                    |
        | MQTT Gateway Telemetry                             | MQTT RPC Downlink
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
|  - Wireless Mesh / Peer Communication via ESP-NOW (T06)                     |
|  - Actuators: Water Pump Relay, Warning Siren, LED Beacon, Panic Button     |
|  - Over-The-Air (OTA) Firmware Client (T14)                                 |
+=============================================================================+
```

---

## 3. Granular Tier Specifications

### 3.1. Tier 1: ESP32-S3 Sensing and Actuation Nodes
* **Microcontroller Target**: Espressif ESP32-S3 (YoloUNO development board), dual-core Xtensa LX7 @ 240 MHz, 512 KB SRAM, 8 MB Flash.
* **Firmware Runtime**: FreeRTOS multi-tasking architecture written in modern C++ with PlatformIO.
* **Sensor Subsystems**:
  * **T01 (I2C on Tasmota / C++)**: Temperature and humidity sensing via DHT20 / SHT30 over I2C bus.
  * **T02 (Modbus RS485)**: Industrial environmental sensing via MAX485 transceiver over UART using Modbus RTU master protocol.
  * **T03 (Bluetooth Low Energy - BLE)**: BLE client service reading remote wireless peripheral sensors.
  * **Analog Front-End**: MQ-2 gas/smoke sensor and optical flame sensor sampled via calibrated ESP32-S3 ADC with software moving-average filtering.
* **Local Intelligence & Networking**:
  * **T04 (On-Device TinyML)**: Quantized neural network (TensorFlow Lite Micro) executing inference directly on the ESP32-S3 to distinguish true fire smoke from transient cooking vapors or dust.
  * **T06 (ESP-NOW)**: Low-latency peer-to-peer wireless packet transmission connecting edge nodes directly to the Local Gateway without Wi-Fi router dependency.
  * **T07 (On-Device Web Server)**: Embedded lightweight HTTP server serving local diagnostic metrics and emergency manual overrides directly over softAP / LAN.
* **Actuation**: Relay output for water pump motor, PWM acoustic buzzer driver, visual strobe LED.
* **Failsafe Logic**: Hardware emergency pushbutton (`vTaskButton`) triggers hardwired override independently of microcontroller CPU state.

### 3.2. Tier 2: Local IoT Gateway (PC / Raspberry Pi)
* **Execution Environment**: Runs on a local industrial PC or Raspberry Pi 4/5 located in the facility.
* **Core Responsibilities (T08)**:
  * Ingests local telemetry from disparate edge protocols: ESP-NOW (via dedicated USB transceiver), Modbus RS485 (via USB-to-RS485 adapter), BLE, and local MQTT.
  * Translates heterogeneous inputs into the unified [AFES 2.0 Telemetry Schema](docs/TELEMETRY_SCHEMA.md).
  * Buffers outgoing packets in a local embedded database (SQLite) during wide-area network outages, executing replay upon reconnection.
* **Edge Artificial Intelligence (T09)**:
  * Multi-sensor spatial fusion model running on the gateway CPU/GPU.
  * Correlates thermal gradients, smoke rise rates, and flame signals across multiple adjacent rooms to detect flashovers and suppress false alarms.
* **Local Operations Interface (T10)**:
  * Self-contained web or desktop dashboard served directly by the gateway.
  * Enables building maintenance personnel to monitor rooms and command actuators locally during Internet disconnection.
* **CoreIOT Synchronization Client (T15)**:
  * Maintains an authenticated gateway session with the CoreIOT platform via MQTT, synchronizing device states, attributes, and bidirectional RPC commands.

### 3.3. Tier 3: CoreIOT Platform (ThingsBoard Engine)
* **Hosting**: Cloud or dedicated server running the HCMUT CoreIOT platform instance.
* **Application Templates & Dashboards (T11)**:
  * Centralized device profiles for `ESP32-S3-Node` and `AFES-Local-Gateway`.
  * Multi-tenant dashboards featuring 2D facility floorplans, real-time gauges, historical trend charts, and RPC control action widgets.
* **RuleChain Engine (T12)**:
  * Configurable event processing graph:
    * Ingestion node $\to$ Schema validation filter $\to$ Threshold evaluation.
    * Fire detection $\to$ Trigger alarm creation $\to$ Push notification $\to$ Initiate downlink RPC.
* **Threshold Alarm Dispatcher (T13)**:
  * Automatically creates `CRITICAL` alarms when temperature $> 50^\circ\text{C}$, smoke $> 500\text{ PPM}$, or flame is detected.
  * Dispatches alert webhooks and notifications.
* **Firmware OTA Management (T14)**:
  * Serves as the central repository for compiled binary firmware packages.
  * Orchestrates version tracking, delta updates, and triggers remote OTA updates to target ESP32 devices via CoreIOT OTA protocols.
* **Gateway Synchronization Hub (T15)**:
  * Connects and synchronizes with the Local IoT Gateway, dynamically creating virtual child devices matching physical nodes discovered on the local network.

### 3.4. Tier 4: Application Backend (Security and Business Facade)
* **Technology**: Java 17+, Spring Boot 3.x, Spring Security 6.x, Spring Data JPA, Hibernate, MySQL 8.4.
* **Security Perimeter**:
  * Acts as the single entry point for web browser and external application traffic.
  * Enforces JWT authentication and Role-Based Access Control (`ROLE_ADMIN`, `ROLE_OPERATOR`, `ROLE_VIEWER`, `ROLE_GATEWAY`).
  * **Strictly isolates CoreIOT credentials**: Web browser clients never receive CoreIOT access tokens.
* **Domain Model**:
  * Manages facility topology: Campuses, Buildings, Floors, Zones, Rooms, and Device mappings.
  * Immutable Audit Log: Records every administrative override, pump engagement, and user login event.
* **Integration Adapters**:
  * Real-time STOMP/WebSocket server pushing live updates to Tier 5 clients.
  * CoreIOT REST / MQTT client translating administrative commands into CoreIOT RPC actions.

### 3.5. Tier 5: Web Presentation Layer
* **Technology**: React 18, Vite, Tailwind CSS, Chart.js, Lucide React, STOMP/WebSocket client.
* **Operational Capabilities**:
  * **Live Facility Map**: Visual 2D floor plan showing color-coded room safety states (Green = Normal, Orange = Warning, Red = Fire Hazard).
  * **Telemetry Analytics**: High-frequency charts displaying temperature, humidity, and smoke PPM over selectable time horizons.
  * **Emergency Control Console**: Authenticated action triggers for siren testing, water pump manual engagement, emergency evacuation alarm, and system reset.
  * **Alarm Triage Table**: Real-time list of active events with one-click operator acknowledgment and resolution logging.

---

## 4. End-to-End Data and Control Workflows

### 4.1. Telemetry Ingestion Pipeline (Normal Operation)

```
[ESP32 Sensing Node]
       |  (1) ESP-NOW / Modbus RS485 / MQTT Telemetry Packet
       v
[Local IoT Gateway]
       |  (2) Ingest, Validate Schema, Run Edge AI Fusion (T09)
       |  (3) Buffer to Local SQLite
       v
[CoreIOT Platform]
       |  (4) Ingest via Gateway MQTT (T15)
       |  (5) Evaluate RuleChain (T12); Update Telemetry Database
       v
[Spring Boot Backend]
       |  (6) Sync Event / Store Business State
       v  (7) Broadcast over WebSocket (/ws/v2/stream)
[React Web Dashboard]
```

### 4.2. Fire Detection and Autonomous Suppression Loop

```
[Sensors: Temp Spike + Smoke Rise + Flame Detection]
       |
       +---> [ESP32 TinyML / Thresholds] ---> [Autonomous Local Siren & Pump On] (Zero-Latency Safety)
       |
       +---> [Local Gateway Edge AI]      ---> [Local Gateway Alarm & Buzzer On] (T09, T10)
       |
       v  (High-Priority Event Packet)
[CoreIOT RuleChain (T12)]
       |
       +---> [Create CRITICAL Alarm (T13)]
       +---> [Trigger RPC Downlink to Adjacent Node Sirens]
       v
[Backend & Frontend WebSocket]
       |
       +---> [Dashboard Flashes Red Alert Beacon]
       +---> [Operator Acknowledges Alert in Web UI]
```

### 4.3. Manual Actuator Override (Downlink RPC)

```
[Administrator (Frontend)]
       |  (1) Click "Engage Pump" -> POST /api/v2/control/command (JWT)
       v
[Spring Boot Backend]
       |  (2) Validate User Role (ROLE_ADMIN) & Idempotency Key
       |  (3) Write Audit Log Entry
       |  (4) Dispatch RPC Request to CoreIOT / Local Gateway
       v
[Local IoT Gateway / CoreIOT]
       |  (5) Route RPC Request to Target Node
       v
[ESP32 Node (vTaskMqtt / vTaskPump)]
       |  (6) Acquire xOutputMutex; Energize Pump Relay
       |  (7) Publish Command Response: status = SUCCESS (200)
       v
[Frontend receives WebSocket confirmation within 200 ms]
```

---

## 5. Dual-Stage Execution Strategy

AFES 2.0 strictly distinguishes **Stage A (Virtual Simulation)** from **Stage B (Physical Hardware)** to guarantee architectural completeness before physical lab commissioning.

| Dimension | Stage A: Simulation & Virtual Validation | Stage B: Real Hardware Integration |
|---|---|---|
| **Objective** | Validate contracts, APIs, RuleChains, and gateway logic. | Deploy and verify physical sensors, transceivers, and actuators. |
| **Sensing Nodes** | Python / Node.js containerized mock nodes emitting synthetic data. | Physical ESP32-S3 (YoloUNO) boards with real sensors. |
| **Sensor Types** | Mathematical models generating thermal rise, noise, and smoke curves. | Physical DHT20 (I2C), Modbus RS485 sensor, BLE sensor, MQ-2. |
| **Local Gateway** | Gateway service running on developer PC connected to Docker network. | Gateway running on physical PC or Raspberry Pi with physical USB adapters. |
| **Telemetry Marker** | `simulation.is_simulated = true` | `simulation.is_simulated = false` |
| **Actuators** | Virtual relays with logged state transitions and virtual indicators. | Physical relay module, 12V submersible pump, 85dB active buzzer. |
| **Evidence Type** | Simulation logs, Docker test runs, automated contract tests. | Lab measurement tables, oscilloscope/logic analyzer traces, demo video. |

> **IMPORTANT**: No claim of physical hardware verification is made during Stage A. All Stage A test reports must clearly state that data was generated via virtual simulation nodes.

---

## 6. Course Project Requirements (T01–T15) Architectural Mapping

| Technology Element | Layer / Tier | Architectural Implementation |
|---|---|---|
| **T01: Sensor via I2C on Tasmota** | Tier 1 (Node) | DHT20 / SHT30 sensor connected via I2C bus using Tasmota or custom C++ driver. |
| **T02: Sensor via Modbus RS485** | Tier 1 / 2 | MAX485 transceiver interfacing industrial RS485 sensor with Modbus RTU protocol. |
| **T03: Sensor via BLE** | Tier 1 / 2 | ESP32-S3 BLE client subscribing to environmental GATT characteristics. |
| **T04: On-Device TinyML Inference** | Tier 1 (Node) | TensorFlow Lite Micro model running on ESP32-S3 classifying fire probability. |
| **T05: TinyML Tooling & Pipeline** | Tooling | Python scripts for data collection, Google Colab / Edge Impulse training, and C++ array export. |
| **T06: Wireless via ESP-NOW** | Tier 1 $\leftrightarrow$ 2 | Connectionless, low-overhead ESP-NOW protocol transmitting telemetry to Gateway. |
| **T07: On-Device Web Server** | Tier 1 (Node) | Lightweight HTTP/REST server hosted directly on ESP32-S3 for local emergency control. |
| **T08: Local IoT Gateway on PC/Pi** | Tier 2 (Gateway) | Python/Node gateway service aggregating multi-protocol sensor data for CoreIOT. |
| **T09: Edge AI Function on Gateway** | Tier 2 (Gateway) | Multi-sensor spatial fusion and anomaly detection model running on Gateway CPU. |
| **T10: Local Gateway Monitoring UI** | Tier 2 (Gateway) | Dedicated local UI served by Gateway for standalone emergency operations. |
| **T11: CoreIOT Templates & Dashboards** | Tier 3 (CoreIOT) | Device profiles, widgets, and administrative operational dashboards on CoreIOT. |
| **T12: CoreIOT RuleChain Features** | Tier 3 (CoreIOT) | Smart rule chain workflows for automatic threshold checking and RPC dispatch. |
| **T13: Alert Notifications** | Tier 3 (CoreIOT) | Automated email/webhook/SMS alarm triggers dispatched when thresholds are breached. |
| **T14: OTA Firmware Updates** | Tier 3 $\leftrightarrow$ 1 | CoreIOT OTA package distribution delivering encrypted firmware binaries to nodes. |
| **T15: Gateway Synchronization** | Tier 2 $\leftrightarrow$ 3 | Bidirectional synchronization between Local IoT Gateway and CoreIOT Gateway service. |
