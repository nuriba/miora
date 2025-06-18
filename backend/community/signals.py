from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OutfitPost, ChallengeParticipation

@receiver(post_save, sender=OutfitPost)
def handle_outfit_post_creation(sender, instance, created, **kwargs):
    """
    Signal handler for when an OutfitPost is created.
    Could be used for notifications, activity feeds, etc.
    """
    if created:
        # Add any post-creation logic here
        pass

@receiver(post_save, sender=ChallengeParticipation)
def handle_challenge_participation_update(sender, instance, **kwargs):
    """
    Signal handler for when a ChallengeParticipation is updated.
    Handles status changes and challenge completion.
    """
    if instance.status == 'submitted':
        # Add any submission handling logic here
        pass
    elif instance.status == 'winner':
        # Add any winner handling logic here
        pass 