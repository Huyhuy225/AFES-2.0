import React from 'react';

export const LoadingSkeleton = ({ count = 3, height = '120px' }) => {
  return (
    <div className="skeleton-grid" data-testid="loading-skeleton">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="skeleton-card glass-panel"
          style={{ minHeight: height }}
        >
          <div className="skeleton-line skeleton-title" />
          <div className="skeleton-line skeleton-value" />
          <div className="skeleton-line skeleton-sub" />
        </div>
      ))}
    </div>
  );
};

export default LoadingSkeleton;
