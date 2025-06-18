from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid


class Avatar(models.Model):
    BODY_TYPE_CHOICES = [
        ('ectomorph', 'Ectomorph'),
        ('mesomorph', 'Mesomorph'),
        ('endomorph', 'Endomorph'),
        ('athletic', 'Athletic'),
        ('average', 'Average'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avatars')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    
    # Body measurements (in centimeters)
    height = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(50)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(20)], null=True, blank=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(50)])
    waist = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(40)])
    hips = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(50)])
    shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    arm_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    inseam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neck = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Avatar customization
    skin_tone = models.CharField(max_length=20, blank=True)
    hair_color = models.CharField(max_length=20, blank=True)
    hair_style = models.CharField(max_length=50, blank=True)
    body_type = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES, default='average')
    
    # 3D model data
    model_file_url = models.URLField(max_length=500, blank=True)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'avatars'
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.email}'s avatar: {self.name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active avatar per user
        if self.is_active:
            Avatar.objects.filter(user=self.user, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class AvatarGenerationLog(models.Model):
    GENERATION_METHOD_CHOICES = [
        ('manual', 'Manual'),
        ('photo', 'Photo'),
        ('scan', '3D Scan'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, related_name='generation_logs')
    generation_method = models.CharField(max_length=50, choices=GENERATION_METHOD_CHOICES)
    source_images = models.JSONField(default=list, blank=True)  # Array of image URLs
    processing_time_ms = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'avatar_generation_logs'