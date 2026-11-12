import React from 'react';
import { AlertOctagon, RotateCw } from 'lucide-react';

export const ErrorBanner = ({ message, code, onRetry }) => {
  if (!message) return null;

  return (
    <aside className="error-banner glass-panel" role="alert" data-testid="error-banner">
      <div className="error-banner-content">
        <div className="error-banner-icon">
          <AlertOctagon size={20} />
        </div>
        <div className="error-banner-text">
          <div className="error-banner-title">
            <strong>System Communication Notice</strong>
            {code && <span className="error-badge">{code}</span>}
          </div>
          <p className="error-banner-message">{message}</p>
        </div>
      </div>
      {onRetry && (
        <button
          type="button"
          className="btn-retry"
          onClick={onRetry}
          title="Retry connection"
        >
          <RotateCw size={14} />
          <span>Retry</span>
        </button>
      )}
    </aside>
  );
};

export default ErrorBanner;
