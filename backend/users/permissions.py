"""
Custom permissions for User Management System.
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class that only allows admin users.
    """
    message = 'You must be an admin to perform this action.'
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )


class IsActiveUser(permissions.BasePermission):
    """
    Permission class that only allows active users.
    """
    message = 'Your account is inactive. Please contact an administrator.'
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.status == 'active'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class that allows access to owners or admin users.
    """
    message = 'You do not have permission to access this resource.'
    
    def has_object_permission(self, request, view, obj):
        # Admin can access any user's data
        if request.user.role == 'admin':
            return True
        # Users can only access their own data
        return obj.id == request.user.id
