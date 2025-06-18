from django.db import models
from django.conf import settings
from try_on.models import Outfit

class OutfitPost(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    caption = models.TextField()
    hashtags = models.JSONField(default=list)
    location = models.CharField(max_length=100, blank=True)
    occasion = models.CharField(max_length=50, blank=True)
    
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s outfit post - {self.created_at}"

    class Meta:
        ordering = ['-created_at']

class StyleChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    theme = models.CharField(max_length=100)
    required_items = models.JSONField(default=list)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    prizes = models.JSONField(default=dict)
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ChallengeParticipation'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']

class ChallengeParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge = models.ForeignKey(StyleChallenge, on_delete=models.CASCADE)
    submission = models.ForeignKey(OutfitPost, on_delete=models.SET_NULL, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('joined', 'Joined'),
            ('submitted', 'Submitted'),
            ('completed', 'Completed'),
            ('winner', 'Winner')
        ],
        default='joined'
    )

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

    class Meta:
        unique_together = ['user', 'challenge']
