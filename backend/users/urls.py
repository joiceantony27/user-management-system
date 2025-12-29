"""
URL configuration for User Management System.
"""
from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    TokenRefreshAPIView,
    CurrentUserView,
    UserProfileView,
    ChangePasswordView,
    AdminUserListView,
    AdminUserDetailView,
    AdminActivateUserView,
    AdminDeactivateUserView,
)

urlpatterns = [
    # Authentication endpoints
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshAPIView.as_view(), name='token-refresh'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
    
    # User profile endpoints
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Admin endpoints
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:user_id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:user_id>/activate/', AdminActivateUserView.as_view(), name='admin-activate-user'),
    path('admin/users/<int:user_id>/deactivate/', AdminDeactivateUserView.as_view(), name='admin-deactivate-user'),
]
