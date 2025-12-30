import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      const storedTokens = localStorage.getItem('tokens');
      const storedUser = localStorage.getItem('user');

      if (storedTokens && storedUser) {
        try {
          setTokens(JSON.parse(storedTokens));
          setUser(JSON.parse(storedUser));

          // Verify token is still valid
          const response = await authAPI.getCurrentUser();
          if (response.data.success) {
            setUser(response.data.data.user);
            localStorage.setItem('user', JSON.stringify(response.data.data.user));
          }
        } catch (error) {
          // Token is invalid, clear storage
          localStorage.removeItem('tokens');
          localStorage.removeItem('user');
          setUser(null);
          setTokens(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const signup = async (formData) => {
    try {
      const response = await authAPI.signup(formData);
      
      if (response.data.success) {
        const { user: userData, tokens: tokenData } = response.data.data;
        
        setUser(userData);
        setTokens(tokenData);
        localStorage.setItem('tokens', JSON.stringify(tokenData));
        localStorage.setItem('user', JSON.stringify(userData));
        
        toast.success('Account created successfully!');
        navigate('/dashboard');
        return { success: true };
      }
    } catch (error) {
      console.error('Signup error:', error);
      const errorData = error.response?.data;
      let errorMessage = 'Signup failed';
      
      if (error.message === 'Network Error') {
        errorMessage = 'Cannot connect to server. Please try again.';
      } else if (errorData?.message) {
        errorMessage = errorData.message;
      } else if (errorData?.detail) {
        errorMessage = errorData.detail;
      }
      
      toast.error(errorMessage);
      return { 
        success: false, 
        errors: errorData?.errors || { detail: errorMessage }
      };
    }
  };

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      
      if (response.data.success) {
        const { user: userData, tokens: tokenData } = response.data.data;
        
        setUser(userData);
        setTokens(tokenData);
        localStorage.setItem('tokens', JSON.stringify(tokenData));
        localStorage.setItem('user', JSON.stringify(userData));
        
        toast.success('Login successful!');
        
        // Redirect based on role
        if (userData.role === 'admin') {
          navigate('/admin');
        } else {
          navigate('/dashboard');
        }
        
        return { success: true };
      }
    } catch (error) {
      const errorData = error.response?.data;
      const errorMessage = errorData?.errors?.detail || errorData?.message || 'Login failed';
      toast.error(errorMessage);
      return { 
        success: false, 
        errors: errorData?.errors || { detail: errorMessage }
      };
    }
  };

  const logout = useCallback(async () => {
    try {
      if (tokens?.refresh) {
        await authAPI.logout(tokens.refresh);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setTokens(null);
      localStorage.removeItem('tokens');
      localStorage.removeItem('user');
      toast.success('Logged out successfully');
      navigate('/login');
    }
  }, [tokens, navigate]);

  const updateUser = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const isAuthenticated = !!user && !!tokens;
  const isAdmin = user?.role === 'admin';

  const value = {
    user,
    tokens,
    loading,
    isAuthenticated,
    isAdmin,
    signup,
    login,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
