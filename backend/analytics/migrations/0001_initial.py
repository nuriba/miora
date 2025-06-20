# Generated by Django 4.2.7 on 2025-06-18 10:14

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
            name="SizeAnalytics",
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
                ("brand", models.CharField(max_length=100)),
                ("garment_category", models.CharField(max_length=50)),
                ("recommended_size", models.CharField(max_length=10)),
                ("actual_size", models.CharField(blank=True, max_length=10)),
                (
                    "fit_score",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("return_reported", models.BooleanField(default=False)),
                ("height_range", models.CharField(blank=True, max_length=20)),
                ("weight_range", models.CharField(blank=True, max_length=20)),
                ("body_type", models.CharField(blank=True, max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "size_analytics",
                "indexes": [
                    models.Index(
                        fields=["brand", "created_at"],
                        name="size_analyt_brand_d3e2f1_idx",
                    ),
                    models.Index(
                        fields=["garment_category", "created_at"],
                        name="size_analyt_garment_788d8f_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="FeatureUsage",
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
                ("feature_name", models.CharField(max_length=100)),
                ("action", models.CharField(max_length=100)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "feature_usage",
                "indexes": [
                    models.Index(
                        fields=["feature_name", "created_at"],
                        name="feature_usa_feature_d67420_idx",
                    ),
                    models.Index(
                        fields=["user", "created_at"],
                        name="feature_usa_user_id_9da78f_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="APIRequestLog",
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
                ("endpoint", models.CharField(max_length=255)),
                ("method", models.CharField(max_length=10)),
                ("status_code", models.IntegerField(blank=True, null=True)),
                ("response_time_ms", models.IntegerField(blank=True, null=True)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "api_request_logs",
                "indexes": [
                    models.Index(
                        fields=["user", "created_at"],
                        name="api_request_user_id_6fe1fb_idx",
                    ),
                    models.Index(
                        fields=["endpoint", "created_at"],
                        name="api_request_endpoin_7a4754_idx",
                    ),
                ],
            },
        ),
    ]
