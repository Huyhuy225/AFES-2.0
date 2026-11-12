import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ControlConsole from '../components/ControlConsole';
import { ACTUATOR_ACTIONS } from '../contracts/afesContracts';

describe('ControlConsole Component Tests', () => {
  const mockZones = [
    { zone_id: 'ZONE-101', name: 'Server Room', room_code: '101' },
  ];

  it('renders control buttons and safety banner', () => {
    render(
      <ControlConsole
        onDispatchCommand={vi.fn()}
        onStartScenario={vi.fn()}
        onStopScenario={vi.fn()}
        zones={mockZones}
      />
    );

    expect(screen.getByText('Restricted Actuator Dispatch Console')).toBeInTheDocument();
    expect(screen.getByTestId('btn-pump-on')).toBeInTheDocument();
    expect(screen.getByTestId('btn-pump-off')).toBeInTheDocument();
    expect(screen.getByTestId('btn-test-alarm')).toBeInTheDocument();
    expect(screen.getByTestId('btn-reset-system')).toBeInTheDocument();
    expect(screen.getByTestId('btn-emergency-shutdown')).toBeInTheDocument();
    expect(screen.getByTestId('btn-sim-warning')).toBeInTheDocument();
    expect(screen.getByTestId('btn-sim-fire')).toBeInTheDocument();
    expect(screen.getByTestId('btn-sim-reset')).toBeInTheDocument();
  });

  it('triggers confirmation modal before dispatching high-impact command', async () => {
    const dispatchMock = vi.fn().mockResolvedValue({ command_id: 'cmd-1', message: 'Pump active' });
    render(
      <ControlConsole
        onDispatchCommand={dispatchMock}
        onStartScenario={vi.fn()}
        onStopScenario={vi.fn()}
        zones={mockZones}
      />
    );

    // Click engage pump
    fireEvent.click(screen.getByTestId('btn-pump-on'));

    // Confirmation modal should appear
    expect(screen.getByTestId('confirm-modal')).toBeInTheDocument();
    expect(screen.getByText(/Are you sure you want to execute/i)).toBeInTheDocument();

    // Confirm execution
    fireEvent.click(screen.getByTestId('modal-confirm-btn'));

    await waitFor(() => {
      expect(dispatchMock).toHaveBeenCalledWith(
        expect.objectContaining({
          action: ACTUATOR_ACTIONS.PUMP_ON,
        })
      );
    });
  });

  it('triggers simulation scenario start and reset callbacks', () => {
    const startMock = vi.fn();
    const stopMock = vi.fn();
    render(
      <ControlConsole
        onDispatchCommand={vi.fn()}
        onStartScenario={startMock}
        onStopScenario={stopMock}
        zones={mockZones}
      />
    );

    fireEvent.click(screen.getByTestId('btn-sim-warning'));
    expect(startMock).toHaveBeenCalledWith('WARNING_SMOKE_ZONE_102');

    fireEvent.click(screen.getByTestId('btn-sim-fire'));
    expect(startMock).toHaveBeenCalledWith('FIRE_SPIKE_ZONE_101');

    fireEvent.click(screen.getByTestId('btn-sim-reset'));
    expect(stopMock).toHaveBeenCalled();
  });
});
