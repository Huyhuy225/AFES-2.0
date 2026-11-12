# AFES 2.0 Course Requirements and Traceability Matrix

> **Institution**: Ho Chi Minh City University of Technology (HCMUT), VNU-HCM
> **Faculty**: Computer Science and Engineering
> **Course**: Internet of Things (IoT) – Semester 261 (Academic Year 2026–2027)
> **Course Lecturer**: Dr. Nguyễn Hòa Hưng (nguyenhoahung@hcmut.edu.vn)
> **Project Title**: AFES 2.0 – Advanced Fire Emergency System
> **Required Platform**: CoreIOT Server and ESP32-S3 (YoloUNO)
> **Deliverables**: Technical Documentation, Source Code on GitHub, Course Report (PDF), Demo Video

---

## 1. Grading Scheme and Evaluation Rules

According to the official Course Project Announcement (dated October 27th, 2026), project evaluation is governed by the following formula:

$$\text{Project Score} = \min(8.0, \sum \text{Technology Elements}) + \text{Report Score} (\le 2.0) + \min(1.0, \sum \text{Advanced Features})$$

$$\text{Maximum Score} = 10.0 \text{ points}$$

### 1.1. Core Rules
1. **Evidence Requirement**: An element earns points only if verifiable evidence (test execution logs, screenshots, recorded demo video, source code) is documented in the final report and repository.
2. **Partial Completion**: Partially implemented elements are graded according to their demonstrated level of completion.
3. **Dual-Stage Traceability**: AFES 2.0 divides implementation into **Stage A (Virtual Simulation & Contract Verification)** and **Stage B (Physical Hardware Integration)**. Claims of physical hardware verification are strictly prohibited until Stage B execution.
4. **Status Definitions**: Every task status field in this matrix must be strictly one of:
   * `NOT_STARTED`: Work has not yet commenced.
   * `IN_PROGRESS`: Active development underway.
   * `IMPLEMENTED`: Code written and committed, pending test verification.
   * `TESTED`: Verified via repeatable automated or lab test procedures.
   * `DOCUMENTED`: Architectural contracts, schemas, test plans, and interfaces fully specified.

---

## 2. Technology Elements Traceability Matrix (T01–T15)

The following matrix documents the complete traceability for all official course technology elements:

| ID | Technology Element | Pts | Status | Owner | Source Location | Issue Ref | Stage A Test Procedure | Stage B Test Procedure | Evidence Location | Completion Criterion |
|---|---|---|---|---|---|---|---|---|---|---|
| **T01** | Sensor using the I2C interface on Tasmota | 0.5 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/sensors/i2c_tasmota/` | Planned `#T01` | Validate I2C mock driver emitting synthetic temperature and humidity packets matching schema. | Flash Tasmota or custom I2C firmware to ESP32-S3; wire DHT20/SHT30 to SDA/SCL pins; verify I2C bus scan and periodic readings. | `reports/evidence/T01/` | Sensor successfully initialized on I2C bus; periodic readings logged to serial console and dispatched via Local Gateway / MQTT. |
| **T02** | Sensor using the Modbus RS485 interface | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/sensors/modbus_rs485/` | Planned `#T02` | Unit test Modbus RTU frame encoder/decoder against a software Modbus slave simulator. | Connect MAX485 transceiver to ESP32-S3 UART; poll industrial RS485 soil/air sensor; verify Modbus CRC check and registers. | `reports/evidence/T02/` | Modbus query-response loop succeeds without unhandled CRC errors, verified by serial and telemetry logs (consecutive cycle target TBD). |
| **T03** | Sensor connected to another device via BLE | 1.5 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/sensors/ble_client/` | Planned `#T03` | Mock BLE central service receiving synthetic GATT notifications in virtual test environment. | ESP32-S3 acts as BLE Central; scans, connects to peripheral BLE sensor beacon, subscribes to environmental GATT service. | `reports/evidence/T03/` | Successful BLE pairing, service discovery, and real-time reception of temperature/humidity notifications. |
| **T04** | Information inferred by AI (TinyML running on the device) | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/tinyml/` | Planned `#T04` | Run TensorFlow Lite Micro inference in desktop simulator against pre-recorded smoke/fire test vectors. | Flash quantized TFLite Micro model (`.tflite`) into ESP32-S3 Flash; feed live MQ-2, DHT20, and flame ADC inputs; measure inference latency. | `reports/evidence/T04/` | Model executes on-device within real-time deadline (latency target TBD during model profiling); outputs classification probability distinguishing true fire from ambient cooking smoke. |
| **T05** | Tooling for data collection, training and exporting a TinyML model | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `tools/tinyml_pipeline/` | Planned `#T05` | Execute Python data collection pipeline and train baseline model using synthetic test dataset. | Run Python serial logger to collect real physical smoke and fire sensor data; train binary classification model; quantize to int8 and export C++ header array. | `reports/evidence/T05/` | Reproducible Python training script (`train.py`), exported `model_data.h`, and validation confusion matrix (target accuracy threshold TBD during dataset labeling). |
| **T06** | Wireless communication using ESP-NOW | 1.5 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/comms/esp_now/` | Planned `#T06` | Simulate ESP-NOW frame structure and packet serialization over local mock network interface. | Provision peer MAC addresses; transmit telemetry packets from edge node to Local Gateway ESP32 receiver via ESP-NOW protocol. | `reports/evidence/T06/` | Bi-directional ESP-NOW packet delivery confirmed via test logs and serial monitor (latency and packet loss targets TBD during RF characterization). |
| **T07** | On-device web server (self-implemented – local display and control) | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/webserver/` | Planned `#T07` | Host embedded HTML/JS test payload on local mock server; verify REST endpoints. | Start ESP32-S3 SoftAP or LAN HTTP server; access web browser from phone/PC; view live sensor readings and trigger manual relay toggle. | `reports/evidence/T07/` | Web page renders correctly in browser; actuator toggle buttons successfully trigger local relay pin without external server. |
| **T08** | IoT Gateway implemented on a PC (or Raspberry Pi) | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `local-gateway/src/` | Planned `#T08` | Run Gateway container on developer PC; ingest simulated multi-node telemetry and forward to local broker. | Deploy Python/Node gateway service on PC/Pi; connect USB transceivers; aggregate physical sensor data; forward to CoreIOT and distribute RPC commands. | `reports/evidence/T08/` | Gateway aggregates data from multiple nodes, buffers offline telemetry in SQLite, and dispatches CoreIOT RPC commands to devices. |
| **T09** | AI function running on the local IoT Gateway | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `local-gateway/src/edge_ai/` | Planned `#T09` | Evaluate multi-sensor spatial fusion model on historical simulation dataset. | Gateway edge AI script ingests multi-room time-series streams; detects cross-zone thermal propagation anomalies; flags fire events to CoreIOT. | `reports/evidence/T09/` | Anomaly detection model accurately detects simulated multi-room fire event and publishes high-priority event packet to CoreIOT. |
| **T10** | Monitoring and control interface on the local IoT Gateway | 1.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `local-gateway/ui/` | Planned `#T10` | Run local web UI on PC; simulate offline network state; verify local manual controls function. | Access gateway UI via local browser (`http://localhost:5000`); inspect connected node health, view real-time charts, and issue local emergency commands. | `reports/evidence/T10/` | Independent operational UI functional on local gateway; permits complete monitoring and manual overrides without Internet connection. |
| **T11** | Using templates to develop the application, design dashboards, and monitor/control remotely | 1.0 | `DOCUMENTED` | Huy (Arch & Backend Lead) | `coreiot/dashboards/` | `#3` | Import CoreIOT dashboard JSON template into CoreIOT sandbox; verify widget bindings with virtual telemetry. | Connect physical gateway to CoreIOT; verify live widgets render telemetry gauges, floorplan status, and remote pump/siren toggle switches. | `reports/evidence/T11/` | Functional CoreIOT dashboard displaying multi-node data, historical trends, and remote control widgets (platform-specific mappings deferred to Issue #3). |
| **T12** | Using RuleChain to develop smart features | 1.0 | `DOCUMENTED` | Huy (Arch & Backend Lead) | `coreiot/rulechains/` | `#3` | Design and export RuleChain JSON; test with simulated sensor telemetry exceeding alert thresholds. | CoreIOT RuleChain evaluates real-time telemetry; detects temperature $> 50^\circ\text{C}$ or smoke $> 500\text{ PPM}$; triggers automated RPC command to activate water pump. | `reports/evidence/T12/` | RuleChain execution log demonstrating automatic downstream RPC trigger and event logging upon threshold breach. |
| **T13** | Sending alert notifications when data exceeds a threshold | 0.5 | `DOCUMENTED` | Huy (Arch & Backend Lead) | `coreiot/notifications/` | `#3` | Inject simulated high-temperature reading into CoreIOT; verify notification trigger node execution. | CoreIOT notification rule dispatches alert email, Telegram message, or SMS to designated safety personnel when threshold is exceeded. | `reports/evidence/T13/` | Verifiable alert receipt confirmed upon threshold violation (delivery SLA TBD). |
| **T14** | OTA firmware updates for devices | 2.0 | `DOCUMENTED` | Khánh (Firmware & Gateway Lead) | `firmware/esp32-s3/src/ota/` | Planned `#T14` | Upload dummy binary to local HTTP server; verify ESP32 OTA client downloads, validates checksum, and restarts. | Upload compiled firmware binary to CoreIOT OTA package repository; CoreIOT assigns package to device; ESP32-S3 updates over Wi-Fi and reboots. | `reports/evidence/T14/` | Firmware version successfully increments (e.g., v2.0.0 $\to$ v2.0.1) confirmed via serial log and device telemetry attribute. |
| **T15** | IoT Gateway on CoreIOT synchronized with the local IoT Gateway | 2.0 | `DOCUMENTED` | Huy & Khánh (CoreIOT & Gateway) | `local-gateway/src/coreiot_sync/` | `#3` | Run synchronization script between local gateway mock and CoreIOT sandbox; verify device provisioning. | Local IoT Gateway authenticates with CoreIOT Gateway API; CoreIOT automatically registers connected edge nodes and bidirectional RPC routes. | `reports/evidence/T15/` | CoreIOT Gateway entity displays connected physical nodes as child devices; telemetry and commands synchronize reliably (latency SLA and exact protocol mappings deferred to Issue #3). |

---

## 3. Advanced Bonus Features Matrix (N01–N07)

The syllabus permits up to 1.0 point bonus from advanced features (capped at 1.0 point total):

| ID | Advanced Feature | Pts | Planned Scope in AFES 2.0 | Status | Target Tier | Owner | Completion Criterion |
|---|---|---|---|---|---|---|---|
| **N01** | Virtual assistant – LLM | 1.0 | Natural language fire incident query assistant embedded in Frontend. | `NOT_STARTED` | Tier 5 (Frontend) | Ý (Frontend Lead @gutjmosnin) | LLM assistant answers operator queries (e.g., "Which zones exceeded warning limits today?"). |
| **N02** | Voice – Audio | 1.0 | Audible evacuation voice prompts generated upon confirmed fire alarm. | `NOT_STARTED` | Tier 1 / 2 | Khánh (Firmware Lead) | Audio amplifier / I2S DAC plays recorded voice evacuation instruction during alarm. |
| **N03** | LVGL-based display | 1.0 | On-device 1.69-inch or 2.4-inch LCD display driven by LVGL graphics library on ESP32-S3. | `NOT_STARTED` | Tier 1 (Node) | Khánh (Firmware Lead) | Screen renders live status gauges, animated fire alarm warning, and network QR code. |
| **N04** | AI running on the device GPU | 1.0 | Edge AI computer vision fire/smoke detection running on Local Gateway GPU / NPU. | `NOT_STARTED` | Tier 2 (Gateway) | Khánh (Gateway Lead) | OpenCV / YOLOv8-nano model detects flames in video feed (target FPS TBD based on hardware accelerator). |
| **N05** | Custom-designed mobile app | 1.0 | Flutter / React Native mobile application for mobile operator push alerts and controls. | `NOT_STARTED` | Client App | Team (TBD) | Mobile app receives instant push notifications and displays floor plan emergency status. |
| **N06** | Custom-designed dashboard able to detect and record events | 1.0 | React 18 / Vite Fullstack Web Application with persistent event log and interactive floorplan. | `IN_PROGRESS` | Tier 5 (Frontend) | Ý (Frontend Lead @gutjmosnin) | Custom web app tracks, correlates, and displays real-time alarms with timeline recording. |
| **N07** | Self-deployed ThingsBoard on a local machine | 1.0 | Explicitly optional course bonus item: self-hosted ThingsBoard instance in Docker for local offline fallback (not an assumed CoreIOT implementation). | `NOT_STARTED` | Tier 3 (CoreIOT) | Huy (Arch & Backend Lead) | Standalone Community ThingsBoard running in docker-compose stack for optional offline evaluation. |

---

## 4. Two-Stage Lifecycle and Verification Protocol

```
+---------------------------------------------------------------------------------+
|                    STAGE A: VIRTUAL SIMULATION & CONTRACT VALIDATION             |
|  - Synthetic Telemetry Generator (Python/Node) emitting AFES v2.0 schema        |
|  - Mock Sensing Nodes running with `simulation.is_simulated = true`             |
|  - Local Gateway Aggregator & CoreIOT Sandbox configuration                     |
|  - Spring Boot Backend RBAC & React Frontend Dashboard validation               |
|  * STRICT RULE: Zero physical hardware claims. All evidence labeled SIMULATION. |
+---------------------------------------------------------------------------------+
                                         |
                                         v Formal Contract Sign-Off
+---------------------------------------------------------------------------------+
|                   STAGE B: PHYSICAL HARDWARE INTEGRATION & MEASUREMENT           |
|  - Flash ESP32-S3 (YoloUNO) boards with FreeRTOS PlatformIO firmware            |
|  - Connect physical sensors: DHT20 (I2C), Modbus RS485, MQ-2, Flame Sensor      |
|  - Deploy Local Gateway on physical PC / Raspberry Pi with USB transceivers     |
|  - Connect live to HCMUT CoreIOT production tenant (`is_simulated = false`)     |
|  * Rigorous lab measurement: latency, power, false-positive rate, video demo.   |
+---------------------------------------------------------------------------------+
```

### 4.1. Strict Separation Rules
1. **Simulation Tagging**: Every Stage A data point, chart, and log file must display the tag `[SIMULATED - STAGE A]`.
2. **Hardware Integrity**: Stage B hardware measurements must record exact instrument model numbers, serial debug timestamps, logic analyzer captures, and physical photographs of the test apparatus.
3. **Traceability**: All pull requests must declare whether they contribute to Stage A tooling or Stage B firmware/hardware.
