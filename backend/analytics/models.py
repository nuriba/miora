from django.db import models
from django.conf import settings
import uuid


class SizeAnalytics(models.Model):
    """Anonymous analytics for brands - no user linkage"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=100)
    garment_category = models.CharField(max_length=50)
    recommended_size = models.CharField(max_length=10)
    actual_size = models.CharField(max_length=10, blank=True)
    fit_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    return_reported = models.BooleanField(default=False)
    
    # Anonymous measurement ranges
    height_range = models.CharField(max_length=20, blank=True)  # e.g., "170-180"
    weight_range = models.CharField(max_length=20, blank=True)  # e.g., "70-80"
    body_type = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'size_analytics'
        indexes = [
            models.Index(fields=['brand', 'created_at']),
            models.Index(fields=['garment_category', 'created_at']),
        ]


class APIRequestLog(models.Model):
    """For rate limiting and monitoring"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField(null=True, blank=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'api_request_logs'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['endpoint', 'created_at']),
        ]


class FeatureUsage(models.Model):
    """Track feature usage for analytics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    feature_name = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'feature_usage'
        indexes = [
            models.Index(fields=['feature_name', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]
