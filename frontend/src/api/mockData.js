/**
 * AFES 2.0 Mock Telemetry & Fixtures Provider
 * Fully compliant with docs/API_SPECIFICATION.md and docs/TELEMETRY_SCHEMA.md
 * Stage A Simulation Contract verified
 */

import {
  SYSTEM_STATES,
  SENSOR_HEALTH,
  DEVICE_STATUS,
  EVENT_TYPES,
  EVENT_SEVERITY,
} from '../contracts/afesContracts';

// Initial baseline mock zones
export const createInitialZones = () => [
  {
    zone_id: 'ZONE-101',
    room_code: 'ROOM-101',
    name: 'Server Equipment Room',
    floor: 1,
    system_state: SYSTEM_STATES.NORMAL,
    active_alarm_count: 0,
    latest_readings: {
      temperature: 24.5,
      humidity: 48.2,
      smoke_ppm: 45.0,
      flame_detected: false,
      ai_inferred_fire_risk: 0.05,
    },
    actuator_state: {
      buzzer_active: false,
      pump_active: false,
    },
    node_count: 2,
    last_updated_epoch_ms: Date.now() - 2500,
  },
  {
    zone_id: 'ZONE-102',
    room_code: 'ROOM-102',
    name: 'High-Density Battery Vault',
    floor: 1,
    system_state: SYSTEM_STATES.NORMAL,
    active_alarm_count: 0,
    latest_readings: {
      temperature: 23.8,
      humidity: 44.5,
      smoke_ppm: 28.0,
      flame_detected: false,
      ai_inferred_fire_risk: 0.03,
    },
    actuator_state: {
      buzzer_active: false,
      pump_active: false,
    },
    node_count: 1,
    last_updated_epoch_ms: Date.now() - 1200,
  },
  {
    zone_id: 'ZONE-103',
    room_code: 'ROOM-201',
    name: 'Chemical Storage Lab',
    floor: 2,
    system_state: SYSTEM_STATES.NORMAL,
    active_alarm_count: 0,
    latest_readings: {
      temperature: 21.0,
      humidity: 52.0,
      smoke_ppm: 32.0,
      flame_detected: false,
      ai_inferred_fire_risk: 0.02,
    },
    actuator_state: {
      buzzer_active: false,
      pump_active: false,
    },
    node_count: 1,
    last_updated_epoch_ms: Date.now() - 3400,
  },
  {
    zone_id: 'ZONE-104',
    room_code: 'ROOM-301',
    name: 'Executive Operations Center',
    floor: 3,
    system_state: SYSTEM_STATES.NORMAL,
    active_alarm_count: 0,
    latest_readings: {
      temperature: 23.2,
      humidity: 50.1,
      smoke_ppm: 18.0,
      flame_detected: false,
      ai_inferred_fire_risk: 0.01,
    },
    actuator_state: {
      buzzer_active: false,
      pump_active: false,
    },
    node_count: 1,
    last_updated_epoch_ms: Date.now() - 5100,
  },
];

// Initial baseline mock devices
export const createInitialDevices = () => [
  {
    device_id: 'ESP32S3-YOLO-01',
    zone_id: 'ZONE-101',
    room_code: 'ROOM-101',
    device_type: 'YOLO_UNO_S3',
    firmware_version: '2.1.0-stageA',
    hardware_version: 'v1.2',
    status: DEVICE_STATUS.ONLINE,
    sensor_health: SENSOR_HEALTH.HEALTHY,
    rssi_dbm: -62,
    uptime_seconds: 128450,
    heap_free_bytes: 194560,
    tinyml_inference_latency_ms: 24,
    is_simulated: true,
    last_seen_epoch_ms: Date.now() - 1500,
  },
  {
    device_id: 'ESP32S3-YOLO-02',
    zone_id: 'ZONE-102',
    room_code: 'ROOM-102',
    device_type: 'YOLO_UNO_S3',
    firmware_version: '2.1.0-stageA',
    hardware_version: 'v1.2',
    status: DEVICE_STATUS.ONLINE,
    sensor_health: SENSOR_HEALTH.HEALTHY,
    rssi_dbm: -71,
    uptime_seconds: 95400,
    heap_free_bytes: 182300,
    tinyml_inference_latency_ms: 28,
    is_simulated: true,
    last_seen_epoch_ms: Date.now() - 1100,
  },
  {
    device_id: 'ESP32S3-YOLO-03',
    zone_id: 'ZONE-103',
    room_code: 'ROOM-201',
    device_type: 'YOLO_UNO_S3',
    firmware_version: '2.1.0-stageA',
    hardware_version: 'v1.2',
    status: DEVICE_STATUS.ONLINE,
    sensor_health: SENSOR_HEALTH.HEALTHY,
    rssi_dbm: -58,
    uptime_seconds: 214000,
    heap_free_bytes: 201400,
    tinyml_inference_latency_ms: 22,
    is_simulated: true,
    last_seen_epoch_ms: Date.now() - 3200,
  },
  {
    device_id: 'ESP32S3-YOLO-04',
    zone_id: 'ZONE-104',
    room_code: 'ROOM-301',
    device_type: 'YOLO_UNO_S3',
    firmware_version: '2.0.8-stageA',
    hardware_version: 'v1.1',
    status: DEVICE_STATUS.OFFLINE,
    sensor_health: SENSOR_HEALTH.ERROR,
    rssi_dbm: -89,
    uptime_seconds: 0,
    heap_free_bytes: 0,
    tinyml_inference_latency_ms: 0,
    is_simulated: true,
    last_seen_epoch_ms: Date.now() - 1800000,
  },
];

// Initial baseline mock alarms: Empty on initial Stage A mock load (neutral baseline)
export const createInitialAlarms = () => [];

// Generate synthetic historical telemetry series
export const generateMockTelemetryHistory = (pointsCount = 20) => {
  const points = [];
  const now = Date.now();
  const stepMs = 60 * 1000; // 1 minute per point

  for (let i = pointsCount - 1; i >= 0; i--) {
    const time = now - i * stepMs;
    // Base normal wave with slight noise
    const baseTemp = 24.0 + Math.sin(i / 3) * 1.5 + (Math.random() * 0.4 - 0.2);
    const baseSmoke = 42.0 + Math.cos(i / 4) * 8.0 + (Math.random() * 4.0 - 2.0);
    const baseHumidity = 48.0 + Math.sin(i / 5) * 3.0;

    points.push({
      timestamp_epoch_ms: time,
      timestamp_iso: new Date(time).toISOString(),
      temperature: Number(baseTemp.toFixed(1)),
      smoke_ppm: Number(baseSmoke.toFixed(1)),
      humidity: Number(baseHumidity.toFixed(1)),
      flame_detected: false,
      ai_inferred_fire_risk: Number((baseSmoke / 1000).toFixed(2)),
      is_simulated: true,
    });
  }

  return points;
};
