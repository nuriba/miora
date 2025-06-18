from django.db import models
from django.conf import settings
import uuid


class UserProfile(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('tr', 'Turkish'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    language_preference = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    privacy_level = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.email}'s profile"