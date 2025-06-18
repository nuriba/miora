from rest_framework import serializers
from .models import TryOnSession, TryOnSessionGarment, Outfit, OutfitGarment
from avatars.serializers import AvatarSerializer
from garments.serializers import GarmentSerializer
from django.conf import settings


class TryOnSessionGarmentSerializer(serializers.ModelSerializer):
    """Serializer for garments in try-on session."""
    garment = GarmentSerializer(read_only=True)
    garment_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = TryOnSessionGarment
        fields = ('id', 'garment', 'garment_id', 'layer_order', 'selected_size', 'fit_score')
        read_only_fields = ('id', 'fit_score')


class TryOnSessionSerializer(serializers.ModelSerializer):
    """Serializer for try-on session."""
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.UUIDField(write_only=True)
    garments = TryOnSessionGarmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = TryOnSession
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 
                           'fit_score', 'recommended_size', 'confidence_level')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TryOnSessionCreateSerializer(serializers.Serializer):
    """Serializer for creating a try-on session with garments."""
    avatar_id = serializers.UUIDField()
    garments = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=4  # Maximum 4 layers
    )
    session_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    def validate_avatar_id(self, value):
        user = self.context['request'].user
        try:
            avatar = Avatar.objects.get(id=value, user=user)
        except Avatar.DoesNotExist:
            raise serializers.ValidationError("Avatar not found or doesn't belong to you.")
        return value
    
    def validate_garments(self, value):
        # Validate each garment entry
        for idx, garment_data in enumerate(value):
            if 'garment_id' not in garment_data:
                raise serializers.ValidationError(
                    f"Garment at index {idx} must have 'garment_id'"
                )
            if 'layer_order' not in garment_data:
                raise serializers.ValidationError(
                    f"Garment at index {idx} must have 'layer_order'"
                )
            
            # Validate garment exists and belongs to user
            try:
                garment = Garment.objects.get(
                    id=garment_data['garment_id'],
                    user=self.context['request'].user
                )
                if garment.processing_status != 'completed':
                    raise serializers.ValidationError(
                        f"Garment {garment.name} is still processing"
                    )
            except Garment.DoesNotExist:
                raise serializers.ValidationError(
                    f"Garment {garment_data['garment_id']} not found"
                )
        
        # Validate layer orders are unique
        layer_orders = [g['layer_order'] for g in value]
        if len(layer_orders) != len(set(layer_orders)):
            raise serializers.ValidationError("Layer orders must be unique")
        
        return value


class OutfitGarmentSerializer(serializers.ModelSerializer):
    """Serializer for garments in outfit."""
    garment = GarmentSerializer(read_only=True)
    
    class Meta:
        model = OutfitGarment
        fields = ('id', 'garment', 'layer_order', 'selected_size')
        read_only_fields = ('id',)


class OutfitSerializer(serializers.ModelSerializer):
    """Serializer for outfit."""
    garments = OutfitGarmentSerializer(many=True, read_only=True)
    avatar = AvatarSerializer(read_only=True)
    
    class Meta:
        model = Outfit
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'thumbnail_url')
    
    def validate(self, data):
        # Validate user doesn't exceed max outfits
        user = self.context['request'].user
        max_outfits = settings.MIORA_SETTINGS.get('MAX_OUTFITS_PER_USER', 50)
        
        if self.instance is None:  # Creating new outfit
            current_count = Outfit.objects.filter(user=user).count()
            if current_count >= max_outfits:
                raise serializers.ValidationError(
                    f"You can only have up to {max_outfits} outfits."
                )
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OutfitCreateFromSessionSerializer(serializers.Serializer):
    """Serializer for creating outfit from try-on session."""
    session_id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    privacy_level = serializers.ChoiceField(
        choices=['private', 'friends', 'public'],
        default='private'
    )
    is_favorite = serializers.BooleanField(default=False)