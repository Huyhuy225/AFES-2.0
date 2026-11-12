import React, { useState, useMemo } from 'react';
import {
  Cpu,
  Wifi,
  WifiOff,
  Clock,
  Zap,
  Activity,
  CheckCircle2,
  AlertCircle,
  XCircle,
  Search,
} from 'lucide-react';
import { DEVICE_STATUS, SENSOR_HEALTH, STAGE_A_SIMULATION_TAG } from '../contracts/afesContracts';
import EmptyState from './EmptyState';

export const DeviceList = ({ devices = [] }) => {
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDevices = useMemo(() => {
    return devices.filter((d) => {
      const matchesStatus = filterStatus === 'ALL' || d.status === filterStatus;
      const matchesSearch =
        searchQuery === '' ||
        d.device_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.zone_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.room_code?.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesStatus && matchesSearch;
    });
  }, [devices, filterStatus, searchQuery]);

  const formatUptime = (seconds) => {
    if (!seconds) return '0m';
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    return hrs > 0 ? `${hrs}h ${mins}m` : `${mins}m`;
  };

  return (
    <div className="devices-container" data-testid="devices-container">
      <div className="devices-toolbar">
        <div className="search-box">
          <Search size={16} className="search-icon" />
          <input
            type="text"
            className="search-input"
            placeholder="Search device ID or zone..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filter-buttons">
          {['ALL', DEVICE_STATUS.ONLINE, DEVICE_STATUS.OFFLINE, DEVICE_STATUS.FAULT].map(
            (status) => (
              <button
                key={status}
                type="button"
                className={`filter-btn ${filterStatus === status ? 'is-active' : ''}`}
                onClick={() => setFilterStatus(status)}
              >
                {status}
              </button>
            )
          )}
        </div>
      </div>

      {filteredDevices.length === 0 ? (
        <EmptyState
          title="No Devices Found"
          description={`No devices match status filter '${filterStatus}' and search query.`}
          icon={Cpu}
        />
      ) : (
        <div className="devices-grid">
          {filteredDevices.map((device) => {
            const isOnline = device.status === DEVICE_STATUS.ONLINE;
            return (
              <article
                key={device.device_id}
                className="device-card glass-panel"
                data-testid={`device-card-${device.device_id}`}
              >
                <div className="device-card__head">
                  <div className="device-title-wrap">
                    <div className="device-avatar">
                      <Cpu size={18} />
                    </div>
                    <div>
                      <h4 className="device-id">{device.device_id}</h4>
                      <div className="device-zone-ref">
                        {device.zone_id} ({device.room_code})
                      </div>
                    </div>
                  </div>

                  <div className="device-status-badge">
                    {device.status === DEVICE_STATUS.ONLINE ? (
                      <span className="badge badge--online">
                        <CheckCircle2 size={12} />
                        <span>ONLINE</span>
                      </span>
                    ) : device.status === DEVICE_STATUS.OFFLINE ? (
                      <span className="badge badge--offline">
                        <WifiOff size={12} />
                        <span>OFFLINE</span>
                      </span>
                    ) : (
                      <span className="badge badge--fault">
                        <XCircle size={12} />
                        <span>FAULT</span>
                      </span>
                    )}
                  </div>
                </div>

                <div className="device-card__meta">
                  <span className="tag-chip">{device.device_type}</span>
                  <span className="tag-chip">FW: {device.firmware_version}</span>
                  {device.is_simulated && (
                    <span className="tag-chip tag-chip--sim" title="Stage A simulation marker">
                      {STAGE_A_SIMULATION_TAG}
                    </span>
                  )}
                </div>

                <div className="device-metrics-grid">
                  <div className="device-metric">
                    <div className="device-metric__label">
                      <Wifi size={12} />
                      <span>RSSI</span>
                    </div>
                    <div className="device-metric__val">
                      {isOnline ? `${device.rssi_dbm} dBm` : '—'}
                    </div>
                  </div>

                  <div className="device-metric">
                    <div className="device-metric__label">
                      <Activity size={12} />
                      <span>Sensor Health</span>
                    </div>
                    <div className="device-metric__val">
                      <span
                        className={`health-dot ${
                          device.sensor_health === SENSOR_HEALTH.HEALTHY
                            ? 'health-dot--good'
                            : 'health-dot--bad'
                        }`}
                      />
                      <span>{device.sensor_health}</span>
                    </div>
                  </div>

                  <div className="device-metric">
                    <div className="device-metric__label">
                      <Clock size={12} />
                      <span>Uptime</span>
                    </div>
                    <div className="device-metric__val">
                      {formatUptime(device.uptime_seconds)}
                    </div>
                  </div>

                  <div className="device-metric">
                    <div className="device-metric__label">
                      <Zap size={12} />
                      <span>TinyML Latency</span>
                    </div>
                    <div className="device-metric__val">
                      {isOnline ? `${device.tinyml_inference_latency_ms} ms` : '—'}
                    </div>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default DeviceList;
