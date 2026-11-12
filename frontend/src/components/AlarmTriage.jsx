import React, { useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Check,
  CheckCheck,
  Flame,
  AlertTriangle,
  Info,
  Clock,
  MapPin,
  Cpu,
} from 'lucide-react';
import { EVENT_SEVERITY } from '../contracts/afesContracts';
import EmptyState from './EmptyState';

export const AlarmTriage = ({
  alarms = [],
  onAcknowledgeAlarm,
  onResolveAlarm,
  isActing = false,
}) => {
  const [severityFilter, setSeverityFilter] = useState('ALL');

  const filteredAlarms = alarms.filter((a) => {
    if (severityFilter === 'ALL') return true;
    return a.severity === severityFilter;
  });

  return (
    <div className="alarm-triage-container" data-testid="alarm-triage">
      <div className="alarm-triage-toolbar">
        <div className="toolbar-title-wrap">
          <h3 className="section-title">Emergency Alarm Triage</h3>
          <span className="alarms-counter-badge">{alarms.length} active</span>
        </div>

        <div className="filter-buttons">
          {['ALL', EVENT_SEVERITY.CRITICAL, EVENT_SEVERITY.WARNING, EVENT_SEVERITY.INFO].map(
            (sev) => (
              <button
                key={sev}
                type="button"
                className={`filter-btn ${severityFilter === sev ? 'is-active' : ''}`}
                onClick={() => setSeverityFilter(sev)}
              >
                {sev}
              </button>
            )
          )}
        </div>
      </div>

      {filteredAlarms.length === 0 ? (
        <EmptyState
          title="All Systems Nominal"
          description="There are zero active alarms matching the current filter. All monitored zones are operating within safety parameters."
          icon={ShieldCheck}
        />
      ) : (
        <div className="alarms-feed">
          {filteredAlarms.map((alarm) => {
            const isCritical = alarm.severity === EVENT_SEVERITY.CRITICAL;
            const isAcknowledged = alarm.ack_status === 'ACKNOWLEDGED';

            return (
              <article
                key={alarm.event_id}
                className={`alarm-entry-card glass-panel ${
                  isCritical ? 'alarm-entry--critical' : 'alarm-entry--warning'
                } ${isAcknowledged ? 'alarm-entry--ack' : ''}`}
                data-testid={`alarm-card-${alarm.event_id}`}
              >
                <div className="alarm-entry__left">
                  <div className="alarm-severity-icon">
                    {isCritical ? (
                      <Flame size={22} className="text-red animate-pulse" />
                    ) : (
                      <AlertTriangle size={22} className="text-amber" />
                    )}
                  </div>
                  <div>
                    <div className="alarm-header-row">
                      <span className={`badge badge--${alarm.severity.toLowerCase()}`}>
                        {alarm.severity}
                      </span>
                      <h4 className="alarm-type-text">{alarm.event_type}</h4>
                      <span className="alarm-id-text">ID: {alarm.event_id}</span>
                    </div>

                    <div className="alarm-meta-row">
                      <span className="alarm-meta-item">
                        <MapPin size={13} />
                        <span>{alarm.zone_id} ({alarm.room_code})</span>
                      </span>
                      <span className="alarm-meta-item">
                        <Cpu size={13} />
                        <span>{alarm.device_id}</span>
                      </span>
                      <span className="alarm-meta-item">
                        <Clock size={13} />
                        <span>{new Date(alarm.timestamp_epoch_ms).toLocaleString()}</span>
                      </span>
                    </div>

                    {alarm.trigger_details && (
                      <div className="alarm-trigger-box">
                        <span className="trigger-title">Trigger Source: {alarm.trigger_source}</span>
                        <div className="trigger-tags">
                          {alarm.trigger_details.temperature_c !== undefined && (
                            <span className="trigger-tag">
                              Temp: {alarm.trigger_details.temperature_c}&deg;C (Limit: {alarm.trigger_details.temperature_threshold_c}&deg;C)
                            </span>
                          )}
                          {alarm.trigger_details.smoke_ppm !== undefined && (
                            <span className="trigger-tag">
                              Smoke: {alarm.trigger_details.smoke_ppm} PPM (Limit: {alarm.trigger_details.smoke_threshold_ppm} PPM)
                            </span>
                          )}
                          {alarm.trigger_details.flame_detected && (
                            <span className="trigger-tag trigger-tag--flame">
                              FLAME DETECTED
                            </span>
                          )}
                          {alarm.trigger_details.tinyml_fire_confidence !== undefined && (
                            <span className="trigger-tag">
                              TinyML Conf: {(alarm.trigger_details.tinyml_fire_confidence * 100).toFixed(0)}%
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {alarm.autonomous_actions_taken && alarm.autonomous_actions_taken.length > 0 && (
                      <div className="alarm-actions-taken">
                        <span className="actions-title">Edge Autonomous Safety Actions:</span>
                        {alarm.autonomous_actions_taken.map((act) => (
                          <span key={act} className="action-pill">
                            {act}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="alarm-entry__actions">
                  <div className="ack-status-badge">
                    {isAcknowledged ? (
                      <span className="badge badge--neutral">
                        <CheckCheck size={12} />
                        <span>ACKNOWLEDGED</span>
                      </span>
                    ) : (
                      <span className="badge badge--pending">
                        <span>PENDING ACK</span>
                      </span>
                    )}
                  </div>

                  {!isAcknowledged ? (
                    <button
                      type="button"
                      className="btn-ack"
                      disabled={isActing}
                      onClick={() => onAcknowledgeAlarm(alarm.event_id)}
                      data-testid={`btn-ack-${alarm.event_id}`}
                    >
                      <Check size={14} />
                      <span>Acknowledge</span>
                    </button>
                  ) : (
                    <button
                      type="button"
                      className="btn-resolve"
                      disabled={isActing}
                      onClick={() => onResolveAlarm(alarm.event_id)}
                      data-testid={`btn-resolve-${alarm.event_id}`}
                    >
                      <CheckCheck size={14} />
                      <span>Resolve & Clear</span>
                    </button>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default AlarmTriage;
