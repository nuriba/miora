from rest_framework import serializers
from .models import SizeRecommendation
from avatars.models import Avatar
from garments.models import Garment


class SizeRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for size recommendations."""
    
    class Meta:
        model = SizeRecommendation
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'recommended_size', 
                           'confidence_score', 'alternative_size')


class SizeRecommendationRequestSerializer(serializers.Serializer):
    """Serializer for requesting size recommendation."""
    avatar_id = serializers.UUIDField()
    garment_id = serializers.UUIDField()
    fit_preference = serializers.ChoiceField(
        choices=['slim', 'regular', 'relaxed'],
        default='regular'
    )
    
    def validate(self, data):
        user = self.context['request'].user
        
        # Validate avatar
        try:
            avatar = Avatar.objects.get(id=data['avatar_id'], user=user)
            data['avatar'] = avatar
        except Avatar.DoesNotExist:
            raise serializers.ValidationError("Avatar not found")
        
        # Validate garment
        try:
            garment = Garment.objects.get(id=data['garment_id'], user=user)
            if garment.processing_status != 'completed':
                raise serializers.ValidationError("Garment is still processing")
            data['garment'] = garment
        except Garment.DoesNotExist:
            raise serializers.ValidationError("Garment not found")
        
        return data


class SizeRecommendationFeedbackSerializer(serializers.Serializer):
    """Serializer for providing feedback on size recommendation."""
    recommendation_id = serializers.UUIDField()
    user_selected_size = serializers.CharField(max_length=10)
    user_feedback = serializers.ChoiceField(
        choices=['perfect', 'too_small', 'too_large', 'too_short', 'too_long']
    )