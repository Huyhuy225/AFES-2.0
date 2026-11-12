import React from 'react';
import {
  Thermometer,
  CloudFog,
  Droplets,
  Flame,
  Volume2,
  Droplet,
  AlertTriangle,
  CheckCircle2,
  BrainCircuit,
} from 'lucide-react';
import { SYSTEM_STATES, THRESHOLDS } from '../contracts/afesContracts';

export const ZoneCard = ({ zone, onSelectZone }) => {
  const {
    zone_id,
    room_code,
    name,
    floor,
    system_state = SYSTEM_STATES.NORMAL,
    active_alarm_count = 0,
    latest_readings = {},
    actuator_state = {},
    node_count = 1,
  } = zone;

  const temp = latest_readings.temperature ?? 0;
  const smoke = latest_readings.smoke_ppm ?? 0;
  const humidity = latest_readings.humidity ?? 0;
  const flameDetected = Boolean(latest_readings.flame_detected);
  const fireRisk = latest_readings.ai_inferred_fire_risk ?? 0;

  const isTempWarning = temp >= THRESHOLDS.TEMP_WARNING_C;
  const isSmokeWarning = smoke >= THRESHOLDS.SMOKE_WARNING_PPM;

  const stateClass =
    system_state === SYSTEM_STATES.CRITICAL
      ? 'zone-card--critical'
      : system_state === SYSTEM_STATES.WARNING
      ? 'zone-card--warning'
      : 'zone-card--normal';

  return (
    <article
      className={`zone-card glass-panel ${stateClass}`}
      data-testid={`zone-card-${zone_id}`}
      onClick={() => onSelectZone && onSelectZone(zone)}
    >
      <div className="zone-card__head">
        <div className="zone-identity">
          <div className="zone-code-tag">
            <span>{zone_id}</span>
            <span className="room-code">({room_code})</span>
          </div>
          <h3 className="zone-name">{name}</h3>
          <div className="zone-meta">Floor {floor} &bull; {node_count} sensing node(s)</div>
        </div>

        <div className="zone-state-badge">
          {system_state === SYSTEM_STATES.NORMAL ? (
            <span className="badge badge--safe">
              <CheckCircle2 size={13} />
              <span>NORMAL</span>
            </span>
          ) : system_state === SYSTEM_STATES.WARNING ? (
            <span className="badge badge--warning">
              <AlertTriangle size={13} />
              <span>WARNING</span>
            </span>
          ) : (
            <span className="badge badge--critical">
              <Flame size={13} />
              <span>FIRE ALARM</span>
            </span>
          )}
        </div>
      </div>

      <div className="zone-readings-grid">
        <div className={`reading-metric ${isTempWarning ? 'reading-metric--alert' : ''}`}>
          <div className="reading-label">
            <Thermometer size={14} />
            <span>Temp</span>
          </div>
          <div className="reading-value">
            <strong>{temp.toFixed(1)}</strong>
            <span className="unit">&deg;C</span>
          </div>
        </div>

        <div className={`reading-metric ${isSmokeWarning ? 'reading-metric--alert' : ''}`}>
          <div className="reading-label">
            <CloudFog size={14} />
            <span>Smoke</span>
          </div>
          <div className="reading-value">
            <strong>{smoke.toFixed(0)}</strong>
            <span className="unit">PPM</span>
          </div>
        </div>

        <div className="reading-metric">
          <div className="reading-label">
            <Droplets size={14} />
            <span>Humidity</span>
          </div>
          <div className="reading-value">
            <strong>{humidity.toFixed(0)}</strong>
            <span className="unit">%</span>
          </div>
        </div>

        <div className={`reading-metric ${flameDetected ? 'reading-metric--danger' : ''}`}>
          <div className="reading-label">
            <Flame size={14} />
            <span>Flame</span>
          </div>
          <div className="reading-value flame-status">
            {flameDetected ? (
              <span className="flame-active">DETECTED</span>
            ) : (
              <span className="flame-clear">CLEAR</span>
            )}
          </div>
        </div>
      </div>

      <div className="zone-fire-risk">
        <div className="fire-risk-header">
          <div className="fire-risk-label">
            <BrainCircuit size={13} />
            <span>TinyML Fire Probability</span>
          </div>
          <span className="fire-risk-percent">{(fireRisk * 100).toFixed(0)}%</span>
        </div>
        <div className="fire-risk-bar-track">
          <div
            className={`fire-risk-bar-fill ${
              fireRisk >= 0.7 ? 'bar-critical' : fireRisk >= 0.4 ? 'bar-warning' : 'bar-normal'
            }`}
            style={{ width: `${Math.min(100, Math.max(0, fireRisk * 100))}%` }}
          />
        </div>
      </div>

      <div className="zone-card__footer">
        <div className="actuator-chips">
          <span
            className={`actuator-chip ${
              actuator_state.pump_active ? 'actuator-chip--active' : ''
            }`}
            title="Suppression relay"
          >
            <Droplet size={12} />
            <span>Pump: {actuator_state.pump_active ? 'ON' : 'OFF'}</span>
          </span>

          <span
            className={`actuator-chip ${
              actuator_state.buzzer_active ? 'actuator-chip--active' : ''
            }`}
            title="Siren acoustic buzzer"
          >
            <Volume2 size={12} />
            <span>Siren: {actuator_state.buzzer_active ? 'ON' : 'OFF'}</span>
          </span>
        </div>

        {active_alarm_count > 0 && (
          <div className="alarm-counter-pill">
            {active_alarm_count} Alarm{active_alarm_count > 1 ? 's' : ''}
          </div>
        )}
      </div>
    </article>
  );
};

export default ZoneCard;
