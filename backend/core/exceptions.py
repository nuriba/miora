from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger('miora.api')


def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses."""
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    logger.error(f'API Exception: {exc}', exc_info=True)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data
        }
        
        # Customize error messages
        if isinstance(exc, ValidationError):
            custom_response_data['message'] = 'Validation failed'
            custom_response_data['errors'] = response.data
            del custom_response_data['details']
        elif isinstance(exc, Http404):
            custom_response_data['message'] = 'Resource not found'
            custom_response_data['details'] = str(exc)
        elif isinstance(exc, PermissionDenied):
            custom_response_data['message'] = 'Permission denied'
            custom_response_data['details'] = str(exc)
        
        response.data = custom_response_data
    
    return response