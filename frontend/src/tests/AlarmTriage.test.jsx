import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import AlarmTriage from '../components/AlarmTriage';
import { EVENT_TYPES, EVENT_SEVERITY } from '../contracts/afesContracts';

describe('AlarmTriage Component Tests', () => {
  const mockAlarms = [
    {
      event_id: 'evt-001',
      timestamp_epoch_ms: 1700000000000,
      timestamp_utc: '2026-11-12T10:00:00Z',
      device_id: 'ESP32S3-YOLO-01',
      zone_id: 'ZONE-101',
      room_code: 'ROOM-101',
      event_type: EVENT_TYPES.FIRE_ALARM_CRITICAL,
      severity: EVENT_SEVERITY.CRITICAL,
      trigger_source: 'MULTI_SENSOR_FUSION',
      trigger_details: {
        temperature_c: 65.0,
        temperature_threshold_c: 50.0,
        smoke_ppm: 850.0,
        smoke_threshold_ppm: 500.0,
        flame_detected: true,
      },
      autonomous_actions_taken: ['LOCAL_BUZZER_ACTIVE', 'LOCAL_PUMP_ENGAGED'],
      ack_status: 'PENDING',
    },
  ];

  it('renders active alarms with trigger details and action pills', () => {
    render(
      <AlarmTriage
        alarms={mockAlarms}
        onAcknowledgeAlarm={vi.fn()}
        onResolveAlarm={vi.fn()}
      />
    );

    expect(screen.getByText('FIRE_ALARM_CRITICAL')).toBeInTheDocument();
    expect(screen.getAllByText('CRITICAL').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/ID: evt-001/i)).toBeInTheDocument();
    expect(screen.getByText('FLAME DETECTED')).toBeInTheDocument();
    expect(screen.getByText('LOCAL_BUZZER_ACTIVE')).toBeInTheDocument();
    expect(screen.getByText('LOCAL_PUMP_ENGAGED')).toBeInTheDocument();
    expect(screen.getByText('PENDING ACK')).toBeInTheDocument();
  });

  it('invokes onAcknowledgeAlarm callback when clicking Acknowledge button', () => {
    const handleAck = vi.fn();
    render(
      <AlarmTriage
        alarms={mockAlarms}
        onAcknowledgeAlarm={handleAck}
        onResolveAlarm={vi.fn()}
      />
    );

    const ackBtn = screen.getByTestId('btn-ack-evt-001');
    fireEvent.click(ackBtn);
    expect(handleAck).toHaveBeenCalledWith('evt-001');
  });

  it('shows empty state when no alarms are active', () => {
    render(
      <AlarmTriage
        alarms={[]}
        onAcknowledgeAlarm={vi.fn()}
        onResolveAlarm={vi.fn()}
      />
    );

    expect(screen.getByText('All Systems Nominal')).toBeInTheDocument();
  });
});
