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

  it('renders calm neutral default Stage A state with no active alarm/warning and all normal zones', async () => {
    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('All monitored sectors nominal')).toBeInTheDocument();
      expect(screen.getByText('Server Equipment Room')).toBeInTheDocument();
    });

    // KPI Summary checks: 1 in KPI card + 4 in zone cards = 5 NORMAL labels
    const normalLabels = screen.getAllByText('NORMAL');
    expect(normalLabels.length).toBe(5);

    // Verify all 4 default zones are present and nominal
    expect(screen.getByText('Server Equipment Room')).toBeInTheDocument();
    expect(screen.getByText('High-Density Battery Vault')).toBeInTheDocument();
    expect(screen.getByText('Chemical Storage Lab')).toBeInTheDocument();
    expect(screen.getByText('Executive Operations Center')).toBeInTheDocument();

    // Alarms tab should display clean empty state
    fireEvent.click(screen.getByTestId('tab-alarms'));
    await waitFor(() => {
      expect(screen.getByText('All Systems Nominal')).toBeInTheDocument();
      expect(screen.getByText('0 active')).toBeInTheDocument();
    });
  });

  it('injects deliberate simulation incident with visible [SIMULATED - STAGE A] tag and reversible reset', async () => {
    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('All monitored sectors nominal')).toBeInTheDocument();
      expect(screen.getByText('Server Equipment Room')).toBeInTheDocument();
    });

    // Navigate to controls console
    fireEvent.click(screen.getByTestId('tab-controls'));
    await waitFor(() => {
      expect(screen.getByTestId('btn-sim-fire')).toBeInTheDocument();
    });

    // Trigger deliberate critical fire simulation
    fireEvent.click(screen.getByTestId('btn-sim-fire'));

    // Check banner displays [SIMULATED - STAGE A] marker and global status transitions to CRITICAL
    await waitFor(() => {
      expect(screen.getByTestId('sim-scenario-banner')).toBeInTheDocument();
      expect(screen.getByText(/\[SIMULATED - STAGE A\] Active Scenario:/i)).toBeInTheDocument();
      expect(screen.getByText('CRITICAL')).toBeInTheDocument();
    });

    // Reset simulation back to neutral baseline via banner button
    fireEvent.click(screen.getByTestId('btn-banner-reset-sim'));

    await waitFor(() => {
      expect(screen.queryByTestId('sim-scenario-banner')).not.toBeInTheDocument();
      expect(screen.getByText('All monitored sectors nominal')).toBeInTheDocument();
      expect(screen.getAllByText('NORMAL').length).toBeGreaterThanOrEqual(1);
    });

    // Switch back to overview tab to verify all 4 zone cards restored to NORMAL
    fireEvent.click(screen.getByTestId('tab-overview'));
    await waitFor(() => {
      expect(screen.getAllByText('NORMAL').length).toBe(5);
    });
  });

  it('handles alarm acknowledgment workflow cleanly', async () => {
    // Deliberately start simulated scenario to generate an alarm
    apiService.startSimulationScenario('FIRE_SPIKE_ZONE_101');
    render(<Dashboard />);

    // Go to alarms tab
    fireEvent.click(screen.getByTestId('tab-alarms'));
    let ackButton;
    await waitFor(() => {
      const ackButtons = screen.getAllByRole('button', { name: /acknowledge/i });
      expect(ackButtons.length).toBeGreaterThan(0);
      ackButton = ackButtons[0];
    });

    // Click Acknowledge
    fireEvent.click(ackButton);

    await waitFor(() => {
      expect(screen.getByText('ACKNOWLEDGED')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /resolve & clear/i })).toBeInTheDocument();
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
    // Start simulation scenario to provide an active alarm
    apiService.startSimulationScenario('FIRE_SPIKE_ZONE_101');
    render(<Dashboard />);

    // Go to alarms tab
    fireEvent.click(screen.getByTestId('tab-alarms'));
    let ackButton;
    await waitFor(() => {
      const ackButtons = screen.getAllByRole('button', { name: /acknowledge/i });
      expect(ackButtons.length).toBeGreaterThan(0);
      ackButton = ackButtons[0];
    });

    // Mock acknowledgeAlarm to reject
    const originalAcknowledge = apiService.acknowledgeAlarm.bind(apiService);
    apiService.acknowledgeAlarm = async () => {
      throw new Error('Connection refused: Backend REST offline');
    };

    try {
      fireEvent.click(ackButton);

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
