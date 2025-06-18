from django.urls import path
from .views import (
    BrandAnalyticsView,
    TrackFeatureUsageView,
    UserStatsView
)

app_name = 'analytics'

urlpatterns = [
    path('brand/', BrandAnalyticsView.as_view(), name='brand_analytics'),
    path('track/', TrackFeatureUsageView.as_view(), name='track_usage'),
    path('user-stats/', UserStatsView.as_view(), name='user_stats'),
]