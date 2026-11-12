import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, beforeEach } from 'vitest';
import Dashboard from '../pages/Dashboard';
import apiService from '../api/sensorApi';

describe('Dashboard Component Integration Tests', () => {
  beforeEach(() => {
    apiService.resetMockStore();
    apiService.setMockMode(true);
  });

  it('renders header, brand name, and Stage A simulation tag', async () => {
    render(<Dashboard />);
    expect(screen.getByText('AFES')).toBeInTheDocument();
    expect(screen.getByText('2.0')).toBeInTheDocument();
    expect(screen.getByText(/\[SIMULATED - STAGE A\]/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByTestId('stats-summary')).toBeInTheDocument();
    });
  });

  it('renders stats summary KPIs and all 5 navigation tabs', async () => {
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('System Safety Status')).toBeInTheDocument();
      expect(screen.getByText('Active Alarms')).toBeInTheDocument();
      expect(screen.getByText('Edge Nodes Online')).toBeInTheDocument();
      expect(screen.getByText('Facility Zones')).toBeInTheDocument();
    });

    expect(screen.getByTestId('tab-overview')).toBeInTheDocument();
    expect(screen.getByTestId('tab-devices')).toBeInTheDocument();
    expect(screen.getByTestId('tab-telemetry')).toBeInTheDocument();
    expect(screen.getByTestId('tab-alarms')).toBeInTheDocument();
    expect(screen.getByTestId('tab-controls')).toBeInTheDocument();
  });

  it('navigates through tabs and displays respective views', async () => {
    render(<Dashboard />);

    // Overview is active by default
    await waitFor(() => {
      expect(screen.getByTestId('view-overview')).toBeInTheDocument();
      expect(screen.getByText('Server Equipment Room')).toBeInTheDocument();
    });

    // Switch to Sensing Fleet tab
    fireEvent.click(screen.getByTestId('tab-devices'));
    await waitFor(() => {
      expect(screen.getByTestId('view-devices')).toBeInTheDocument();
      expect(screen.getByText('Hardware Sensing Fleet & Edge Nodes')).toBeInTheDocument();
      expect(screen.getByText('ESP32S3-YOLO-01')).toBeInTheDocument();
    });

    // Switch to Telemetry Trends tab
    fireEvent.click(screen.getByTestId('tab-telemetry'));
    await waitFor(() => {
      expect(screen.getByTestId('view-telemetry')).toBeInTheDocument();
      expect(screen.getByTestId('telemetry-chart')).toBeInTheDocument();
    });

    // Switch to Alarm Triage tab
    fireEvent.click(screen.getByTestId('tab-alarms'));
    await waitFor(() => {
      expect(screen.getByTestId('view-alarms')).toBeInTheDocument();
      expect(screen.getByText('Emergency Alarm Triage')).toBeInTheDocument();
    });

    // Switch to Actuator Controls tab
    fireEvent.click(screen.getByTestId('tab-controls'));
    await waitFor(() => {
      expect(screen.getByTestId('view-controls')).toBeInTheDocument();
      expect(screen.getByTestId('control-console')).toBeInTheDocument();
    });
  });

  it('handles alarm acknowledgment workflow cleanly', async () => {
    render(<Dashboard />);

    // Go to alarms tab
    fireEvent.click(screen.getByTestId('tab-alarms'));
    await waitFor(() => {
      expect(screen.getByTestId('btn-ack-evt-smoke-102-001')).toBeInTheDocument();
    });

    // Click Acknowledge
    fireEvent.click(screen.getByTestId('btn-ack-evt-smoke-102-001'));

    await waitFor(() => {
      expect(screen.getByText('ACKNOWLEDGED')).toBeInTheDocument();
      expect(screen.getByTestId('btn-resolve-evt-smoke-102-001')).toBeInTheDocument();
    });
  });

  it('toggles mock / live mode via header button', async () => {
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('Mock / Simulated Stream')).toBeInTheDocument();
    });

    const toggleBtn = screen.getByText('Switch to Live API');
    fireEvent.click(toggleBtn);

    await waitFor(() => {
      expect(screen.getByText('Switch to Mock Simulator')).toBeInTheDocument();
    });
  });

  it('displays error banner when live alarm acknowledgment fails without simulating success', async () => {
    render(<Dashboard />);

    // Go to alarms tab
    fireEvent.click(screen.getByTestId('tab-alarms'));
    await waitFor(() => {
      expect(screen.getByTestId('btn-ack-evt-smoke-102-001')).toBeInTheDocument();
    });

    // Mock acknowledgeAlarm to reject
    const originalAcknowledge = apiService.acknowledgeAlarm.bind(apiService);
    apiService.acknowledgeAlarm = async () => {
      throw new Error('Connection refused: Backend REST offline');
    };

    try {
      fireEvent.click(screen.getByTestId('btn-ack-evt-smoke-102-001'));

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
        expect(screen.getByText(/Alarm acknowledgment failed/i)).toBeInTheDocument();
        // Alarm must NOT be acknowledged
        expect(screen.queryByText('ACKNOWLEDGED')).not.toBeInTheDocument();
      });
    } finally {
      apiService.acknowledgeAlarm = originalAcknowledge;
    }
  });
});
