from django.contrib import admin
from .models import SizeRecommendation

@admin.register(SizeRecommendation)
class SizeRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'garment', 'recommended_size', 'confidence_score', 'user_feedback']
    list_filter = ['fit_preference', 'user_feedback']
    search_fields = ['user__email', 'garment__name']