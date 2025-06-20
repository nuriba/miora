# Generated by Django 4.2.7 on 2025-06-15 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("display_name", models.CharField(blank=True, max_length=100)),
                ("avatar_url", models.URLField(blank=True, max_length=500)),
                ("bio", models.TextField(blank=True)),
                (
                    "language_preference",
                    models.CharField(
                        choices=[("en", "English"), ("tr", "Turkish")],
                        default="en",
                        max_length=10,
                    ),
                ),
                (
                    "privacy_level",
                    models.CharField(
                        choices=[
                            ("public", "Public"),
                            ("friends", "Friends Only"),
                            ("private", "Private"),
                        ],
                        default="private",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "user_profiles",
            },
        ),
    ]
