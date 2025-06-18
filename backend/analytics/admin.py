from django.contrib import admin
from .models import SizeAnalytics, APIRequestLog, FeatureUsage

@admin.register(SizeAnalytics)
class SizeAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['brand', 'garment_category', 'recommended_size', 'fit_score', 'created_at']
    list_filter = ['brand', 'garment_category', 'return_reported']
    date_hierarchy = 'created_at'

@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'endpoint', 'method', 'status_code', 'response_time_ms', 'created_at']
    list_filter = ['method', 'status_code']
    search_fields = ['user__email', 'endpoint']
    date_hierarchy = 'created_at'

@admin.register(FeatureUsage)
class FeatureUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'feature_name', 'action', 'created_at']
    list_filter = ['feature_name', 'action']
    search_fields = ['user__email']
    date_hierarchy = 'created_at'