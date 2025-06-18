from django.contrib import admin
from .models import TryOnSession, TryOnSessionGarment, Outfit, OutfitGarment

@admin.register(TryOnSession)
class TryOnSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'fit_score', 'recommended_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email']

@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_favorite', 'privacy_level', 'created_at']
    list_filter = ['is_favorite', 'privacy_level']
    search_fields = ['name', 'user__email']