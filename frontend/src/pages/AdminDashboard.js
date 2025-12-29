import React, { useState, useEffect, useCallback } from 'react';
import { adminAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/LoadingSpinner';
import Modal from '../components/Modal';
import Pagination from '../components/Pagination';
import toast from 'react-hot-toast';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  
  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [modalAction, setModalAction] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);

  // Filters
  const [filters, setFilters] = useState({
    status: '',
    role: '',
    search: '',
  });

  // Fetch users
  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page: currentPage,
        ...filters,
      };
      
      // Remove empty filters
      Object.keys(params).forEach((key) => {
        if (!params[key]) delete params[key];
      });

      const response = await adminAPI.getUsers(params);
      
      if (response.data.success) {
        setUsers(response.data.data.users);
        setTotalUsers(response.data.data.count);
        setTotalPages(Math.ceil(response.data.data.count / 10));
      }
    } catch (error) {
      toast.error('Failed to fetch users');
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, filters]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  // Handle filter change
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
    setCurrentPage(1);
  };

  // Handle action click
  const handleActionClick = (action, userItem) => {
    setSelectedUser(userItem);
    setModalAction(action);
    setModalOpen(true);
  };

  // Confirm action
  const handleConfirmAction = async () => {
    if (!selectedUser || !modalAction) return;

    setActionLoading(true);
    try {
      let response;
      if (modalAction === 'activate') {
        response = await adminAPI.activateUser(selectedUser.id);
      } else {
        response = await adminAPI.deactivateUser(selectedUser.id);
      }

      if (response.data.success) {
        toast.success(response.data.message);
        fetchUsers();
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || `Failed to ${modalAction} user`;
      toast.error(errorMessage);
    } finally {
      setActionLoading(false);
      setModalOpen(false);
      setSelectedUser(null);
      setModalAction(null);
    }
  };

  // Close modal
  const handleCloseModal = () => {
    if (!actionLoading) {
      setModalOpen(false);
      setSelectedUser(null);
      setModalAction(null);
    }
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="admin-dashboard">
      <div className="page-header">
        <h1 className="page-title">Admin Panel</h1>
        <p className="page-subtitle">Manage all users in the system</p>
      </div>

      {/* Filters */}
      <div className="card filters-card">
        <div className="filters-row">
          <div className="filter-group">
            <label htmlFor="status-filter" className="form-label">
              Status
            </label>
            <select
              id="status-filter"
              name="status"
              value={filters.status}
              onChange={handleFilterChange}
              className="form-input"
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="role-filter" className="form-label">
              Role
            </label>
            <select
              id="role-filter"
              name="role"
              value={filters.role}
              onChange={handleFilterChange}
              className="form-input"
            >
              <option value="">All Roles</option>
              <option value="admin">Admin</option>
              <option value="user">User</option>
            </select>
          </div>

          <div className="filter-group search-group">
            <label htmlFor="search-filter" className="form-label">
              Search
            </label>
            <input
              type="text"
              id="search-filter"
              name="search"
              value={filters.search}
              onChange={handleFilterChange}
              className="form-input"
              placeholder="Search by name or email..."
            />
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-row">
        <div className="stat-card">
          <span className="stat-number">{totalUsers}</span>
          <span className="stat-label">Total Users</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{users.filter(u => u.status === 'active').length}</span>
          <span className="stat-label">Active (this page)</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{users.filter(u => u.role === 'admin').length}</span>
          <span className="stat-label">Admins (this page)</span>
        </div>
      </div>

      {/* Users Table */}
      <div className="card">
        {loading ? (
          <div className="loading-container">
            <LoadingSpinner size="large" />
          </div>
        ) : users.length === 0 ? (
          <div className="empty-state">
            <p>No users found</p>
          </div>
        ) : (
          <>
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Email</th>
                    <th>Full Name</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((userItem) => (
                    <tr key={userItem.id}>
                      <td>{userItem.email}</td>
                      <td>{userItem.full_name}</td>
                      <td>
                        <span className={`badge ${userItem.role === 'admin' ? 'badge-primary' : 'badge-secondary'}`}>
                          {userItem.role}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${userItem.status === 'active' ? 'badge-success' : 'badge-danger'}`}>
                          {userItem.status}
                        </span>
                      </td>
                      <td>{formatDate(userItem.created_at)}</td>
                      <td>
                        <div className="action-buttons">
                          {userItem.id !== user.id ? (
                            <>
                              {userItem.status === 'inactive' ? (
                                <button
                                  className="btn btn-sm btn-success"
                                  onClick={() => handleActionClick('activate', userItem)}
                                >
                                  Activate
                                </button>
                              ) : (
                                <button
                                  className="btn btn-sm btn-danger"
                                  onClick={() => handleActionClick('deactivate', userItem)}
                                >
                                  Deactivate
                                </button>
                              )}
                            </>
                          ) : (
                            <span className="text-muted text-xs">Current User</span>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}
      </div>

      {/* Confirmation Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={handleCloseModal}
        title={`${modalAction === 'activate' ? 'Activate' : 'Deactivate'} User`}
        actions={
          <>
            <button
              className="btn btn-secondary"
              onClick={handleCloseModal}
              disabled={actionLoading}
            >
              Cancel
            </button>
            <button
              className={`btn ${modalAction === 'activate' ? 'btn-success' : 'btn-danger'}`}
              onClick={handleConfirmAction}
              disabled={actionLoading}
            >
              {actionLoading ? (
                <LoadingSpinner />
              ) : (
                `${modalAction === 'activate' ? 'Activate' : 'Deactivate'}`
              )}
            </button>
          </>
        }
      >
        <p>
          Are you sure you want to {modalAction} the user{' '}
          <strong>{selectedUser?.email}</strong>?
        </p>
        {modalAction === 'deactivate' && (
          <p className="mt-2 text-sm text-muted">
            This user will not be able to log in until their account is activated again.
          </p>
        )}
      </Modal>
    </div>
  );
};

export default AdminDashboard;
