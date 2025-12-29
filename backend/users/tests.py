"""
Unit tests for User Management System.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User


class UserModelTests(TestCase):
    """Tests for the User model."""
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            full_name='Test User'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.status, 'active')
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPass123!',
            full_name='Admin User'
        )
        
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertEqual(admin.role, 'admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_user_email_normalized(self):
        """Test that email is normalized for new users."""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='TestPass123!',
            full_name='Test User'
        )
        
        self.assertEqual(user.email, email.lower())
    
    def test_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='TestPass123!',
                full_name='Test User'
            )
    
    def test_user_activate_deactivate(self):
        """Test activating and deactivating a user."""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            full_name='Test User'
        )
        
        # Initially active
        self.assertEqual(user.status, 'active')
        
        # Deactivate
        user.deactivate()
        self.assertEqual(user.status, 'inactive')
        
        # Activate
        user.activate()
        self.assertEqual(user.status, 'active')


class AuthenticationTests(APITestCase):
    """Tests for authentication endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.signup_url = '/api/auth/signup/'
        self.login_url = '/api/auth/login/'
        self.logout_url = '/api/auth/logout/'
        self.me_url = '/api/auth/me/'
        
        # Create a test user
        self.test_user = User.objects.create_user(
            email='existing@example.com',
            password='ExistingPass123!',
            full_name='Existing User'
        )
    
    def test_user_signup_success(self):
        """Test successful user registration."""
        data = {
            'email': 'newuser@example.com',
            'password': 'NewUserPass123!',
            'confirm_password': 'NewUserPass123!',
            'full_name': 'New User'
        }
        
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])
        self.assertIn('access', response.data['data']['tokens'])
        self.assertIn('refresh', response.data['data']['tokens'])
    
    def test_user_signup_duplicate_email(self):
        """Test signup with existing email fails."""
        data = {
            'email': 'existing@example.com',
            'password': 'NewPass123!',
            'confirm_password': 'NewPass123!',
            'full_name': 'Duplicate User'
        }
        
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
    
    def test_user_signup_weak_password(self):
        """Test signup with weak password fails."""
        data = {
            'email': 'weakpass@example.com',
            'password': 'weak',
            'confirm_password': 'weak',
            'full_name': 'Weak Password User'
        }
        
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_signup_password_mismatch(self):
        """Test signup with mismatched passwords fails."""
        data = {
            'email': 'mismatch@example.com',
            'password': 'Password123!',
            'confirm_password': 'DifferentPass123!',
            'full_name': 'Mismatch User'
        }
        
        response = self.client.post(self.signup_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_success(self):
        """Test successful user login."""
        data = {
            'email': 'existing@example.com',
            'password': 'ExistingPass123!'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials fails."""
        data = {
            'email': 'existing@example.com',
            'password': 'WrongPassword123!'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
    
    def test_user_login_inactive_account(self):
        """Test login with inactive account fails."""
        self.test_user.deactivate()
        
        data = {
            'email': 'existing@example.com',
            'password': 'ExistingPass123!'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_current_user(self):
        """Test getting current user info."""
        # Login first
        login_data = {
            'email': 'existing@example.com',
            'password': 'ExistingPass123!'
        }
        login_response = self.client.post(self.login_url, login_data)
        token = login_response.data['data']['tokens']['access']
        
        # Get current user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['user']['email'], 'existing@example.com')


class UserProfileTests(APITestCase):
    """Tests for user profile endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.profile_url = '/api/users/profile/'
        self.change_password_url = '/api/users/change-password/'
        
        # Create and authenticate a test user
        self.test_user = User.objects.create_user(
            email='testuser@example.com',
            password='TestPass123!',
            full_name='Test User'
        )
        
        # Get token
        login_response = self.client.post('/api/auth/login/', {
            'email': 'testuser@example.com',
            'password': 'TestPass123!'
        })
        self.token = login_response.data['data']['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_update_profile_success(self):
        """Test successful profile update."""
        data = {
            'full_name': 'Updated Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(self.profile_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['user']['full_name'], 'Updated Name')
        self.assertEqual(response.data['data']['user']['email'], 'updated@example.com')
    
    def test_change_password_success(self):
        """Test successful password change."""
        data = {
            'current_password': 'TestPass123!',
            'new_password': 'NewTestPass123!',
            'confirm_new_password': 'NewTestPass123!'
        }
        
        response = self.client.post(self.change_password_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify new password works
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('NewTestPass123!'))
    
    def test_change_password_wrong_current(self):
        """Test password change with wrong current password fails."""
        data = {
            'current_password': 'WrongPassword123!',
            'new_password': 'NewTestPass123!',
            'confirm_new_password': 'NewTestPass123!'
        }
        
        response = self.client.post(self.change_password_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminUserManagementTests(APITestCase):
    """Tests for admin user management endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPass123!',
            full_name='Admin User'
        )
        
        # Create regular users
        self.regular_user = User.objects.create_user(
            email='regular@example.com',
            password='RegularPass123!',
            full_name='Regular User'
        )
        
        # Get admin token
        login_response = self.client.post('/api/auth/login/', {
            'email': 'admin@example.com',
            'password': 'AdminPass123!'
        })
        self.admin_token = login_response.data['data']['tokens']['access']
        
        # Get regular user token
        login_response = self.client.post('/api/auth/login/', {
            'email': 'regular@example.com',
            'password': 'RegularPass123!'
        })
        self.user_token = login_response.data['data']['tokens']['access']
    
    def test_admin_list_users(self):
        """Test admin can list all users."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/admin/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('users', response.data['data'])
    
    def test_regular_user_cannot_list_users(self):
        """Test regular user cannot list all users."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get('/api/admin/users/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_deactivate_user(self):
        """Test admin can deactivate a user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(f'/api/admin/users/{self.regular_user.id}/deactivate/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.status, 'inactive')
    
    def test_admin_activate_user(self):
        """Test admin can activate a user."""
        # First deactivate the user
        self.regular_user.deactivate()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(f'/api/admin/users/{self.regular_user.id}/activate/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.status, 'active')
    
    def test_admin_cannot_deactivate_self(self):
        """Test admin cannot deactivate their own account."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(f'/api/admin/users/{self.admin_user.id}/deactivate/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
