from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class SizeRecommendation(models.Model):
    FIT_PREFERENCE_CHOICES = [
        ('slim', 'Slim Fit'),
        ('regular', 'Regular Fit'),
        ('relaxed', 'Relaxed Fit'),
    ]
    
    USER_FEEDBACK_CHOICES = [
        ('perfect', 'Perfect Fit'),
        ('too_small', 'Too Small'),
        ('too_large', 'Too Large'),
        ('too_short', 'Too Short'),
        ('too_long', 'Too Long'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='size_recommendations')
    avatar = models.ForeignKey('avatars.Avatar', on_delete=models.SET_NULL, null=True)
    garment = models.ForeignKey('garments.Garment', on_delete=models.CASCADE, related_name='size_recommendations')
    
    # Recommendation details
    recommended_size = models.CharField(max_length=10)
    confidence_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    alternative_size = models.CharField(max_length=10, blank=True)
    fit_preference = models.CharField(max_length=20, choices=FIT_PREFERENCE_CHOICES, default='regular')
    
    # User feedback
    user_selected_size = models.CharField(max_length=10, blank=True)
    user_feedback = models.CharField(max_length=20, choices=USER_FEEDBACK_CHOICES, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'size_recommendations'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['garment']),
        ]