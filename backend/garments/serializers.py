from rest_framework import serializers
from .models import Garment, GarmentProcessingLog, BrandSizeChart
from django.conf import settings


class GarmentSerializer(serializers.ModelSerializer):
    """Serializer for garment details."""
    processing_logs = serializers.SerializerMethodField()
    
    class Meta:
        model = Garment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 
                           'thumbnail_url', 'model_3d_url', 'texture_urls')
    
    def get_processing_logs(self, obj):
        # Only include logs if requested
        if self.context.get('include_logs', False):
            logs = obj.processing_logs.all().order_by('-created_at')
            return GarmentProcessingLogSerializer(logs, many=True).data
        return None
    
    def validate(self, data):
        # Validate user doesn't exceed max garments
        user = self.context['request'].user
        max_garments = settings.MIORA_SETTINGS.get('MAX_GARMENTS_PER_USER', 100)
        
        if self.instance is None:  # Creating new garment
            current_count = Garment.objects.filter(user=user).count()
            if current_count >= max_garments:
                raise serializers.ValidationError(
                    f"You can only have up to {max_garments} garments."
                )
        
        # Validate category
        valid_categories = settings.MIORA_SETTINGS.get('DEFAULT_GARMENT_CATEGORIES', [])
        if 'category' in data and data['category'] not in valid_categories:
            raise serializers.ValidationError(
                f"Category must be one of {valid_categories}"
            )
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['processing_status'] = 'pending'
        return super().create(validated_data)


class GarmentUploadSerializer(serializers.Serializer):
    """Serializer for garment upload."""
    name = serializers.CharField(max_length=200)
    category = serializers.ChoiceField(choices=Garment.CATEGORY_CHOICES)
    image = serializers.ImageField()
    brand = serializers.CharField(max_length=100, required=False, allow_blank=True)
    source_url = serializers.URLField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    currency = serializers.CharField(max_length=3, default='USD')
    color = serializers.CharField(max_length=50, required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=Garment.GENDER_CHOICES, default='unisex')
    
    def validate_image(self, value):
        # Validate image size
        max_size = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        if value.size > max_size:
            raise serializers.ValidationError(
                f"Image size cannot exceed {max_size / 1024 / 1024}MB"
            )
        
        # Validate image format
        allowed_formats = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in allowed_formats:
            raise serializers.ValidationError(
                f"Image format must be one of {allowed_formats}"
            )
        
        return value


class GarmentProcessingLogSerializer(serializers.ModelSerializer):
    """Serializer for garment processing logs."""
    
    class Meta:
        model = GarmentProcessingLog
        fields = '__all__'
        read_only_fields = '__all__'


class BrandSizeChartSerializer(serializers.ModelSerializer):
    """Serializer for brand size charts."""
    
    class Meta:
        model = BrandSizeChart
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_size_data(self, value):
        # Validate that size_data is a proper dictionary
        if not isinstance(value, dict):
            raise serializers.ValidationError("Size data must be a dictionary")
        
        # Validate that each size has required measurements
        for size, measurements in value.items():
            if not isinstance(measurements, dict):
                raise serializers.ValidationError(
                    f"Measurements for size {size} must be a dictionary"
                )
        
        return value