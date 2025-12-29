"""
Views for User Management System.
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import (
    UserSerializer,
    UserSignupSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    AdminUserUpdateSerializer,
)
from .permissions import IsAdmin, IsActiveUser


def get_tokens_for_user(user):
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignupView(APIView):
    """
    User registration endpoint.
    
    POST /api/auth/signup/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            
            return Response({
                'success': True,
                'message': 'User registered successfully.',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': tokens,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Validation error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    User login endpoint.
    
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.update_last_login()
            tokens = get_tokens_for_user(user)
            
            return Response({
                'success': True,
                'message': 'Login successful.',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': tokens,
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Validation error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout endpoint - blacklists the refresh token.
    
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({
                    'success': False,
                    'message': 'Refresh token is required.',
                    'errors': {'refresh': ['This field is required.']},
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logged out successfully.',
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response({
                'success': False,
                'message': 'Invalid or expired token.',
                'errors': {'refresh': [str(e)]},
            }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshAPIView(TokenRefreshView):
    """
    Token refresh endpoint.
    
    POST /api/auth/token/refresh/
    """
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            return Response({
                'success': True,
                'message': 'Token refreshed successfully.',
                'data': {
                    'tokens': response.data,
                }
            }, status=status.HTTP_200_OK)
        
        return response


class CurrentUserView(APIView):
    """
    Get current authenticated user information.
    
    GET /api/auth/me/
    """
    permission_classes = [IsAuthenticated, IsActiveUser]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'message': 'User data retrieved successfully.',
            'data': {
                'user': serializer.data,
            }
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    User profile management.
    
    GET /api/users/profile/ - Get profile
    PUT /api/users/profile/ - Update profile
    """
    permission_classes = [IsAuthenticated, IsActiveUser]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'message': 'Profile retrieved successfully.',
            'data': {
                'user': serializer.data,
            }
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            context={'request': request},
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully.',
                'data': {
                    'user': UserSerializer(request.user).data,
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Validation error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Change user password.
    
    POST /api/users/change-password/
    """
    permission_classes = [IsAuthenticated, IsActiveUser]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'success': True,
                'message': 'Password changed successfully.',
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Validation error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class AdminUserListView(generics.ListAPIView):
    """
    Admin endpoint to list all users with pagination.
    
    GET /api/admin/users/
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        
        # Optional filtering
        status_filter = self.request.query_params.get('status')
        if status_filter in ['active', 'inactive']:
            queryset = queryset.filter(status=status_filter)
        
        role_filter = self.request.query_params.get('role')
        if role_filter in ['admin', 'user']:
            queryset = queryset.filter(role=role_filter)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(email__icontains=search) |
                models.Q(full_name__icontains=search)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'Users retrieved successfully.',
            'data': {
                'count': response.data.get('count', len(response.data.get('results', []))),
                'next': response.data.get('next'),
                'previous': response.data.get('previous'),
                'users': response.data.get('results', response.data),
            }
        }, status=status.HTTP_200_OK)


class AdminUserDetailView(APIView):
    """
    Admin endpoint to view a specific user.
    
    GET /api/admin/users/<id>/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        
        return Response({
            'success': True,
            'message': 'User retrieved successfully.',
            'data': {
                'user': serializer.data,
            }
        }, status=status.HTTP_200_OK)


class AdminActivateUserView(APIView):
    """
    Admin endpoint to activate a user account.
    
    POST /api/admin/users/<id>/activate/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if user.status == 'active':
            return Response({
                'success': False,
                'message': 'User is already active.',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.activate()
        
        return Response({
            'success': True,
            'message': f'User {user.email} has been activated successfully.',
            'data': {
                'user': UserSerializer(user).data,
            }
        }, status=status.HTTP_200_OK)


class AdminDeactivateUserView(APIView):
    """
    Admin endpoint to deactivate a user account.
    
    POST /api/admin/users/<id>/deactivate/
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Prevent self-deactivation
        if user.id == request.user.id:
            return Response({
                'success': False,
                'message': 'You cannot deactivate your own account.',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user.status == 'inactive':
            return Response({
                'success': False,
                'message': 'User is already inactive.',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.deactivate()
        
        return Response({
            'success': True,
            'message': f'User {user.email} has been deactivated successfully.',
            'data': {
                'user': UserSerializer(user).data,
            }
        }, status=status.HTTP_200_OK)
