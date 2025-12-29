import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user, isAdmin } = useAuth();

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1 className="page-title">Welcome, {user?.full_name}! 👋</h1>
        <p className="page-subtitle">
          Here's your account overview
        </p>
      </div>

      <div className="dashboard-grid">
        {/* User Info Card */}
        <div className="card dashboard-card">
          <div className="card-header">
            <h2 className="card-title">Account Information</h2>
            <Link to="/profile" className="btn btn-sm btn-outline">
              Edit Profile
            </Link>
          </div>
          <div className="info-list">
            <div className="info-item">
              <span className="info-label">Full Name</span>
              <span className="info-value">{user?.full_name}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Email</span>
              <span className="info-value">{user?.email}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Role</span>
              <span className={`badge ${isAdmin ? 'badge-primary' : 'badge-secondary'}`}>
                {user?.role}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Status</span>
              <span className={`badge ${user?.status === 'active' ? 'badge-success' : 'badge-danger'}`}>
                {user?.status}
              </span>
            </div>
          </div>
        </div>

        {/* Activity Card */}
        <div className="card dashboard-card">
          <div className="card-header">
            <h2 className="card-title">Activity</h2>
          </div>
          <div className="info-list">
            <div className="info-item">
              <span className="info-label">Last Login</span>
              <span className="info-value">{formatDate(user?.last_login)}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Account Created</span>
              <span className="info-value">{formatDate(user?.created_at)}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Last Updated</span>
              <span className="info-value">{formatDate(user?.updated_at)}</span>
            </div>
          </div>
        </div>

        {/* Quick Actions Card */}
        <div className="card dashboard-card">
          <div className="card-header">
            <h2 className="card-title">Quick Actions</h2>
          </div>
          <div className="quick-actions">
            <Link to="/profile" className="action-btn">
              <span className="action-icon">👤</span>
              <span className="action-label">View Profile</span>
            </Link>
            <Link to="/profile#password" className="action-btn">
              <span className="action-icon">🔒</span>
              <span className="action-label">Change Password</span>
            </Link>
            {isAdmin && (
              <Link to="/admin" className="action-btn">
                <span className="action-icon">⚙️</span>
                <span className="action-label">Admin Panel</span>
              </Link>
            )}
          </div>
        </div>

        {/* Stats Card (for admins) */}
        {isAdmin && (
          <div className="card dashboard-card admin-card">
            <div className="card-header">
              <h2 className="card-title">Admin Access</h2>
            </div>
            <div className="admin-info">
              <p>
                As an administrator, you have access to the Admin Panel where you can:
              </p>
              <ul>
                <li>View all registered users</li>
                <li>Activate or deactivate user accounts</li>
                <li>Manage user roles</li>
              </ul>
              <Link to="/admin" className="btn btn-primary mt-3">
                Go to Admin Panel
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
