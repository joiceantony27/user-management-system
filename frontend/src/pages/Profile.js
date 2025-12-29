import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { userAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import toast from 'react-hot-toast';
import './Profile.css';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  
  // Profile form state
  const [profileData, setProfileData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
  });
  const [profileErrors, setProfileErrors] = useState({});
  const [profileLoading, setProfileLoading] = useState(false);

  // Password form state
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_new_password: '',
  });
  const [passwordErrors, setPasswordErrors] = useState({});
  const [passwordLoading, setPasswordLoading] = useState(false);

  // Profile validation
  const validateProfile = () => {
    const errors = {};
    
    if (!profileData.full_name.trim()) {
      errors.full_name = 'Full name is required';
    } else if (profileData.full_name.trim().length < 2) {
      errors.full_name = 'Full name must be at least 2 characters';
    }

    if (!profileData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(profileData.email)) {
      errors.email = 'Please enter a valid email address';
    }

    setProfileErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Password validation
  const validatePassword = () => {
    const errors = {};

    if (!passwordData.current_password) {
      errors.current_password = 'Current password is required';
    }

    if (!passwordData.new_password) {
      errors.new_password = 'New password is required';
    } else {
      if (passwordData.new_password.length < 8) {
        errors.new_password = 'Password must be at least 8 characters';
      } else if (!/[A-Z]/.test(passwordData.new_password)) {
        errors.new_password = 'Password must contain at least one uppercase letter';
      } else if (!/[a-z]/.test(passwordData.new_password)) {
        errors.new_password = 'Password must contain at least one lowercase letter';
      } else if (!/\d/.test(passwordData.new_password)) {
        errors.new_password = 'Password must contain at least one digit';
      } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(passwordData.new_password)) {
        errors.new_password = 'Password must contain at least one special character';
      }
    }

    if (!passwordData.confirm_new_password) {
      errors.confirm_new_password = 'Please confirm your new password';
    } else if (passwordData.new_password !== passwordData.confirm_new_password) {
      errors.confirm_new_password = 'Passwords do not match';
    }

    setPasswordErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle profile input change
  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData((prev) => ({ ...prev, [name]: value }));
    if (profileErrors[name]) {
      setProfileErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  // Handle password input change
  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData((prev) => ({ ...prev, [name]: value }));
    if (passwordErrors[name]) {
      setPasswordErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  // Submit profile update
  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateProfile()) return;

    setProfileLoading(true);
    try {
      const response = await userAPI.updateProfile(profileData);
      
      if (response.data.success) {
        updateUser(response.data.data.user);
        toast.success('Profile updated successfully!');
      }
    } catch (error) {
      const errorData = error.response?.data;
      if (errorData?.errors) {
        const serverErrors = {};
        Object.keys(errorData.errors).forEach((key) => {
          serverErrors[key] = Array.isArray(errorData.errors[key])
            ? errorData.errors[key][0]
            : errorData.errors[key];
        });
        setProfileErrors(serverErrors);
      }
      toast.error(errorData?.message || 'Failed to update profile');
    } finally {
      setProfileLoading(false);
    }
  };

  // Submit password change
  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    
    if (!validatePassword()) return;

    setPasswordLoading(true);
    try {
      const response = await userAPI.changePassword(passwordData);
      
      if (response.data.success) {
        toast.success('Password changed successfully!');
        setPasswordData({
          current_password: '',
          new_password: '',
          confirm_new_password: '',
        });
      }
    } catch (error) {
      const errorData = error.response?.data;
      if (errorData?.errors) {
        const serverErrors = {};
        Object.keys(errorData.errors).forEach((key) => {
          serverErrors[key] = Array.isArray(errorData.errors[key])
            ? errorData.errors[key][0]
            : errorData.errors[key];
        });
        setPasswordErrors(serverErrors);
      }
      toast.error(errorData?.message || 'Failed to change password');
    } finally {
      setPasswordLoading(false);
    }
  };

  // Reset profile form
  const handleProfileReset = () => {
    setProfileData({
      full_name: user?.full_name || '',
      email: user?.email || '',
    });
    setProfileErrors({});
  };

  // Reset password form
  const handlePasswordReset = () => {
    setPasswordData({
      current_password: '',
      new_password: '',
      confirm_new_password: '',
    });
    setPasswordErrors({});
  };

  return (
    <div className="profile-page">
      <div className="page-header">
        <h1 className="page-title">My Profile</h1>
        <p className="page-subtitle">Manage your account settings</p>
      </div>

      <div className="profile-container">
        {/* Tabs */}
        <div className="profile-tabs">
          <button
            className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            Profile Information
          </button>
          <button
            className={`tab-btn ${activeTab === 'password' ? 'active' : ''}`}
            onClick={() => setActiveTab('password')}
          >
            Change Password
          </button>
        </div>

        {/* Profile Tab Content */}
        {activeTab === 'profile' && (
          <div className="card">
            <form onSubmit={handleProfileSubmit}>
              <div className="form-group">
                <label htmlFor="full_name" className="form-label">
                  Full Name
                </label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={profileData.full_name}
                  onChange={handleProfileChange}
                  className={`form-input ${profileErrors.full_name ? 'error' : ''}`}
                  disabled={profileLoading}
                />
                {profileErrors.full_name && (
                  <p className="form-error">{profileErrors.full_name}</p>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="email" className="form-label">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={profileData.email}
                  onChange={handleProfileChange}
                  className={`form-input ${profileErrors.email ? 'error' : ''}`}
                  disabled={profileLoading}
                />
                {profileErrors.email && (
                  <p className="form-error">{profileErrors.email}</p>
                )}
              </div>

              <div className="form-group">
                <label className="form-label">Role</label>
                <input
                  type="text"
                  value={user?.role}
                  className="form-input"
                  disabled
                />
                <p className="form-hint">Role cannot be changed</p>
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  onClick={handleProfileReset}
                  className="btn btn-secondary"
                  disabled={profileLoading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={profileLoading}
                >
                  {profileLoading ? <LoadingSpinner /> : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Password Tab Content */}
        {activeTab === 'password' && (
          <div className="card">
            <form onSubmit={handlePasswordSubmit}>
              <div className="form-group">
                <label htmlFor="current_password" className="form-label">
                  Current Password
                </label>
                <input
                  type="password"
                  id="current_password"
                  name="current_password"
                  value={passwordData.current_password}
                  onChange={handlePasswordChange}
                  className={`form-input ${passwordErrors.current_password ? 'error' : ''}`}
                  disabled={passwordLoading}
                  placeholder="Enter your current password"
                />
                {passwordErrors.current_password && (
                  <p className="form-error">{passwordErrors.current_password}</p>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="new_password" className="form-label">
                  New Password
                </label>
                <input
                  type="password"
                  id="new_password"
                  name="new_password"
                  value={passwordData.new_password}
                  onChange={handlePasswordChange}
                  className={`form-input ${passwordErrors.new_password ? 'error' : ''}`}
                  disabled={passwordLoading}
                  placeholder="Enter your new password"
                />
                {passwordErrors.new_password && (
                  <p className="form-error">{passwordErrors.new_password}</p>
                )}
                <p className="form-hint">
                  Must be at least 8 characters with uppercase, lowercase, number, and special character
                </p>
              </div>

              <div className="form-group">
                <label htmlFor="confirm_new_password" className="form-label">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  id="confirm_new_password"
                  name="confirm_new_password"
                  value={passwordData.confirm_new_password}
                  onChange={handlePasswordChange}
                  className={`form-input ${passwordErrors.confirm_new_password ? 'error' : ''}`}
                  disabled={passwordLoading}
                  placeholder="Confirm your new password"
                />
                {passwordErrors.confirm_new_password && (
                  <p className="form-error">{passwordErrors.confirm_new_password}</p>
                )}
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  onClick={handlePasswordReset}
                  className="btn btn-secondary"
                  disabled={passwordLoading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={passwordLoading}
                >
                  {passwordLoading ? <LoadingSpinner /> : 'Change Password'}
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
