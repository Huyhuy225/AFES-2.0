import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ZoneCard from '../components/ZoneCard';
import { SYSTEM_STATES } from '../contracts/afesContracts';

describe('ZoneCard Component Tests', () => {
  const normalZone = {
    zone_id: 'ZONE-101',
    room_code: 'ROOM-101',
    name: 'Server Equipment Room',
    floor: 1,
    system_state: SYSTEM_STATES.NORMAL,
    active_alarm_count: 0,
    latest_readings: {
      temperature: 24.5,
      humidity: 48.0,
      smoke_ppm: 45.0,
      flame_detected: false,
      ai_inferred_fire_risk: 0.05,
    },
    actuator_state: {
      buzzer_active: false,
      pump_active: false,
    },
    node_count: 2,
  };

  const criticalZone = {
    zone_id: 'ZONE-999',
    room_code: 'ROOM-999',
    name: 'Hazard Sector',
    floor: 2,
    system_state: SYSTEM_STATES.CRITICAL,
    active_alarm_count: 2,
    latest_readings: {
      temperature: 78.4,
      humidity: 20.0,
      smoke_ppm: 890.0,
      flame_detected: true,
      ai_inferred_fire_risk: 0.95,
    },
    actuator_state: {
      buzzer_active: true,
      pump_active: true,
    },
    node_count: 1,
  };

  it('renders normal zone with readings and safe indicators', () => {
    render(<ZoneCard zone={normalZone} />);
    expect(screen.getByText('ZONE-101')).toBeInTheDocument();
    expect(screen.getByText('Server Equipment Room')).toBeInTheDocument();
    expect(screen.getByText('NORMAL')).toBeInTheDocument();
    expect(screen.getByText('24.5')).toBeInTheDocument();
    expect(screen.getByText('45')).toBeInTheDocument();
    expect(screen.getByText('CLEAR')).toBeInTheDocument();
    expect(screen.getByText('Pump: OFF')).toBeInTheDocument();
    expect(screen.getByText('Siren: OFF')).toBeInTheDocument();
  });

  it('renders critical fire alarm state with flame detected and actuators active', () => {
    render(<ZoneCard zone={criticalZone} />);
    expect(screen.getByText('Hazard Sector')).toBeInTheDocument();
    expect(screen.getByText('FIRE ALARM')).toBeInTheDocument();
    expect(screen.getByText('78.4')).toBeInTheDocument();
    expect(screen.getByText('890')).toBeInTheDocument();
    expect(screen.getByText('DETECTED')).toBeInTheDocument();
    expect(screen.getByText('Pump: ON')).toBeInTheDocument();
    expect(screen.getByText('Siren: ON')).toBeInTheDocument();
    expect(screen.getByText('2 Alarms')).toBeInTheDocument();
    expect(screen.getByText('95%')).toBeInTheDocument();
  });
});
