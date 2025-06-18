from rest_framework import serializers
from .models import StyleAnalytics, WearEvent, StyleMilestone, TrendAnalysis

class StyleAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleAnalytics
        fields = '__all__'
        read_only_fields = ('user', 'last_updated', 'created_at')

class WearEventSerializer(serializers.ModelSerializer):
    garment_name = serializers.CharField(source='garment.name', read_only=True)
    garment_category = serializers.CharField(source='garment.category', read_only=True)
    
    class Meta:
        model = WearEvent
        fields = '__all__'
        read_only_fields = ('user',)

class StyleMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleMilestone
        fields = '__all__'
        read_only_fields = ('user', 'achieved_at')

class TrendAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAnalysis
        fields = '__all__'
        read_only_fields = ('created_at',) 