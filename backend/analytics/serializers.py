from rest_framework import serializers
from .models import SizeAnalytics, APIRequestLog, FeatureUsage


class SizeAnalyticsSerializer(serializers.ModelSerializer):
    """Read-only serializer for size analytics."""
    
    class Meta:
        model = SizeAnalytics
        fields = '__all__'
        read_only_fields = '__all__'


class BrandAnalyticsRequestSerializer(serializers.Serializer):
    """Serializer for brand analytics requests."""
    brand = serializers.CharField(max_length=100)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    garment_category = serializers.CharField(max_length=50, required=False)


class APIRequestLogSerializer(serializers.ModelSerializer):
    """Read-only serializer for API request logs."""
    
    class Meta:
        model = APIRequestLog
        fields = '__all__'
        read_only_fields = '__all__'


class FeatureUsageSerializer(serializers.ModelSerializer):
    """Serializer for feature usage tracking."""
    
    class Meta:
        model = FeatureUsage
        fields = ('feature_name', 'action', 'metadata', 'created_at')
        read_only_fields = ('created_at',)
    
    def create(self, validated_data):
        # Add user from context if authenticated
        if self.context['request'].user.is_authenticated:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)