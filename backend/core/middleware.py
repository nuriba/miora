import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from analytics.models import APIRequestLog

logger = logging.getLogger('miora.api')


class APILoggingMiddleware(MiddlewareMixin):
    """Middleware to log API requests."""
    
    def process_request(self, request):
        """Log request start time."""
        request._start_time = time.time()
    
    def process_response(self, request, response):
        """Log API request details."""
        if request.path.startswith('/api/'):
            try:
                # Calculate response time
                response_time = None
                if hasattr(request, '_start_time'):
                    response_time = int((time.time() - request._start_time) * 1000)
                
                # Create log entry
                APIRequestLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    endpoint=request.path,
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=response_time,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
            except Exception as e:
                logger.error(f'Failed to log API request: {str(e)}')
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RateLimitMiddleware(MiddlewareMixin):
    """Simple rate limiting middleware."""
    
    def process_request(self, request):
        """Check rate limits."""
        if request.path.startswith('/api/'):
            # Skip rate limiting for authenticated users with higher limits
            if request.user.is_authenticated:
                return None
            
            # Simple IP-based rate limiting for anonymous users
            ip = APILoggingMiddleware().get_client_ip(request)
            
            # Count requests in last hour
            from django.utils import timezone
            from datetime import timedelta
            
            hour_ago = timezone.now() - timedelta(hours=1)
            request_count = APIRequestLog.objects.filter(
                ip_address=ip,
                created_at__gte=hour_ago
            ).count()
            
            # Check limit (100 requests per hour for anonymous)
            if request_count > 100:
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.'
                }, status=429)
        
        return None