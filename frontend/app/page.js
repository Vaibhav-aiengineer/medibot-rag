'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

const DEMO_ACCOUNTS = [
  { username: 'dr.mehta',      password: 'doctor',     role: 'doctor',             label: 'Dr. Mehta',     color: 'var(--role-doctor)' },
  { username: 'nurse.priya',   password: 'nurse',      role: 'nurse',              label: 'Nurse Priya',   color: 'var(--role-nurse)' },
  { username: 'billing.ravi',  password: 'billing',    role: 'billing_executive',  label: 'Billing Ravi',  color: 'var(--role-billing)' },
  { username: 'tech.anand',    password: 'technician', role: 'technician',         label: 'Tech Anand',    color: 'var(--role-technician)' },
  { username: 'admin.sys',     password: 'admin',      role: 'admin',              label: 'Admin',         color: 'var(--role-admin)' },
];

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (user, pass) => {
    setError('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass }),
      });

      const data = await res.json();

      if (!data.success) {
        setError(data.message || 'Login failed');
        setLoading(false);
        return;
      }

      // Fetch collections for this role
      const colRes = await fetch(`${API_URL}/collections/${data.role}`);
      const colData = await colRes.json();

      // Store session
      const session = {
        username: user,
        role: data.role,
        token: data.token,
        collections: colData.collections || [],
      };
      sessionStorage.setItem('medibot_session', JSON.stringify(session));

      router.push('/chat');
    } catch (err) {
      setError('Cannot connect to server. Is the backend running?');
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError('Please enter username and password');
      return;
    }
    handleLogin(username.trim(), password.trim());
  };

  const handleDemoLogin = (account) => {
    setUsername(account.username);
    setPassword(account.password);
    handleLogin(account.username, account.password);
  };

  return (
    <div className="login-page">
      <div className="login-card">
        {/* Logo */}
        <div className="login-logo">
          <div className="login-logo-icon">🏥</div>
          <h1>MediBot</h1>
        </div>
        <p className="login-subtitle">
          Hospital Knowledge Assistant — Powered by Hybrid RAG
        </p>

        {/* Login Form */}
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              className="form-input"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              className="form-input"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          {error && <div className="login-error">{error}</div>}

          <button
            id="login-submit"
            className="login-btn"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* Demo Accounts */}
        <div className="login-divider">
          <span>Quick Demo Login</span>
        </div>

        <div className="demo-accounts">
          {DEMO_ACCOUNTS.map((account) => (
            <button
              key={account.username}
              id={`demo-${account.role}`}
              className="demo-btn"
              onClick={() => handleDemoLogin(account)}
              disabled={loading}
            >
              <span className="demo-dot" style={{ background: account.color }} />
              <span className="demo-name">{account.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
