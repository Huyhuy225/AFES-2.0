# AFES 2.0 ESP32-S3 Firmware Foundation (`firmware/esp32-s3/`)

> **Course Item**: Minimal ESP32-S3 PlatformIO C++ foundation (Stage B)
> **GitHub Issue**: [#36](https://github.com/Huyhuy225/AFES-2.0/issues/36)
> **Evidence Policy**: A build alone is **not** completion. Closing `#36` requires flashing a physical ESP32-S3 (`YOLO_UNO_S3`), recording the `115200` baud serial boot log, and observing live MQTT telemetry labelled `PHYSICAL HARDWARE`.

## Setup

1. Install **PlatformIO** (VS Code extension or `pip install platformio`).
2. Copy `include/secrets.example.h` to `include/secrets.h` (never commit `include/secrets.h`).
3. Fill in your local Wi-Fi SSID/password and Local Gateway MQTT broker IP/credentials.
4. Adjust GPIO pin mappings in `include/config.h` to match your physical YoloUNO S3 wiring.

## Build, Flash, and Monitor

```powershell
cd firmware/esp32-s3
pio run
pio run -t upload
pio device monitor -b 115200
```

## Stage B Contract Rules

- `simulation.is_simulated` is hardcoded to `false` (`scenario_id = null`, `synthetic_noise_added = false`).
- `device.device_type` is `"YOLO_UNO_S3"`.
- `device.mac_address` is read from hardware eFuse (`esp_read_mac`), never hardcoded.
- Local safety actions (buzzer, alarm LED, pump relay) execute autonomously without depending on Wi-Fi or WAN availability.
