from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Garment(models.Model):
    CATEGORY_CHOICES = [
        ('shirt', 'Shirt'),
        ('t-shirt', 'T-Shirt'),
        ('pants', 'Pants'),
        ('jeans', 'Jeans'),
        ('dress', 'Dress'),
        ('skirt', 'Skirt'),
        ('jacket', 'Jacket'),
        ('coat', 'Coat'),
        ('sweater', 'Sweater'),
        ('shorts', 'Shorts'),
        ('suit', 'Suit'),
        ('activewear', 'Activewear'),
        ('underwear', 'Underwear'),
        ('accessories', 'Accessories'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    ]
    
    PROCESSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='garments')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='unisex')
    
    # Images and 3D model
    original_image_url = models.URLField(max_length=500)
    cleaned_image_url = models.URLField(max_length=500, blank=True)  # Background removed
    thumbnail_url = models.URLField(max_length=500, blank=True)
    model_3d_url = models.URLField(max_length=500, blank=True)
    texture_urls = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=dict, blank=True)  # AI-detected features
    
    # Garment metadata
    source_url = models.URLField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    size_chart = models.JSONField(default=dict, blank=True)
    available_sizes = models.JSONField(default=list, blank=True)
    material_properties = models.JSONField(default=dict, blank=True)
    color = models.CharField(max_length=50, blank=True)
    pattern = models.CharField(max_length=50, blank=True)
    
    # Privacy and status
    is_private = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=50, choices=PROCESSING_STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'garments'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['category']),
            models.Index(fields=['processing_status']),
        ]
    
    @property
    def image_url(self):
        """Backward compatibility property."""
        return self.original_image_url

    def __str__(self):
        return f"{self.name} ({self.category})"


class GarmentProcessingLog(models.Model):
    PROCESSING_STEP_CHOICES = [
        ('upload', 'Upload'),
        ('image_processing', 'Image Processing'),
        ('3d_generation', '3D Generation'),
        ('validation', 'Validation'),
    ]
    
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garment = models.ForeignKey(Garment, on_delete=models.CASCADE, related_name='processing_logs')
    processing_step = models.CharField(max_length=50, choices=PROCESSING_STEP_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    processing_time_ms = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'garment_processing_logs'


class BrandSizeChart(models.Model):
    SIZE_SYSTEM_CHOICES = [
        ('US', 'United States'),
        ('EU', 'European'),
        ('UK', 'United Kingdom'),
        ('JP', 'Japanese'),
        ('CN', 'Chinese'),
        ('INT', 'International'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=100)
    garment_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=Garment.GENDER_CHOICES, blank=True)
    size_system = models.CharField(max_length=20, choices=SIZE_SYSTEM_CHOICES)
    size_data = models.JSONField()  # Structured size measurements
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'brand_size_charts'
        unique_together = ['brand', 'garment_type', 'gender', 'size_system']
    
    def __str__(self):
        return f"{self.brand} - {self.garment_type} ({self.size_system})"