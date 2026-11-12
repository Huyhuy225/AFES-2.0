import React from 'react';
import { Inbox } from 'lucide-react';

export const EmptyState = ({
  title = 'No Data Available',
  description = 'There are no active records matching the current filter.',
  icon = Inbox,
  actionButton = null,
}) => {
  return (
    <div className="empty-state-panel glass-panel" data-testid="empty-state">
      <div className="empty-state-icon">
        {React.createElement(icon, { size: 32 })}
      </div>
      <h3 className="empty-state-title">{title}</h3>
      <p className="empty-state-desc">{description}</p>
      {actionButton && <div className="empty-state-action">{actionButton}</div>}
    </div>
  );
};

export default EmptyState;
