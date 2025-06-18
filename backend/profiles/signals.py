from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from avatars.models import Avatar


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_avatar(sender, instance, created, **kwargs):
    """Create a default avatar for new users."""
    if created:
        Avatar.objects.create(
            user=instance,
            name="Default Avatar",
            is_active=True,
            height=170,  # Default height
            chest=90,    # Default chest
            waist=75,    # Default waist
            hips=90,     # Default hips
        )