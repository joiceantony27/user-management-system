"""
URL configuration for User Management System project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root endpoint with basic information."""
    return JsonResponse({
        'message': 'Welcome to User Management System API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'users': '/api/users/',
            'admin': '/api/admin/',
        },
        'documentation': '/api/docs/',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include('users.urls')),
]
