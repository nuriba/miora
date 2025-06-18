from django.db import models
from django.conf import settings
from garments.models import Garment
from try_on.models import TryOnSession, Outfit

class StyleAnalytics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Color preferences
    dominant_colors = models.JSONField(default=list)
    color_frequency = models.JSONField(default=dict)
    favorite_color_combinations = models.JSONField(default=list)
    
    # Style preferences
    preferred_styles = models.JSONField(default=list)
    style_evolution_timeline = models.JSONField(default=list)
    
    # Fit preferences
    preferred_fits = models.JSONField(default=dict)
    size_consistency = models.JSONField(default=dict)
    
    # Brand preferences
    top_brands = models.JSONField(default=list)
    brand_loyalty_score = models.FloatField(default=0.0)
    
    # Seasonal patterns
    seasonal_preferences = models.JSONField(default=dict)
    weather_adaptation_score = models.FloatField(default=0.0)
    
    # Sustainability metrics
    garment_reuse_rate = models.FloatField(default=0.0)
    cost_per_wear = models.JSONField(default=dict)
    sustainability_score = models.FloatField(default=0.0)
    
    # Usage patterns
    most_worn_items = models.JSONField(default=list)
    least_worn_items = models.JSONField(default=list)
    outfit_repetition_rate = models.FloatField(default=0.0)
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Style Analytics for {self.user.username}"

class WearEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
    date_worn = models.DateField()
    occasion = models.CharField(max_length=100, blank=True)
    weather = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    
    class Meta:
        unique_together = ['user', 'garment', 'date_worn']

class StyleMilestone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    milestone_type = models.CharField(max_length=50, choices=[
        ('first_outfit', 'First Outfit Created'),
        ('style_evolution', 'Style Evolution'),
        ('sustainability_goal', 'Sustainability Goal Reached'),
        ('brand_diversity', 'Brand Diversity Achievement'),
        ('color_mastery', 'Color Combination Mastery'),
    ])
    title = models.CharField(max_length=200)
    description = models.TextField()
    achieved_at = models.DateTimeField()
    data = models.JSONField(default=dict)

class TrendAnalysis(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    trend_score = models.FloatField()
    adoption_rate = models.FloatField()
    seasonal_relevance = models.JSONField(default=dict)
    demographic_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.trend_score}%" 