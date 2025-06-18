from django.contrib import admin
from .models import OutfitPost, StyleChallenge, ChallengeParticipation

@admin.register(OutfitPost)
class OutfitPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'likes_count', 'comments_count', 'shares_count', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('user__username', 'caption', 'location', 'occasion')

@admin.register(StyleChallenge)
class StyleChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'start_date', 'end_date')
    list_filter = ('theme', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'theme')

@admin.register(ChallengeParticipation)
class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status', 'joined_at')
    list_filter = ('status', 'joined_at')
    search_fields = ('user__username', 'challenge__title')
