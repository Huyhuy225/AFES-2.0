import React, { useState } from 'react';
import {
  Droplet,
  Volume2,
  RotateCcw,
  AlertOctagon,
  ShieldAlert,
  Play,
  RotateCw,
  Clock,
  CheckCircle2,
  FlaskConical,
} from 'lucide-react';
import { ACTUATOR_ACTIONS, STAGE_A_SIMULATION_TAG } from '../contracts/afesContracts';

export const ControlConsole = ({
  onDispatchCommand,
  onStartScenario,
  onStopScenario,
  activeScenario = null,
  isActing = false,
  zones = [],
}) => {
  const [selectedZone, setSelectedZone] = useState('');
  const [confirmModal, setConfirmModal] = useState(null);
  const [actionHistory, setActionHistory] = useState([]);

  const handleActionClick = (action, label, requiresConfirm = true) => {
    if (requiresConfirm) {
      setConfirmModal({ action, label });
    } else {
      executeAction(action);
    }
  };

  const executeAction = async (action) => {
    setConfirmModal(null);
    const payload = {
      target_zone_id: selectedZone || null,
      action,
      parameters: action === ACTUATOR_ACTIONS.PUMP_ON ? { duration_ms: 10000 } : {},
      idempotency_key: `idemp-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    };

    try {
      const res = await onDispatchCommand(payload);
      setActionHistory((prev) => [
        {
          id: res.command_id || Date.now(),
          action,
          zone: selectedZone || 'ALL_ZONES',
          status: 'SUCCESS',
          time: new Date().toLocaleTimeString(),
          message: res.message || 'Command executed successfully',
        },
        ...prev.slice(0, 9),
      ]);
    } catch (err) {
      setActionHistory((prev) => [
        {
          id: Date.now(),
          action,
          zone: selectedZone || 'ALL_ZONES',
          status: 'FAILED',
          time: new Date().toLocaleTimeString(),
          message: err.message,
        },
        ...prev.slice(0, 9),
      ]);
    }
  };

  return (
    <div className="control-console-container" data-testid="control-console">
      <div className="console-warning-banner glass-panel">
        <div className="warning-icon">
          <AlertOctagon size={22} className="text-amber" />
        </div>
        <div className="warning-text">
          <strong>Restricted Actuator Dispatch Console</strong>
          <p>
            Manual actuator overrides execute direct hardware / simulated relay commands. Commands
            are audited and logged under administrative role boundary.
          </p>
        </div>
      </div>

      <div className="console-grid">
        {/* Left Column: Command Groups */}
        <div className="console-main glass-panel">
          <div className="console-zone-picker">
            <label htmlFor="zone-select" className="control-label">
              Target Zone Scope:
            </label>
            <select
              id="zone-select"
              className="zone-select-input"
              value={selectedZone}
              onChange={(e) => setSelectedZone(e.target.value)}
            >
              <option value="">All Zones (Broadcast)</option>
              {zones.map((z) => (
                <option key={z.zone_id} value={z.zone_id}>
                  {z.zone_id} - {z.name} (Room {z.room_code})
                </option>
              ))}
            </select>
          </div>

          <div className="command-groups">
            {/* Water Suppression Group */}
            <div className="command-group">
              <h4 className="command-group-title">
                <Droplet size={16} className="text-blue" />
                <span>Fire Suppression Pump</span>
              </h4>
              <div className="button-row">
                <button
                  type="button"
                  className="btn-cmd btn-cmd--primary"
                  disabled={isActing}
                  onClick={() =>
                    handleActionClick(ACTUATOR_ACTIONS.PUMP_ON, 'Energize Water Pump (10s)')
                  }
                  data-testid="btn-pump-on"
                >
                  <Droplet size={15} />
                  <span>Engage Pump (10s)</span>
                </button>

                <button
                  type="button"
                  className="btn-cmd btn-cmd--neutral"
                  disabled={isActing}
                  onClick={() =>
                    handleActionClick(ACTUATOR_ACTIONS.PUMP_OFF, 'Stop Water Pump', false)
                  }
                  data-testid="btn-pump-off"
                >
                  <span>Stop Pump</span>
                </button>
              </div>
            </div>

            {/* Acoustic Siren Group */}
            <div className="command-group">
              <h4 className="command-group-title">
                <Volume2 size={16} className="text-amber" />
                <span>Acoustic Warning Siren</span>
              </h4>
              <div className="button-row">
                <button
                  type="button"
                  className="btn-cmd btn-cmd--warning"
                  disabled={isActing}
                  onClick={() =>
                    handleActionClick(ACTUATOR_ACTIONS.TEST_ALARM, 'Emit Siren Acoustic Test')
                  }
                  data-testid="btn-test-alarm"
                >
                  <Volume2 size={15} />
                  <span>Test Siren Pulse</span>
                </button>
              </div>
            </div>

            {/* System Reset & Safety Group */}
            <div className="command-group">
              <h4 className="command-group-title">
                <RotateCcw size={16} className="text-emerald" />
                <span>Synchronized Reset & Safety Loop</span>
              </h4>
              <div className="button-row">
                <button
                  type="button"
                  className="btn-cmd btn-cmd--success"
                  disabled={isActing}
                  onClick={() =>
                    handleActionClick(
                      ACTUATOR_ACTIONS.RESET_ALERTS,
                      'Synchronized Alert Reset (RESET_ALERTS)'
                    )
                  }
                  data-testid="btn-reset-system"
                >
                  <RotateCcw size={15} />
                  <span>RESET_ALERTS (Unlatch)</span>
                </button>

                <button
                  type="button"
                  className="btn-cmd btn-cmd--danger"
                  disabled={isActing}
                  onClick={() =>
                    handleActionClick(
                      ACTUATOR_ACTIONS.EMERGENCY_SHUTDOWN,
                      'Building-Wide Emergency Evacuation Alarm'
                    )
                  }
                  data-testid="btn-emergency-shutdown"
                >
                  <ShieldAlert size={15} />
                  <span>Emergency Evac Alarm</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Stage A Simulation Injector & Audit History */}
        <div className="console-sidebar">
          {/* Stage A Simulation Controller */}
          <div className="simulation-injector-panel glass-panel">
            <div className="sim-panel-header">
              <div className="sim-title-wrap">
                <FlaskConical size={18} className="text-purple" />
                <h4 className="sim-panel-title">Stage A Simulation Lab</h4>
              </div>
              <span className="tag-chip tag-chip--sim">{STAGE_A_SIMULATION_TAG}</span>
            </div>
            <p className="sim-panel-desc">
              Inject synthetic environmental anomalies to verify end-to-end dashboard reactivity
              without physical fire or hardware risk.
            </p>

            <div className="sim-buttons">
              <button
                type="button"
                className={`btn-sim ${activeScenario === 'WARNING_SMOKE_ZONE_102' ? 'is-active' : ''}`}
                onClick={() => onStartScenario('WARNING_SMOKE_ZONE_102')}
                data-testid="btn-sim-warning"
              >
                <Play size={14} />
                <span>Simulate Warning: Zone 102 Smoke (535 PPM)</span>
              </button>

              <button
                type="button"
                className={`btn-sim ${activeScenario === 'FIRE_SPIKE_ZONE_101' ? 'is-active' : ''}`}
                onClick={() => onStartScenario('FIRE_SPIKE_ZONE_101')}
                data-testid="btn-sim-fire"
              >
                <Play size={14} />
                <span>Simulate Critical: Zone 101 Fire (75&deg;C + Flame)</span>
              </button>

              <button
                type="button"
                className="btn-sim btn-sim--reset"
                onClick={onStopScenario}
                data-testid="btn-sim-reset"
              >
                <RotateCw size={14} />
                <span>Reset Simulation to Baseline</span>
              </button>
            </div>
            {activeScenario && (
              <div className="active-sim-banner" data-testid="active-sim-indicator">
                <span className="active-sim-pulse" />
                <span className="active-sim-text">
                  Demonstration active: <strong>{activeScenario}</strong> {STAGE_A_SIMULATION_TAG}
                </span>
              </div>
            )}
          </div>

          {/* Audit Log Panel */}
          <div className="audit-log-panel glass-panel">
            <h4 className="audit-log-title">
              <Clock size={16} />
              <span>Recent Actuator Audit Log</span>
            </h4>
            {actionHistory.length === 0 ? (
              <div className="audit-empty">No commands issued in this session.</div>
            ) : (
              <div className="audit-entries">
                {actionHistory.map((entry) => (
                  <div key={entry.id} className="audit-entry">
                    <div className="audit-entry-top">
                      <span className="audit-action">{entry.action}</span>
                      <span
                        className={`audit-status-tag ${
                          entry.status === 'FAILED' ? 'audit-status--failed' : 'audit-status--success'
                        }`}
                      >
                        {entry.status}
                      </span>
                      <span className="audit-time">{entry.time}</span>
                    </div>
                    <div className="audit-entry-msg">{entry.message}</div>
                    <div className="audit-entry-scope">Scope: {entry.zone}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Safety Confirmation Modal */}
      {confirmModal && (
        <div className="modal-backdrop" data-testid="confirm-modal">
          <div className="modal-content glass-panel">
            <div className="modal-head">
              <ShieldAlert size={28} className="text-amber" />
              <h3 className="modal-title">Confirm Actuator Command</h3>
            </div>
            <p className="modal-body">
              Are you sure you want to execute <strong>{confirmModal.label}</strong>
              {selectedZone ? ` for zone ${selectedZone}` : ' across all monitored zones'}?
            </p>
            <div className="modal-actions">
              <button
                type="button"
                className="btn-modal-cancel"
                onClick={() => setConfirmModal(null)}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn-modal-confirm"
                onClick={() => executeAction(confirmModal.action)}
                data-testid="modal-confirm-btn"
              >
                Confirm & Dispatch
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ControlConsole;
