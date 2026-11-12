import React from 'react';
import { Flame, RefreshCw, Database, Server, Shield } from 'lucide-react';
import { STAGE_A_SIMULATION_TAG } from '../contracts/afesContracts';

export const Header = ({
  isMockMode,
  onToggleMockMode,
  onRefresh,
  isRefreshing,
  lastUpdated,
}) => {
  return (
    <header className="app-header glass-panel" data-testid="app-header">
      <div className="app-header__left">
        <div className="brand-badge">
          <div className="brand-logo-glow">
            <Flame size={24} className="brand-icon" />
          </div>
          <div>
            <div className="brand-title">
              <span className="brand-name">AFES</span>
              <span className="brand-version">2.0</span>
            </div>
            <div className="brand-subtitle">
              Advanced Fire Emergency System &bull; NOC Dashboard
            </div>
          </div>
        </div>

        <div className="simulation-tag-pill" title="Stage A virtual simulation contract marker">
          <span className="status-dot status-dot--amber" />
          <span>{STAGE_A_SIMULATION_TAG}</span>
        </div>
      </div>

      <div className="app-header__right">
        <div className="data-mode-badge" title="Telemetry data source">
          {isMockMode ? (
            <span className="badge badge--mock">
              <Database size={13} />
              <span>Mock / Simulated Stream</span>
            </span>
          ) : (
            <span className="badge badge--live">
              <Server size={13} />
              <span>Spring Boot REST /api/v2</span>
            </span>
          )}
        </div>

        <button
          type="button"
          className="btn-mode-toggle"
          onClick={onToggleMockMode}
          title="Toggle between Live API and local Mock Simulator"
        >
          {isMockMode ? 'Switch to Live API' : 'Switch to Mock Simulator'}
        </button>

        <div className="header-divider" />

        <div className="refresh-status">
          {lastUpdated && (
            <span className="last-sync-time">
              Synced {new Date(lastUpdated).toLocaleTimeString()}
            </span>
          )}
          <button
            type="button"
            className={`btn-refresh ${isRefreshing ? 'is-spinning' : ''}`}
            onClick={onRefresh}
            disabled={isRefreshing}
            title="Refresh telemetry"
          >
            <RefreshCw size={15} />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
