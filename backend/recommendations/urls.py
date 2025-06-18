from django.urls import path
from .views import (
    GetSizeRecommendationView,
    ProvideFeedbackView,
    RecommendationHistoryView
)

app_name = 'recommendations'

urlpatterns = [
    path('get/', GetSizeRecommendationView.as_view(), name='get_recommendation'),
    path('feedback/', ProvideFeedbackView.as_view(), name='provide_feedback'),
    path('history/', RecommendationHistoryView.as_view(), name='recommendation_history'),
]