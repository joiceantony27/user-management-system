"""
Custom exception handler for consistent error responses.
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework import status
from django.http import Http404


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'An error occurred',
            'errors': None,
        }
        
        # Handle different exception types
        if isinstance(exc, ValidationError):
            custom_response_data['message'] = 'Validation error'
            custom_response_data['errors'] = response.data
            
        elif isinstance(exc, AuthenticationFailed):
            custom_response_data['message'] = str(exc.detail)
            response.status_code = status.HTTP_401_UNAUTHORIZED
            
        elif isinstance(exc, NotAuthenticated):
            custom_response_data['message'] = 'Authentication credentials were not provided.'
            response.status_code = status.HTTP_401_UNAUTHORIZED
            
        elif isinstance(exc, PermissionDenied):
            custom_response_data['message'] = str(exc.detail)
            response.status_code = status.HTTP_403_FORBIDDEN
            
        elif isinstance(exc, Http404):
            custom_response_data['message'] = 'Resource not found.'
            response.status_code = status.HTTP_404_NOT_FOUND
            
        else:
            # For other exceptions, try to get detail from response
            if hasattr(exc, 'detail'):
                if isinstance(exc.detail, dict):
                    custom_response_data['errors'] = exc.detail
                    # Get first error message
                    for key, value in exc.detail.items():
                        if isinstance(value, list):
                            custom_response_data['message'] = value[0]
                        else:
                            custom_response_data['message'] = str(value)
                        break
                else:
                    custom_response_data['message'] = str(exc.detail)
            else:
                custom_response_data['message'] = str(exc)
        
        response.data = custom_response_data
    
    return response
