import React, { useState, useEffect, useCallback } from 'react';
import {
  LayoutDashboard,
  Cpu,
  Activity,
  ShieldAlert,
  Sliders,
  AlertTriangle,
} from 'lucide-react';
import apiService from '../api/sensorApi';
import Header from '../components/Header';
import StatsSummary from '../components/StatsSummary';
import ZoneCard from '../components/ZoneCard';
import DeviceList from '../components/DeviceList';
import AlarmTriage from '../components/AlarmTriage';
import TelemetryChart from '../components/TelemetryChart';
import ControlConsole from '../components/ControlConsole';
import LoadingSkeleton from '../components/LoadingSkeleton';
import ErrorBanner from '../components/ErrorBanner';

export const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [zones, setZones] = useState([]);
  const [devices, setDevices] = useState([]);
  const [alarms, setAlarms] = useState([]);
  const [telemetry, setTelemetry] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isActing, setIsActing] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isMockMode, setIsMockMode] = useState(apiService.isUsingMock());
  const [activeScenario, setActiveScenario] = useState(null);

  const fetchDashboardData = useCallback(async (showRefreshIndicator = false) => {
    if (showRefreshIndicator) {
      setIsRefreshing(true);
    }
    setError(null);

    try {
      const [zonesData, devicesData, alarmsData, telemetryData] = await Promise.all([
        apiService.getZonesSummary(),
        apiService.getDevices(),
        apiService.getActiveAlarms(),
        apiService.getTelemetryHistory(),
      ]);

      setZones(zonesData || []);
      setDevices(devicesData || []);
      setAlarms(alarmsData || []);
      setTelemetry(telemetryData || []);
      setLastUpdated(Date.now());
      setActiveScenario(apiService.getSimulationScenario());
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError({
        message: err.message || 'Unable to connect to AFES backend API.',
        code: err.code || 'ERR_CONNECTION',
      });
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(() => {
      fetchDashboardData();
    }, 4000);
    return () => clearInterval(interval);
  }, [fetchDashboardData]);

  const handleToggleMockMode = () => {
    const nextMode = !isMockMode;
    setIsMockMode(nextMode);
    apiService.setMockMode(nextMode);
    fetchDashboardData(true);
  };

  const handleAcknowledgeAlarm = async (alarmId) => {
    setIsActing(true);
    try {
      await apiService.acknowledgeAlarm(alarmId, 'Acknowledged via NOC Dashboard');
      await fetchDashboardData();
    } catch (err) {
      setError({
        message: `Alarm acknowledgment failed: ${err.message}`,
        code: err.code || 'ERR_MUTATION_FAILED',
      });
    } finally {
      setIsActing(false);
    }
  };

  const handleResolveAlarm = async (alarmId) => {
    setIsActing(true);
    try {
      await apiService.resolveAlarm(alarmId);
      await fetchDashboardData();
    } catch (err) {
      setError({
        message: `Alarm resolution failed: ${err.message}`,
        code: err.code || 'ERR_MUTATION_FAILED',
      });
    } finally {
      setIsActing(false);
    }
  };

  const handleDispatchCommand = async (payload) => {
    setIsActing(true);
    try {
      const result = await apiService.dispatchControlCommand(payload);
      await fetchDashboardData();
      return result;
    } catch (err) {
      setError({
        message: `Actuator command dispatch failed: ${err.message}`,
        code: err.code || 'ERR_MUTATION_FAILED',
      });
      throw err;
    } finally {
      setIsActing(false);
    }
  };

  const handleStartScenario = (scenarioId) => {
    apiService.startSimulationScenario(scenarioId);
    setActiveScenario(scenarioId);
    fetchDashboardData();
  };

  const handleStopScenario = () => {
    apiService.stopSimulationScenario();
    setActiveScenario(null);
    fetchDashboardData();
  };

  const activeAlarmCount = alarms.length;

  return (
    <div className="app-shell" data-testid="app-shell">
      <Header
        isMockMode={isMockMode}
        onToggleMockMode={handleToggleMockMode}
        onRefresh={() => fetchDashboardData(true)}
        isRefreshing={isRefreshing}
        lastUpdated={lastUpdated}
      />

      <main className="app-main">
        {error && (
          <ErrorBanner
            message={error.message}
            code={error.code}
            onRetry={() => fetchDashboardData(true)}
          />
        )}

        {/* Global Stats Bar */}
        <StatsSummary zones={zones} devices={devices} alarms={alarms} />

        {/* Navigation Tabs */}
        <nav className="dashboard-nav glass-panel" aria-label="Dashboard views">
          <button
            type="button"
            className={`nav-tab ${activeTab === 'overview' ? 'is-active' : ''}`}
            onClick={() => setActiveTab('overview')}
            data-testid="tab-overview"
          >
            <LayoutDashboard size={16} />
            <span>Facility Overview</span>
          </button>

          <button
            type="button"
            className={`nav-tab ${activeTab === 'devices' ? 'is-active' : ''}`}
            onClick={() => setActiveTab('devices')}
            data-testid="tab-devices"
          >
            <Cpu size={16} />
            <span>Sensing Fleet ({devices.length})</span>
          </button>

          <button
            type="button"
            className={`nav-tab ${activeTab === 'telemetry' ? 'is-active' : ''}`}
            onClick={() => setActiveTab('telemetry')}
            data-testid="tab-telemetry"
          >
            <Activity size={16} />
            <span>Telemetry Trends</span>
          </button>

          <button
            type="button"
            className={`nav-tab ${activeTab === 'alarms' ? 'is-active' : ''}`}
            onClick={() => setActiveTab('alarms')}
            data-testid="tab-alarms"
          >
            <ShieldAlert size={16} />
            <span>Alarm Triage</span>
            {activeAlarmCount > 0 && (
              <span className="tab-badge-count">{activeAlarmCount}</span>
            )}
          </button>

          <button
            type="button"
            className={`nav-tab ${activeTab === 'controls' ? 'is-active' : ''}`}
            onClick={() => setActiveTab('controls')}
            data-testid="tab-controls"
          >
            <Sliders size={16} />
            <span>Actuator Controls</span>
          </button>
        </nav>

        {/* Tab View Contents */}
        <div className="tab-content-area">
          {isLoading ? (
            <LoadingSkeleton count={4} height="160px" />
          ) : (
            <>
              {/* Tab 1: Facility Overview */}
              {activeTab === 'overview' && (
                <section className="overview-tab-view" data-testid="view-overview">
                  <div className="section-head">
                    <div>
                      <h2 className="section-title">Monitored Zones & Safety Shell</h2>
                      <p className="section-subtitle">
                        Real-time environmental sensing status across mapped facility floors.
                      </p>
                    </div>
                  </div>

                  <div className="zones-grid">
                    {zones.map((zone) => (
                      <ZoneCard key={zone.zone_id} zone={zone} />
                    ))}
                  </div>
                </section>
              )}

              {/* Tab 2: Sensing Fleet */}
              {activeTab === 'devices' && (
                <section className="devices-tab-view" data-testid="view-devices">
                  <div className="section-head">
                    <div>
                      <h2 className="section-title">Hardware Sensing Fleet & Edge Nodes</h2>
                      <p className="section-subtitle">
                        Operational diagnostics, TinyML latency metrics, and connection states.
                      </p>
                    </div>
                  </div>
                  <DeviceList devices={devices} />
                </section>
              )}

              {/* Tab 3: Telemetry Trends */}
              {activeTab === 'telemetry' && (
                <section className="telemetry-tab-view" data-testid="view-telemetry">
                  <div className="section-head">
                    <div>
                      <h2 className="section-title">Historical Telemetry Stream</h2>
                      <p className="section-subtitle">
                        High-frequency temperature and smoke PPM time-series analytics.
                      </p>
                    </div>
                  </div>
                  <TelemetryChart telemetry={telemetry} />
                </section>
              )}

              {/* Tab 4: Alarm Triage */}
              {activeTab === 'alarms' && (
                <section className="alarms-tab-view" data-testid="view-alarms">
                  <AlarmTriage
                    alarms={alarms}
                    onAcknowledgeAlarm={handleAcknowledgeAlarm}
                    onResolveAlarm={handleResolveAlarm}
                    isActing={isActing}
                  />
                </section>
              )}

              {/* Tab 5: Actuator Controls & Simulation */}
              {activeTab === 'controls' && (
                <section className="controls-tab-view" data-testid="view-controls">
                  <div className="section-head">
                    <div>
                      <h2 className="section-title">Emergency Actuator & Override Console</h2>
                      <p className="section-subtitle">
                        Direct suppression pump, siren modulation, and Stage A simulation tools.
                      </p>
                    </div>
                  </div>
                  <ControlConsole
                    onDispatchCommand={handleDispatchCommand}
                    onStartScenario={handleStartScenario}
                    onStopScenario={handleStopScenario}
                    activeScenario={activeScenario}
                    isActing={isActing}
                    zones={zones}
                  />
                </section>
              )}
            </>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="footer-content">
          <span>AFES 2.0 &bull; HCMUT IoT Course Project (Semester 261)</span>
          <span className="footer-divider">&bull;</span>
          <span>Tier 5 User Presentation Baseline (N06 Custom Dashboard)</span>
          <span className="footer-divider">&bull;</span>
          <span>Lead: Ý (@gutjmosnin)</span>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
