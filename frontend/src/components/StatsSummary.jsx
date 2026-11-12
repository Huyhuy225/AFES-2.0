import React from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Cpu,
  Layers,
  Droplet,
  Volume2,
} from 'lucide-react';
import { SYSTEM_STATES } from '../contracts/afesContracts';

export const StatsSummary = ({ zones = [], devices = [], alarms = [] }) => {
  const activeAlarmCount = alarms.length;
  const criticalAlarmCount = alarms.filter((a) => a.severity === 'CRITICAL').length;
  const onlineDeviceCount = devices.filter((d) => d.status === 'ONLINE').length;
  const totalZonesCount = zones.length;

  const isAnyPumpActive = zones.some((z) => z.actuator_state?.pump_active);
  const isAnyBuzzerActive = zones.some((z) => z.actuator_state?.buzzer_active);

  const globalStatus = criticalAlarmCount > 0
    ? SYSTEM_STATES.CRITICAL
    : activeAlarmCount > 0
    ? SYSTEM_STATES.WARNING
    : SYSTEM_STATES.NORMAL;

  return (
    <section className="stats-kpi-grid" data-testid="stats-summary">
      <article className={`kpi-card glass-panel kpi-card--${globalStatus.toLowerCase()}`}>
        <div className="kpi-card__head">
          <span className="kpi-card__label">System Safety Status</span>
          {globalStatus === SYSTEM_STATES.NORMAL ? (
            <ShieldCheck size={20} className="kpi-icon kpi-icon--safe" />
          ) : (
            <ShieldAlert size={20} className="kpi-icon kpi-icon--alert" />
          )}
        </div>
        <div className="kpi-card__body">
          <div className="kpi-card__value">{globalStatus}</div>
          <div className="kpi-card__sub">
            {globalStatus === SYSTEM_STATES.NORMAL
              ? 'All monitored sectors nominal'
              : `${activeAlarmCount} active security condition(s)`}
          </div>
        </div>
      </article>

      <article className="kpi-card glass-panel">
        <div className="kpi-card__head">
          <span className="kpi-card__label">Active Alarms</span>
          <ShieldAlert size={20} className={activeAlarmCount > 0 ? 'kpi-icon--alert' : 'kpi-icon--muted'} />
        </div>
        <div className="kpi-card__body">
          <div className="kpi-card__value">
            <span className={activeAlarmCount > 0 ? 'text-amber' : ''}>{activeAlarmCount}</span>
            {criticalAlarmCount > 0 && (
              <span className="kpi-badge-critical">{criticalAlarmCount} Critical</span>
            )}
          </div>
          <div className="kpi-card__sub">Pending operator action</div>
        </div>
      </article>

      <article className="kpi-card glass-panel">
        <div className="kpi-card__head">
          <span className="kpi-card__label">Edge Nodes Online</span>
          <Cpu size={20} className="kpi-icon--neutral" />
        </div>
        <div className="kpi-card__body">
          <div className="kpi-card__value">
            {onlineDeviceCount} <span className="kpi-card__denom">/ {devices.length}</span>
          </div>
          <div className="kpi-card__sub">ESP32-S3 sensing fleet</div>
        </div>
      </article>

      <article className="kpi-card glass-panel">
        <div className="kpi-card__head">
          <span className="kpi-card__label">Facility Zones</span>
          <Layers size={20} className="kpi-icon--neutral" />
        </div>
        <div className="kpi-card__body">
          <div className="kpi-card__value">{totalZonesCount}</div>
          <div className="kpi-card__sub">Mapped building sectors</div>
        </div>
      </article>

      <article className={`kpi-card glass-panel ${isAnyPumpActive ? 'kpi-card--active' : ''}`}>
        <div className="kpi-card__head">
          <span className="kpi-card__label">Suppression Pump</span>
          <Droplet size={20} className={isAnyPumpActive ? 'text-blue' : 'kpi-icon--muted'} />
        </div>
        <div className="kpi-card__body">
          <div className="kpi-card__value">
            {isAnyPumpActive ? 'ENERGIZED' : 'STANDBY'}
          </div>
          <div className="kpi-card__sub">
            {isAnyPumpActive ? 'Fire water valve open' : 'Ready on standby'}
          </div>
        </div>
      </article>

      <article className={`kpi-card glass-panel ${isAnyBuzzerActive ? 'kpi-card--active' : ''}`}>
        <div className="kpi-card__head">
          <span className="kpi-card__label">Warning Siren</span>
          <Volume2 size={20} className={isAnyBuzzerActive ? 'text-amber' : 'kpi-icon--muted'} />
        </div>
        <div className="kpi-card__body">
          <div className="kpi-card__value">
            {isAnyBuzzerActive ? 'SOUNDING' : 'SILENCED'}
          </div>
          <div className="kpi-card__sub">
            {isAnyBuzzerActive ? 'Acoustic siren active' : 'Normal acoustic level'}
          </div>
        </div>
      </article>
    </section>
  );
};

export default StatsSummary;
