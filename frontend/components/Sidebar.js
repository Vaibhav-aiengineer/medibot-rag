'use client';

const ROLE_LABELS = {
  doctor: 'Doctor',
  nurse: 'Nurse',
  billing_executive: 'Billing Executive',
  technician: 'Technician',
  admin: 'Administrator',
};

const ROLE_ICONS = {
  doctor: '🩺',
  nurse: '💉',
  billing_executive: '💰',
  technician: '🔧',
  admin: '🛡️',
};

export default function Sidebar({ session, onLogout }) {
  if (!session) return null;

  const initial = session.username.charAt(0).toUpperCase();
  const roleLabel = ROLE_LABELS[session.role] || session.role;
  const roleIcon = ROLE_ICONS[session.role] || '👤';

  // Pick the role color variable name for avatar
  const roleColorMap = {
    doctor: 'var(--role-doctor)',
    nurse: 'var(--role-nurse)',
    billing_executive: 'var(--role-billing)',
    technician: 'var(--role-technician)',
    admin: 'var(--role-admin)',
  };
  const avatarBg = roleColorMap[session.role] || 'var(--accent-start)';

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">🏥</div>
        <h2>MediBot</h2>
      </div>

      {/* User Info */}
      <div className="sidebar-section">
        <div className="sidebar-section-title">Logged in as</div>
        <div className="sidebar-user">
          <div className="sidebar-avatar" style={{ background: avatarBg }}>
            {initial}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{session.username}</div>
            <span className={`role-badge ${session.role}`}>
              {roleIcon} {roleLabel}
            </span>
          </div>
        </div>
      </div>

      {/* Collections */}
      <div className="sidebar-section">
        <div className="sidebar-section-title">Accessible Collections</div>
        <div className="collection-tags">
          {session.collections.map((col) => (
            <span key={col} className="collection-tag">
              {col}
            </span>
          ))}
        </div>
      </div>

      <div className="sidebar-spacer" />

      {/* Logout */}
      <button id="logout-btn" className="logout-btn" onClick={onLogout}>
        ← Sign Out
      </button>
    </aside>
  );
}
