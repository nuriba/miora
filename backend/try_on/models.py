from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TryOnSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tryon_sessions')
    avatar = models.ForeignKey('avatars.Avatar', on_delete=models.SET_NULL, null=True, related_name='tryon_sessions')
    session_name = models.CharField(max_length=200, blank=True)
    
    # Session results
    fit_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    recommended_size = models.CharField(max_length=10, blank=True)
    confidence_level = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Analytics
    session_duration_seconds = models.IntegerField(null=True, blank=True)
    viewport_interactions = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tryon_sessions'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Try-on session for {self.user.email} - {self.created_at}"


class TryOnSessionGarment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(TryOnSession, on_delete=models.CASCADE, related_name='garments')
    garment = models.ForeignKey('garments.Garment', on_delete=models.CASCADE)
    layer_order = models.IntegerField(validators=[MinValueValidator(1)])  # 1=innermost
    selected_size = models.CharField(max_length=10, blank=True)
    fit_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    class Meta:
        db_table = 'tryon_session_garments'
        unique_together = ['session', 'layer_order']
        ordering = ['layer_order']


class Outfit(models.Model):
    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('friends', 'Friends Only'),
        ('public', 'Public'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outfits')
    avatar = models.ForeignKey('avatars.Avatar', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    is_favorite = models.BooleanField(default=False)
    privacy_level = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='private')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'outfits'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', 'is_favorite']),
        ]
    
    def __str__(self):
        return f"{self.name} by {self.user.email}"


class OutfitGarment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='garments')
    garment = models.ForeignKey('garments.Garment', on_delete=models.CASCADE)
    layer_order = models.IntegerField(validators=[MinValueValidator(1)])
    selected_size = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'outfit_garments'
        unique_together = ['outfit', 'layer_order']
        ordering = ['layer_order']


class OutfitTemplate(models.Model):
    """Pre-defined outfit combinations"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    occasion = models.CharField(max_length=50, choices=[
        ('casual', 'Casual'),
        ('business', 'Business'),
        ('formal', 'Formal'),
        ('sport', 'Sport'),
        ('party', 'Party'),
    ])
    season = models.CharField(max_length=20, choices=[
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
        ('all', 'All Seasons'),
    ])
    style_tags = models.JSONField(default=list)
    
class StyleRule(models.Model):
    """Fashion rules for outfit compatibility"""
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=50, choices=[
        ('color_match', 'Color Matching'),
        ('pattern_mix', 'Pattern Mixing'),
        ('formality', 'Formality Level'),
        ('seasonal', 'Seasonal Appropriateness'),
    ])
    compatible_items = models.JSONField()  # List of compatible categories/styles
    incompatible_items = models.JSONField()  # List of incompatible items
    confidence_score = models.FloatField(default=1.0)

class OutfitRating(models.Model):
    """Community ratings for outfits"""
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    style_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    fit_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)