#pragma once

// AFES 2.0 Stage B Physical Node Configuration
#define AFES_SCHEMA_VERSION "2.0"
#define AFES_TENANT_ID "default"
#define AFES_DEVICE_ID "ESP32S3-YOLO-01"
#define AFES_DEVICE_TYPE "YOLO_UNO_S3"
#define AFES_FIRMWARE_VERSION "2.1.0-stageB"
#define AFES_HARDWARE_VERSION "v1.0"

#define AFES_ZONE_ID "ZONE-A-FL1"
#define AFES_ROOM_CODE "ROOM-101"
#define AFES_BUILDING_ID "BLDG-CSE-B1"
#define AFES_FLOOR_LEVEL 1

#define AFES_GATEWAY_ID "GW-LOCAL-PC01"
#define AFES_GATEWAY_PROTOCOL "MQTT"
#define AFES_MESH_ROLE "ENDPOINT"

// Timing (ms)
#define TELEMETRY_INTERVAL_MS 2000UL
#define SAFETY_LOOP_INTERVAL_MS 200UL

// GPIO pin assignments (adjust to match physical YoloUNO S3 wiring)
#define PIN_MQ2_SMOKE_ADC 1
#define PIN_FLAME_ADC 2
#define PIN_FLAME_DO 3
#define PIN_BUZZER 4
#define PIN_ALARM_LED 5
#define PIN_PUMP_RELAY 6

// Local autonomous safety thresholds (independent of WAN/MQTT availability)
#define SMOKE_WARNING_PPM 300.0f
#define SMOKE_CRITICAL_PPM 500.0f
#define TEMP_CRITICAL_C 50.0f
