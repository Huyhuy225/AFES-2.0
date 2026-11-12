import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import DeviceList from '../components/DeviceList';
import { DEVICE_STATUS, SENSOR_HEALTH } from '../contracts/afesContracts';

describe('DeviceList Component Tests', () => {
  const mockDevices = [
    {
      device_id: 'ESP32S3-YOLO-01',
      zone_id: 'ZONE-101',
      room_code: 'ROOM-101',
      device_type: 'YOLO_UNO_S3',
      firmware_version: '2.1.0-stageA',
      status: DEVICE_STATUS.ONLINE,
      sensor_health: SENSOR_HEALTH.HEALTHY,
      rssi_dbm: -62,
      uptime_seconds: 7200,
      tinyml_inference_latency_ms: 24,
      is_simulated: true,
    },
    {
      device_id: 'ESP32S3-YOLO-04',
      zone_id: 'ZONE-104',
      room_code: 'ROOM-301',
      device_type: 'YOLO_UNO_S3',
      firmware_version: '2.0.8-stageA',
      status: DEVICE_STATUS.OFFLINE,
      sensor_health: SENSOR_HEALTH.ERROR,
      rssi_dbm: -89,
      uptime_seconds: 0,
      tinyml_inference_latency_ms: 0,
      is_simulated: true,
    },
  ];

  it('renders device cards and simulation chips', () => {
    render(<DeviceList devices={mockDevices} />);
    expect(screen.getByText('ESP32S3-YOLO-01')).toBeInTheDocument();
    expect(screen.getByText('ESP32S3-YOLO-04')).toBeInTheDocument();
    expect(screen.getAllByText(/\[SIMULATED - STAGE A\]/i).length).toBe(2);
    expect(screen.getAllByText('ONLINE').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('OFFLINE').length).toBeGreaterThanOrEqual(1);
  });

  it('filters devices by status', () => {
    render(<DeviceList devices={mockDevices} />);

    // Click OFFLINE filter button
    const offlineBtn = screen.getByRole('button', { name: 'OFFLINE' });
    fireEvent.click(offlineBtn);

    expect(screen.queryByText('ESP32S3-YOLO-01')).not.toBeInTheDocument();
    expect(screen.getByText('ESP32S3-YOLO-04')).toBeInTheDocument();
  });

  it('filters devices by search query', () => {
    render(<DeviceList devices={mockDevices} />);

    const searchInput = screen.getByPlaceholderText('Search device ID or zone...');
    fireEvent.change(searchInput, { target: { value: 'YOLO-01' } });

    expect(screen.getByText('ESP32S3-YOLO-01')).toBeInTheDocument();
    expect(screen.queryByText('ESP32S3-YOLO-04')).not.toBeInTheDocument();
  });

  it('shows empty state when search finds no devices', () => {
    render(<DeviceList devices={mockDevices} />);

    const searchInput = screen.getByPlaceholderText('Search device ID or zone...');
    fireEvent.change(searchInput, { target: { value: 'NON_EXISTENT' } });

    expect(screen.getByText('No Devices Found')).toBeInTheDocument();
  });
});
