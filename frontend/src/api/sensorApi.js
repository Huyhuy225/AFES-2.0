/**
 * AFES 2.0 Unified API Client and Telemetry Service
 * Implements REST endpoints conforming to docs/API_SPECIFICATION.md
 * Integrates zero-credential client with full in-memory mock simulator fallback
 */

import {
  createInitialZones,
  createInitialDevices,
  createInitialAlarms,
  generateMockTelemetryHistory,
} from './mockData';
import {
  SYSTEM_STATES,
  EVENT_TYPES,
  EVENT_SEVERITY,
  ACTUATOR_ACTIONS,
} from '../contracts/afesContracts';

const DEFAULT_API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v2';
const INITIAL_MOCK_MODE = import.meta.env.VITE_USE_MOCK_DATA !== 'false';

// Stateful mock repository for Stage A local testing
class MockStateStore {
  constructor() {
    this.reset();
  }

  reset() {
    this.zones = createInitialZones();
    this.devices = createInitialDevices();
    this.alarms = createInitialAlarms();
    this.telemetryHistory = generateMockTelemetryHistory(25);
    this.activeScenario = null;
    this.commandLog = [];
  }

  getZonesSummary() {
    return JSON.parse(JSON.stringify(this.zones));
  }

  getDevices(filter = {}) {
    let result = [...this.devices];
    if (filter.status && filter.status !== 'ALL') {
      result = result.filter((d) => d.status === filter.status);
    }
    if (filter.zone_id) {
      result = result.filter((d) => d.zone_id === filter.zone_id);
    }
    return JSON.parse(JSON.stringify(result));
  }

  getDeviceHealth(deviceId) {
    const dev = this.devices.find((d) => d.device_id === deviceId);
    if (!dev) {
      throw new Error(`Device not found: ${deviceId}`);
    }
    return JSON.parse(JSON.stringify(dev));
  }

  getTelemetryHistory(_params = {}) {
    return JSON.parse(JSON.stringify(this.telemetryHistory));
  }

  getActiveAlarms() {
    return JSON.parse(JSON.stringify(this.alarms.filter((a) => a.ack_status !== 'RESOLVED')));
  }

  acknowledgeAlarm(alarmId, note = 'Acknowledged by operator') {
    const alarm = this.alarms.find((a) => a.event_id === alarmId);
    if (!alarm) {
      throw new Error(`Alarm ${alarmId} not found`);
    }
    alarm.ack_status = 'ACKNOWLEDGED';
    alarm.operator_note = note;
    alarm.acknowledged_at = new Date().toISOString();
    return JSON.parse(JSON.stringify(alarm));
  }

  resolveAlarm(alarmId) {
    const index = this.alarms.findIndex((a) => a.event_id === alarmId);
    if (index === -1) {
      throw new Error(`Alarm ${alarmId} not found`);
    }
    const resolved = this.alarms[index];
    resolved.ack_status = 'RESOLVED';
    resolved.resolved_at = new Date().toISOString();

    // If resolving alarm for a zone, update zone system state back to NORMAL if no other alarms
    const zone = this.zones.find((z) => z.zone_id === resolved.zone_id);
    if (zone) {
      const otherAlarms = this.alarms.filter(
        (a) => a.zone_id === zone.zone_id && a.event_id !== alarmId && a.ack_status !== 'RESOLVED'
      );
      zone.active_alarm_count = otherAlarms.length;
      if (otherAlarms.length === 0) {
        zone.system_state = SYSTEM_STATES.NORMAL;
        zone.actuator_state.buzzer_active = false;
      }
    }
    return JSON.parse(JSON.stringify(resolved));
  }

  dispatchCommand({ target_device_id, target_zone_id, action, parameters }) {
    const commandId = `cmd-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
    const logEntry = {
      command_id: commandId,
      target_device_id,
      target_zone_id,
      action,
      parameters,
      timestamp: Date.now(),
      status: 'EXECUTED',
    };

    // Apply side-effects to mock zones and actuators
    if (action === ACTUATOR_ACTIONS.PUMP_ON) {
      this.zones.forEach((z) => {
        if (!target_zone_id || z.zone_id === target_zone_id) {
          z.actuator_state.pump_active = true;
        }
      });
      logEntry.message = `Water pump relay energized${parameters?.duration_ms ? ` for ${parameters.duration_ms} ms` : ''}`;
    } else if (action === ACTUATOR_ACTIONS.PUMP_OFF) {
      this.zones.forEach((z) => {
        if (!target_zone_id || z.zone_id === target_zone_id) {
          z.actuator_state.pump_active = false;
        }
      });
      logEntry.message = 'Water pump relay de-energized';
    } else if (action === ACTUATOR_ACTIONS.TEST_ALARM) {
      this.zones.forEach((z) => {
        if (!target_zone_id || z.zone_id === target_zone_id) {
          z.actuator_state.buzzer_active = true;
        }
      });
      logEntry.message = 'Acoustic siren test pulse emitted';
    } else if (action === ACTUATOR_ACTIONS.RESET_ALERTS) {
      // Synchronized reset: clears alerts, zeroes manual overrides, silences sirens
      this.zones.forEach((z) => {
        z.actuator_state.pump_active = false;
        z.actuator_state.buzzer_active = false;
        if (z.system_state !== SYSTEM_STATES.CRITICAL) {
          z.system_state = SYSTEM_STATES.NORMAL;
          z.active_alarm_count = 0;
        }
      });
      this.alarms.forEach((a) => {
        if (a.ack_status === 'PENDING') {
          a.ack_status = 'ACKNOWLEDGED';
        }
      });
      logEntry.message = 'System alerts safely unlatched and actuators reset';
    } else if (action === ACTUATOR_ACTIONS.EMERGENCY_SHUTDOWN) {
      this.zones.forEach((z) => {
        z.system_state = SYSTEM_STATES.CRITICAL;
        z.actuator_state.pump_active = true;
        z.actuator_state.buzzer_active = true;
      });
      logEntry.message = 'Building-wide emergency evacuation alarm activated';
    }

    this.commandLog.push(logEntry);
    return logEntry;
  }

  startSimulationScenario(scenarioId) {
    this.activeScenario = scenarioId;
    if (scenarioId === 'FIRE_SPIKE_ZONE_101') {
      const z101 = this.zones.find((z) => z.zone_id === 'ZONE-101');
      if (z101) {
        z101.system_state = SYSTEM_STATES.CRITICAL;
        z101.active_alarm_count += 1;
        z101.latest_readings = {
          temperature: 74.8,
          humidity: 28.5,
          smoke_ppm: 885.0,
          flame_detected: true,
          ai_inferred_fire_risk: 0.96,
        };
        z101.actuator_state.buzzer_active = true;
        z101.actuator_state.pump_active = true;
      }

      const newAlarm = {
        event_id: `evt-crit-${Date.now()}`,
        timestamp_utc: new Date().toISOString(),
        timestamp_epoch_ms: Date.now(),
        device_id: 'ESP32S3-YOLO-01',
        zone_id: 'ZONE-101',
        room_code: 'ROOM-101',
        event_type: EVENT_TYPES.FIRE_ALARM_CRITICAL,
        severity: EVENT_SEVERITY.CRITICAL,
        trigger_source: 'MULTI_SENSOR_FUSION',
        trigger_details: {
          temperature_c: 74.8,
          temperature_threshold_c: 50.0,
          smoke_ppm: 885.0,
          smoke_threshold_ppm: 500.0,
          flame_detected: true,
          tinyml_fire_confidence: 0.96,
        },
        autonomous_actions_taken: [
          'LOCAL_BUZZER_ACTIVE',
          'LOCAL_PUMP_ENGAGED',
          'EMERGENCY_LOCK_ENGAGED',
        ],
        ack_required: true,
        ack_status: 'PENDING',
        simulation: {
          is_simulated: true,
          scenario_id: 'FIRE_SPIKE_ZONE_101',
        },
      };
      this.alarms.unshift(newAlarm);

      // Add a spike point to history
      this.telemetryHistory.push({
        timestamp_epoch_ms: Date.now(),
        timestamp_iso: new Date().toISOString(),
        temperature: 74.8,
        smoke_ppm: 885.0,
        humidity: 28.5,
        flame_detected: true,
        ai_inferred_fire_risk: 0.96,
        is_simulated: true,
      });
    }
  }

  stopSimulationScenario() {
    this.activeScenario = null;
    this.reset();
  }
}

// Global singleton instance for mock store
const mockStore = new MockStateStore();

class ApiService {
  constructor() {
    this.baseUrl = DEFAULT_API_URL;
    this.useMock = INITIAL_MOCK_MODE;
    this.isBackendLive = false;
  }

  setMockMode(enable) {
    this.useMock = Boolean(enable);
  }

  isUsingMock() {
    return this.useMock;
  }

  async _fetch(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...options.headers,
    };

    // Strict security check: Ensure NO CoreIOT administrative tokens are present
    if (headers['X-CoreIOT-Token'] || headers['X-Authorization']) {
      throw new Error('SECURITY VIOLATION: CoreIOT token detected in client request.');
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const message = errorData?.error?.message || `HTTP ${response.status}: ${response.statusText}`;
        const err = new Error(message);
        err.status = response.status;
        err.code = errorData?.error?.code || 'ERR_HTTP';
        throw err;
      }

      this.isBackendLive = true;
      const json = await response.json();
      return json.data;
    } catch (err) {
      clearTimeout(timeoutId);
      // Auto-fallback to mock mode on network failure if allowed
      this.isBackendLive = false;
      throw err;
    }
  }

  async getZonesSummary() {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 60));
      return mockStore.getZonesSummary();
    }
    try {
      return await this._fetch('/zones/summary');
    } catch (err) {
      console.warn('Backend unavailable, falling back to mock zones summary', err.message);
      return mockStore.getZonesSummary();
    }
  }

  async getDevices(params = {}) {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 50));
      return mockStore.getDevices(params);
    }
    try {
      const query = new URLSearchParams(params).toString();
      return await this._fetch(`/devices${query ? `?${query}` : ''}`);
    } catch (err) {
      console.warn('Backend unavailable, falling back to mock devices', err.message);
      return mockStore.getDevices(params);
    }
  }

  async getDeviceHealth(deviceId) {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 40));
      return mockStore.getDeviceHealth(deviceId);
    }
    try {
      return await this._fetch(`/devices/${deviceId}/health`);
    } catch {
      return mockStore.getDeviceHealth(deviceId);
    }
  }

  async getTelemetryHistory(params = {}) {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 60));
      return mockStore.getTelemetryHistory(params);
    }
    try {
      const query = new URLSearchParams(params).toString();
      return await this._fetch(`/telemetry/history${query ? `?${query}` : ''}`);
    } catch (err) {
      console.warn('Backend unavailable, falling back to mock telemetry history', err.message);
      return mockStore.getTelemetryHistory(params);
    }
  }

  async getActiveAlarms() {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 50));
      return mockStore.getActiveAlarms();
    }
    try {
      return await this._fetch('/alarms/active');
    } catch (err) {
      console.warn('Backend unavailable, falling back to mock active alarms', err.message);
      return mockStore.getActiveAlarms();
    }
  }

  async acknowledgeAlarm(alarmId, note) {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 80));
      return mockStore.acknowledgeAlarm(alarmId, note);
    }
    // Explicit live mode: invoke backend REST directly.
    // Safety Invariant: NEVER fall back to mockStore on mutation failure; propagate error directly.
    return await this._fetch(`/alarms/${alarmId}/acknowledge`, {
      method: 'POST',
      body: JSON.stringify({ note: note || 'Acknowledged by operator' }),
    });
  }

  async resolveAlarm(alarmId) {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 80));
      return mockStore.resolveAlarm(alarmId);
    }
    // Explicit live mode: invoke backend REST directly.
    // Safety Invariant: NEVER fall back to mockStore on mutation failure; propagate error directly.
    return await this._fetch(`/alarms/${alarmId}/resolve`, {
      method: 'POST',
    });
  }

  async dispatchControlCommand(payload) {
    if (this.useMock) {
      await new Promise((r) => setTimeout(r, 100));
      return mockStore.dispatchCommand(payload);
    }
    // Explicit live mode: invoke backend REST directly.
    // Safety Invariant: NEVER fall back to mockStore on mutation failure; propagate error directly.
    return await this._fetch('/control/command', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  startSimulationScenario(scenarioId) {
    mockStore.startSimulationScenario(scenarioId);
  }

  stopSimulationScenario() {
    mockStore.stopSimulationScenario();
  }

  getSimulationScenario() {
    return mockStore.activeScenario;
  }

  resetMockStore() {
    mockStore.reset();
  }
}

export const apiService = new ApiService();
export default apiService;
