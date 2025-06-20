# Generated by Django 4.2.7 on 2025-06-15 10:51

from django.conf import settings
import django.core.validators
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
            name="Garment",
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
                ("name", models.CharField(max_length=200)),
                ("brand", models.CharField(blank=True, max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("shirt", "Shirt"),
                            ("t-shirt", "T-Shirt"),
                            ("pants", "Pants"),
                            ("jeans", "Jeans"),
                            ("dress", "Dress"),
                            ("skirt", "Skirt"),
                            ("jacket", "Jacket"),
                            ("coat", "Coat"),
                            ("sweater", "Sweater"),
                            ("shorts", "Shorts"),
                            ("suit", "Suit"),
                            ("activewear", "Activewear"),
                            ("underwear", "Underwear"),
                            ("accessories", "Accessories"),
                        ],
                        max_length=50,
                    ),
                ),
                ("subcategory", models.CharField(blank=True, max_length=50)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("unisex", "Unisex"),
                        ],
                        default="unisex",
                        max_length=20,
                    ),
                ),
                ("original_image_url", models.URLField(max_length=500)),
                ("thumbnail_url", models.URLField(blank=True, max_length=500)),
                ("model_3d_url", models.URLField(blank=True, max_length=500)),
                ("texture_urls", models.JSONField(blank=True, default=list)),
                ("source_url", models.URLField(blank=True, max_length=500)),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("currency", models.CharField(default="USD", max_length=3)),
                ("size_chart", models.JSONField(blank=True, default=dict)),
                ("available_sizes", models.JSONField(blank=True, default=list)),
                ("material_properties", models.JSONField(blank=True, default=dict)),
                ("color", models.CharField(blank=True, max_length=50)),
                ("pattern", models.CharField(blank=True, max_length=50)),
                ("is_private", models.BooleanField(default=False)),
                (
                    "processing_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="garments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "garments",
            },
        ),
        migrations.CreateModel(
            name="GarmentProcessingLog",
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
                (
                    "processing_step",
                    models.CharField(
                        choices=[
                            ("upload", "Upload"),
                            ("image_processing", "Image Processing"),
                            ("3d_generation", "3D Generation"),
                            ("validation", "Validation"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("started", "Started"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        max_length=50,
                    ),
                ),
                ("processing_time_ms", models.IntegerField(blank=True, null=True)),
                ("error_message", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "garment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="processing_logs",
                        to="garments.garment",
                    ),
                ),
            ],
            options={
                "db_table": "garment_processing_logs",
            },
        ),
        migrations.CreateModel(
            name="BrandSizeChart",
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
                ("garment_type", models.CharField(max_length=50)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("unisex", "Unisex"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "size_system",
                    models.CharField(
                        choices=[
                            ("US", "United States"),
                            ("EU", "European"),
                            ("UK", "United Kingdom"),
                            ("JP", "Japanese"),
                            ("CN", "Chinese"),
                            ("INT", "International"),
                        ],
                        max_length=20,
                    ),
                ),
                ("size_data", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "brand_size_charts",
                "unique_together": {("brand", "garment_type", "gender", "size_system")},
            },
        ),
        migrations.AddIndex(
            model_name="garment",
            index=models.Index(fields=["user"], name="garments_user_id_508213_idx"),
        ),
        migrations.AddIndex(
            model_name="garment",
            index=models.Index(fields=["category"], name="garments_categor_e80eed_idx"),
        ),
        migrations.AddIndex(
            model_name="garment",
            index=models.Index(
                fields=["processing_status"], name="garments_process_f8b846_idx"
            ),
        ),
    ]
