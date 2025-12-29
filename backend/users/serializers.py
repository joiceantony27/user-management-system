"""
Serializers for User Management System.
"""
import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - used for reading user data."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'status',
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']


class UserSignupSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'confirm_password']
    
    def validate_email(self, value):
        """Validate email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError('Please enter a valid email address.')
        
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        
        return value.lower()
    
    def validate_full_name(self, value):
        """Validate full name."""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('Full name must be at least 2 characters long.')
        return value.strip()
    
    def validate_password(self, value):
        """Validate password strength."""
        # Check minimum length
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        
        # Check for at least one digit
        if not re.search(r'\d', value):
            raise serializers.ValidationError('Password must contain at least one digit.')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        
        # Django's built-in password validation
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        
        return value
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_email(self, value):
        """Normalize email to lowercase."""
        return value.lower()
    
    def validate(self, attrs):
        """Validate user credentials."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            
            if not user:
                raise serializers.ValidationError({
                    'detail': 'Invalid email or password.'
                })
            
            if user.status == 'inactive':
                raise serializers.ValidationError({
                    'detail': 'Your account has been deactivated. Please contact an administrator.'
                })
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError({
                'detail': 'Both email and password are required.'
            })
        
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = ['email', 'full_name']
    
    def validate_email(self, value):
        """Validate email format and uniqueness."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError('Please enter a valid email address.')
        
        # Check uniqueness, excluding current user
        user = self.context.get('request').user
        if User.objects.filter(email=value.lower()).exclude(id=user.id).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        
        return value.lower()
    
    def validate_full_name(self, value):
        """Validate full name."""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('Full name must be at least 2 characters long.')
        return value.strip()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    
    current_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        min_length=8
    )
    confirm_new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_current_password(self, value):
        """Validate that current password is correct."""
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        # Check minimum length
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        
        # Check for at least one digit
        if not re.search(r'\d', value):
            raise serializers.ValidationError('Password must contain at least one digit.')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        
        # Django's built-in password validation
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        
        return value
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            raise serializers.ValidationError({
                'confirm_new_password': 'New passwords do not match.'
            })
        
        # Check that new password is different from current
        if attrs.get('current_password') == attrs.get('new_password'):
            raise serializers.ValidationError({
                'new_password': 'New password must be different from current password.'
            })
        
        return attrs


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin to update user status."""
    
    class Meta:
        model = User
        fields = ['status']
    
    def validate_status(self, value):
        """Validate status value."""
        if value not in ['active', 'inactive']:
            raise serializers.ValidationError('Status must be either "active" or "inactive".')
        return value
