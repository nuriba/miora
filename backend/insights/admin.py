from django.contrib import admin
from .models import StyleAnalytics, WearEvent, StyleMilestone, TrendAnalysis

@admin.register(StyleAnalytics)
class StyleAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'sustainability_score', 'brand_loyalty_score', 'weather_adaptation_score', 'last_updated')
    list_filter = ('last_updated', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('last_updated', 'created_at')

@admin.register(WearEvent)
class WearEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'garment', 'date_worn', 'occasion', 'weather', 'rating')
    list_filter = ('date_worn', 'weather', 'rating', 'occasion')
    search_fields = ('user__username', 'garment__name', 'occasion', 'location')
    date_hierarchy = 'date_worn'

@admin.register(StyleMilestone)
class StyleMilestoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'milestone_type', 'title', 'achieved_at')
    list_filter = ('milestone_type', 'achieved_at')
    search_fields = ('user__username', 'title', 'description')
    readonly_fields = ('achieved_at',)

@admin.register(TrendAnalysis)
class TrendAnalysisAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'trend_score', 'adoption_rate', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category')
    readonly_fields = ('created_at',) 