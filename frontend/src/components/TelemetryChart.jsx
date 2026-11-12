import React, { useMemo } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
} from 'recharts';
import { Activity, Thermometer, CloudFog } from 'lucide-react';
import { THRESHOLDS } from '../contracts/afesContracts';
import EmptyState from './EmptyState';

export const TelemetryChart = ({ telemetry = [], title = 'Environmental Telemetry Stream' }) => {
  const chartData = useMemo(() => {
    if (!Array.isArray(telemetry) || telemetry.length === 0) return [];
    return telemetry.map((pt) => ({
      time: new Date(pt.timestamp_epoch_ms || Date.now()).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      }),
      temperature: Number(pt.temperature || 0),
      smoke_ppm: Number(pt.smoke_ppm || 0),
      humidity: Number(pt.humidity || 0),
      fullTimestamp: pt.timestamp_iso || new Date(pt.timestamp_epoch_ms).toISOString(),
    }));
  }, [telemetry]);

  const stats = useMemo(() => {
    if (chartData.length === 0) return null;
    const temps = chartData.map((d) => d.temperature);
    const smokes = chartData.map((d) => d.smoke_ppm);
    return {
      avgTemp: (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1),
      maxTemp: Math.max(...temps).toFixed(1),
      avgSmoke: (smokes.reduce((a, b) => a + b, 0) / smokes.length).toFixed(0),
      maxSmoke: Math.max(...smokes).toFixed(0),
    };
  }, [chartData]);

  return (
    <section className="telemetry-chart-panel glass-panel" data-testid="telemetry-chart">
      <div className="chart-header">
        <div className="chart-title-wrap">
          <Activity size={18} className="text-blue" />
          <h3 className="section-title">{title}</h3>
        </div>
        <div className="chart-indicators">
          <span className="legend-indicator">
            <span className="dot dot--temp" />
            <span>Temperature (&deg;C)</span>
          </span>
          <span className="legend-indicator">
            <span className="dot dot--smoke" />
            <span>Smoke (PPM)</span>
          </span>
        </div>
      </div>

      <div className="chart-wrapper">
        {chartData.length === 0 ? (
          <EmptyState
            title="Waiting for Telemetry Feed"
            description="No telemetry time-series records have been received yet."
            icon={Activity}
          />
        ) : (
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={chartData} margin={{ top: 10, right: 24, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.08)" />
              <XAxis
                dataKey="time"
                stroke="#64748b"
                tick={{ fontSize: 11, fill: '#94a3b8' }}
                tickLine={false}
              />
              <YAxis
                yAxisId="temp"
                orientation="left"
                stroke="#f97316"
                tick={{ fontSize: 11, fill: '#fdba74' }}
                tickLine={false}
                axisLine={false}
                domain={[0, 'auto']}
                unit="°C"
              />
              <YAxis
                yAxisId="smoke"
                orientation="right"
                stroke="#38bdf8"
                tick={{ fontSize: 11, fill: '#7dd3fc' }}
                tickLine={false}
                axisLine={false}
                domain={[0, 'auto']}
                unit=" ppm"
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(15, 23, 42, 0.95)',
                  borderColor: 'rgba(255, 255, 255, 0.15)',
                  borderRadius: '8px',
                  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
                  fontSize: '12px',
                  color: '#f8fafc',
                }}
              />
              <Legend verticalAlign="top" height={36} />
              <ReferenceLine
                yAxisId="temp"
                y={THRESHOLDS.TEMP_WARNING_C}
                label={{ value: 'Temp Warning (50°C)', fill: '#ef4444', fontSize: 10 }}
                stroke="#ef4444"
                strokeDasharray="4 4"
              />
              <ReferenceLine
                yAxisId="smoke"
                y={THRESHOLDS.SMOKE_WARNING_PPM}
                label={{ value: 'Smoke Warning (500 PPM)', fill: '#f59e0b', fontSize: 10 }}
                stroke="#f59e0b"
                strokeDasharray="4 4"
              />
              <Line
                yAxisId="temp"
                type="monotone"
                dataKey="temperature"
                name="Temperature"
                stroke="#f97316"
                strokeWidth={2}
                dot={{ r: 2 }}
                activeDot={{ r: 5 }}
              />
              <Line
                yAxisId="smoke"
                type="monotone"
                dataKey="smoke_ppm"
                name="Smoke PPM"
                stroke="#38bdf8"
                strokeWidth={2}
                dot={{ r: 2 }}
                activeDot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {stats && (
        <div className="chart-stats-bar">
          <div className="chart-stat-item">
            <Thermometer size={14} className="text-orange" />
            <span className="stat-label">Avg / Peak Temp:</span>
            <strong>{stats.avgTemp}&deg;C / {stats.maxTemp}&deg;C</strong>
          </div>
          <div className="chart-stat-item">
            <CloudFog size={14} className="text-blue" />
            <span className="stat-label">Avg / Peak Smoke:</span>
            <strong>{stats.avgSmoke} PPM / {stats.maxSmoke} PPM</strong>
          </div>
        </div>
      )}
    </section>
  );
};

export default TelemetryChart;
