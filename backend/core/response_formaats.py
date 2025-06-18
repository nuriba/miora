from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """Standardized API response format."""
    
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        """Return success response."""
        response_data = {
            'success': True,
            'message': message,
        }
        if data is not None:
            response_data['data'] = data
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message="An error occurred", errors=None, 
              status_code=status.HTTP_400_BAD_REQUEST):
        """Return error response."""
        response_data = {
            'success': False,
            'message': message,
        }
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(data=None, message="Created successfully"):
        """Return created response."""
        return APIResponse.success(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def deleted(message="Deleted successfully"):
        """Return deleted response."""
        return APIResponse.success(
            message=message,
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    @staticmethod
    def not_found(message="Resource not found"):
        """Return not found response."""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(message="Unauthorized"):
        """Return unauthorized response."""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message="Forbidden"):
        """Return forbidden response."""
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )