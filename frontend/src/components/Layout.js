import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Layout.css';

const Layout = () => {
  const { user, isAdmin, logout } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { to: '/dashboard', label: 'Dashboard', icon: '🏠' },
    { to: '/profile', label: 'Profile', icon: '👤' },
  ];

  if (isAdmin) {
    navLinks.push({ to: '/admin', label: 'Admin Panel', icon: '⚙️' });
  }

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="layout">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-brand">
            <Link to="/dashboard" className="navbar-logo">
              <span className="logo-icon">👥</span>
              <span className="logo-text">UMS</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="navbar-links desktop-only">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`nav-link ${isActive(link.to) ? 'active' : ''}`}
              >
                <span className="nav-icon">{link.icon}</span>
                {link.label}
              </Link>
            ))}
          </div>

          <div className="navbar-right">
            {/* User Info */}
            <div className="user-info desktop-only">
              <span className="user-name">{user?.full_name}</span>
              <span className={`user-role badge ${isAdmin ? 'badge-primary' : 'badge-secondary'}`}>
                {user?.role}
              </span>
            </div>

            {/* Logout Button */}
            <button onClick={handleLogout} className="btn btn-outline btn-sm logout-btn">
              Logout
            </button>

            {/* Mobile Menu Toggle */}
            <button
              className="mobile-menu-toggle mobile-only"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? '✕' : '☰'}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="mobile-menu">
            <div className="mobile-user-info">
              <span className="user-name">{user?.full_name}</span>
              <span className={`user-role badge ${isAdmin ? 'badge-primary' : 'badge-secondary'}`}>
                {user?.role}
              </span>
            </div>
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`mobile-nav-link ${isActive(link.to) ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="nav-icon">{link.icon}</span>
                {link.label}
              </Link>
            ))}
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          <Outlet />
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} User Management System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
