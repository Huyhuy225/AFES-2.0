# AFES 2.0 Development Guide & Validation Standards

This guide covers the development setup, repository hygiene practices, and the dual-track testing standards for **AFES 2.0 (Advanced Fire Emergency System – Multi-Node IoT Monitoring and Emergency Response)**.

---

## 1. System Architecture Overview

AFES 2.0 operates across multiple hardware and software tiers:

1. **Edge Sensor Nodes**: ESP32-based microcontroller nodes interfacing with multi-sensor arrays (flame optical detectors, MQ-2 gas/smoke sensors, DHT22 temperature/humidity sensors), buzzer indicators, and emergency cutoff relays.
2. **Local Edge Gateway**: An on-premises gateway aggregating node telemetry over Wi-Fi/MQTT, handling low-latency offline emergency actions, and relaying telemetry to the cloud.
3. **CoreIOT Platform**: Central cloud IoT platform providing device provisioning, token authentication, telemetry ingestion, and rule-based event routing.
4. **Backend Services**: Business logic, historical event storage (PostgreSQL/TimescaleDB), audit logging, and notification dispatchers.
5. **Frontend Dashboard**: Real-time monitoring UI displaying node statuses, telemetry streams, and emergency alarm states.

---

## 2. Local Environment Setup

### 2.1 Prerequisites
Ensure the following tools are installed on your workstation:
- **Git** (version 2.30+)
- **Python** (version 3.11+ / 3.12 / 3.14)
- **Node.js** (version 20+ LTS)
- **PlatformIO CLI / VSCode Extension** (for ESP32 embedded firmware)
- **Docker & Docker Compose** (for running local MQTT broker and database containers)

### 2.2 Configuration Management
1. Clone the repository and ensure you are on the `develop` branch.
2. Copy the example configuration template:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` to configure your local test values.

> [!WARNING]
> Never commit `.env` or any file containing real passwords, private keys, or API credentials to version control. The repository enforces zero-credential storage.

---

## 3. Dual-Track Testing: Simulation vs. Physical Hardware Validation

AFES 2.0 strictly distinguishes between **Software Simulation Validation** and **Physical Hardware Validation**. Every pull request that introduces functional code must document the relevant validation track in its PR submission.

```
+------------------------------------------------------------------------+
|                            AFES 2.0 Validation                         |
+------------------------------------+-----------------------------------+
|     Track 1: Simulation Track      |    Track 2: Physical Hardware     |
+------------------------------------+-----------------------------------+
| - Mock sensor telemetry streams    | - Real ESP32 microcontrollers     |
| - Synthetic flame/smoke/heat spikes| - Physical MQ-2, DHT22, Flame     |
| - Virtual MQTT broker              | - Serial monitor (115200 baud)    |
| - Automated unit & integration tests| - Real GPIO, relay, buzzer tests  |
| - Zero physical hardware required  | - Power loss & RF attenuation tests|
| - Fast, deterministic CI-ready     | - Physical bench measurement logs |
+------------------------------------+-----------------------------------+
```

---

### Track 1: Software & Simulation Validation

Simulation validation enables rapid iteration and automated verification without requiring physical microcontrollers or live sensor hardware.

#### 1. When to Use
- Validating business logic, state machine transitions, and emergency threshold rules.
- Validating MQTT telemetry JSON schemas and contract parsing.
- Gateway routing, data transformations, and CoreIOT payload formatting.
- Unit testing, linting, and automated repository hygiene.

#### 2. Simulation Environment Setup
- **Local MQTT Broker**: Run a local Mosquitto broker:
  ```bash
  docker run -d --name afes-mosquitto -p 1883:1883 eclipse-mosquitto:2
  ```
- **Configuration**: Ensure `HARDWARE_SIMULATION_MODE=true` in your `.env`.

#### 3. Executing Simulation Tests
- Run synthetic sensor stream generation:
  ```bash
  # Example: Execute local telemetry simulator producing synthetic temperature, smoke, and flame signals
  python -m tests.simulation.publisher --nodes 3 --interval 1000
  ```
- Run unit and schema verification tests:
  ```bash
  # Example: Run contract validation tests
  pytest tests/unit/
  ```

#### 4. Required Simulation Deliverables in Pull Requests
- Exact commands executed and terminal exit code (`exit 0`).
- Synthetic telemetry log excerpts demonstrating expected threshold detection.
- Schema verification pass confirmation.

---

### Track 2: Physical Hardware Validation

Physical hardware validation verifies real-world sensor physics, analog-to-digital conversion, electrical characteristics, wiring integrity, and physical fail-safe mechanisms.

#### 1. When to Use
- ESP32 firmware updates, driver implementation, or pinout changes.
- Sensor calibration (e.g., MQ-2 analog curve, flame sensor optical threshold).
- Physical relay actuation (e.g., automated power/gas valve cutoff).
- Hardware buzzer frequencies and emergency sound patterns.
- Hardware watchdog, brownout protection, and Wi-Fi reconnection after signal loss.

#### 2. Hardware Bench Setup
- **Microcontroller**: ESP32-WROOM-32 development board connected via USB.
- **Sensors**:
  - Optical Flame Sensor: Digital pin GPIO 19 / Analog pin ADC1_CH0 (GPIO 36).
  - MQ-2 Smoke/Combustible Gas Sensor: Analog pin ADC1_CH3 (GPIO 39), with 2-minute pre-heat warm-up.
  - DHT22 Temperature/Humidity: Digital pin GPIO 23 with 10k pull-up resistor.
  - Actuators: 5V Relay module on GPIO 18; Active 3.3V Buzzer on GPIO 5.
- **Power Supply**: 5V/2A external DC power source for sensors and relay coil.

#### 3. Executing Physical Hardware Tests
1. **Build and Flash Firmware**:
   ```bash
   pio run -e esp32dev --target upload
   ```
2. **Monitor Serial Output**:
   ```bash
   pio device monitor --baud 115200
   ```
3. **Physical Stimulus Verification**:
   - **Flame Test**: Introduce a controlled light/flame stimulus at 0.5m distance. Verify serial log registers `FLAME_DETECTED`, GPIO 18 trips the relay within 200ms, and emergency buzzer sounds.
   - **Smoke Test**: Apply aerosol test smoke to the MQ-2 sensor. Verify serial log registers sensor ADC increase above configured ppm threshold.
   - **Network Severing Test**: Power off the Wi-Fi access point during active operation. Verify the ESP32 logs offline mode, stores emergency events in local ring buffer, and successfully reconnects with exponential backoff when the AP restarts.

#### 4. Required Physical Hardware Deliverables in Pull Requests
- Serial monitor log excerpts (with timestamps and baud rate 115200).
- Recorded sensor readings (raw ADC vs. converted engineering units).
- Photographs or video recordings of physical bench tests showing LED/relay/buzzer actuation.
- Documentation of hardware revisions and ambient test conditions (temperature, humidity).

---

### Validation Matrix by PR Scope

| Change Area | Track 1: Simulation Required | Track 2: Hardware Required | Notes |
|---|---|---|---|
| **Governance & Docs** | `git diff --check`, YAML check | N/A | Static checks only |
| **Backend & APIs** | Full Simulation suite | N/A | Mock telemetry used |
| **Local Gateway Service** | Full Simulation suite | Optional (Recommended) | Mock nodes or physical ESP32 |
| **ESP32 Firmware** | Simulation unit tests | **Mandatory** | Physical bench log required |
| **Sensor Drivers & Actuators** | Unit tests on mock structs | **Mandatory** | Physical stimulus test required |
| **Emergency Trigger Logic** | Full Simulation suite | **Mandatory** | End-to-end latency measured |

---

## 4. Local Repository Hygiene & Pre-Flight Checks

Before opening any pull request, execute the following verification steps locally:

### Step 1: Git Diff & Whitespace Check
```bash
git diff --check
```
Ensure zero trailing whitespace errors or conflict markers exist.

### Step 2: YAML Syntax Validation
Verify that all GitHub Actions workflows and issue templates are valid YAML:
```bash
python -c "import glob, yaml, sys; errors = [f for f in glob.glob('.github/**/*.yml', recursive=True) if not yaml.safe_load(open(f, encoding='utf-8'))]; sys.exit(1 if errors else 0)"
```

### Step 3: Zero-Credential Audit
Verify that no private keys, passwords, or tokens are staged:
```bash
python -c "import os, sys; [print(f'Committed .env: {f}') for f in os.listdir('.') if f.startswith('.env') and f != '.env.example']"
```

---

## 5. Troubleshooting & FAQ

### 1. MQ-2 Sensor reports wildly fluctuating values
- *Cause*: MQ-2 sensors require a 24-48 hour initial burn-in and a 2-3 minute warm-up cycle upon cold boot before readings stabilize.
- *Fix*: Allow the heating element to stabilize before recording baseline clean-air values.

### 2. Serial Monitor displays garbled characters
- *Cause*: Baud rate mismatch.
- *Fix*: Confirm serial monitor is configured for `115200` baud (`monitor_speed = 115200` in `platformio.ini`).

### 3. CI fails with YAML syntax error
- *Cause*: Inconsistent indentation or invalid characters in `.github/workflows/` or `.github/ISSUE_TEMPLATE/`.
- *Fix*: Run the local Python YAML validation command above to pinpoint the exact line number.
