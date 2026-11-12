import { describe, it, expect, beforeEach } from 'vitest';
import apiService from '../api/sensorApi';
import { ACTUATOR_ACTIONS, SYSTEM_STATES } from '../contracts/afesContracts';

describe('ApiService & MockStateStore Unit Tests', () => {
  beforeEach(() => {
    apiService.resetMockStore();
    apiService.setMockMode(true);
  });

  it('retrieves zones summary conforming to API specification', async () => {
    const zones = await apiService.getZonesSummary();
    expect(Array.isArray(zones)).toBe(true);
    expect(zones.length).toBeGreaterThan(0);

    const first = zones[0];
    expect(first).toHaveProperty('zone_id');
    expect(first).toHaveProperty('room_code');
    expect(first).toHaveProperty('system_state');
    expect(first).toHaveProperty('latest_readings');
    expect(first.latest_readings).toHaveProperty('temperature');
    expect(first.latest_readings).toHaveProperty('smoke_ppm');
  });

  it('retrieves registered devices and filters by status', async () => {
    const all = await apiService.getDevices();
    expect(all.length).toBe(4);

    const online = await apiService.getDevices({ status: 'ONLINE' });
    expect(online.every((d) => d.status === 'ONLINE')).toBe(true);
    expect(online.length).toBe(3);
  });

  it('retrieves active alarms and acknowledges an alarm', async () => {
    const alarms = await apiService.getActiveAlarms();
    expect(alarms.length).toBeGreaterThan(0);

    const targetId = alarms[0].event_id;
    const acked = await apiService.acknowledgeAlarm(targetId, 'Unit test ack');
    expect(acked.ack_status).toBe('ACKNOWLEDGED');
    expect(acked.operator_note).toBe('Unit test ack');
  });

  it('resolves an alarm and updates zone state if cleared', async () => {
    const alarms = await apiService.getActiveAlarms();
    const targetId = alarms[0].event_id;

    const resolved = await apiService.resolveAlarm(targetId);
    expect(resolved.ack_status).toBe('RESOLVED');

    const updatedAlarms = await apiService.getActiveAlarms();
    expect(updatedAlarms.find((a) => a.event_id === targetId)).toBeUndefined();
  });

  it('dispatches PUMP_ON command and updates actuator state', async () => {
    const res = await apiService.dispatchControlCommand({
      target_zone_id: 'ZONE-101',
      action: ACTUATOR_ACTIONS.PUMP_ON,
      parameters: { duration_ms: 10000 },
    });

    expect(res.status).toBe('EXECUTED');
    const zones = await apiService.getZonesSummary();
    const z101 = zones.find((z) => z.zone_id === 'ZONE-101');
    expect(z101.actuator_state.pump_active).toBe(true);
  });

  it('dispatches RESET_ALERTS command safely unlatching state', async () => {
    const res = await apiService.dispatchControlCommand({
      action: ACTUATOR_ACTIONS.RESET_ALERTS,
    });

    expect(res.status).toBe('EXECUTED');
    const zones = await apiService.getZonesSummary();
    expect(zones.every((z) => !z.actuator_state.pump_active)).toBe(true);
  });

  it('triggers simulation fire scenario and verifies spike in state', async () => {
    apiService.startSimulationScenario('FIRE_SPIKE_ZONE_101');

    const zones = await apiService.getZonesSummary();
    const z101 = zones.find((z) => z.zone_id === 'ZONE-101');
    expect(z101.system_state).toBe(SYSTEM_STATES.CRITICAL);
    expect(z101.latest_readings.flame_detected).toBe(true);
    expect(z101.latest_readings.temperature).toBeGreaterThan(70);

    const alarms = await apiService.getActiveAlarms();
    const critAlarm = alarms.find((a) => a.severity === 'CRITICAL');
    expect(critAlarm).toBeDefined();

    // Reset simulation
    apiService.stopSimulationScenario();
    const resetZones = await apiService.getZonesSummary();
    const resetZ101 = resetZones.find((z) => z.zone_id === 'ZONE-101');
    expect(resetZ101.system_state).toBe(SYSTEM_STATES.NORMAL);
  });
});
