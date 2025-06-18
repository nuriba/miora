from rest_framework import serializers
from .models import Avatar, AvatarGenerationLog
from django.conf import settings


class AvatarSerializer(serializers.ModelSerializer):
    """Serializer for avatar details."""
    
    class Meta:
        model = Avatar
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'model_file_url', 'thumbnail_url')
    
    def validate(self, data):
        # Validate that user doesn't exceed max avatars
        user = self.context['request'].user
        max_avatars = settings.MIORA_SETTINGS.get('MAX_AVATARS_PER_USER', 5)
        
        if self.instance is None:  # Creating new avatar
            current_count = Avatar.objects.filter(user=user).count()
            if current_count >= max_avatars:
                raise serializers.ValidationError(
                    f"You can only have up to {max_avatars} avatars."
                )
        
        # Validate measurements are reasonable
        if 'height' in data and not (50 <= data['height'] <= 250):
            raise serializers.ValidationError("Height must be between 50cm and 250cm")
        
        if 'chest' in data and not (50 <= data['chest'] <= 200):
            raise serializers.ValidationError("Chest measurement must be between 50cm and 200cm")
        
        if 'waist' in data and not (40 <= data['waist'] <= 200):
            raise serializers.ValidationError("Waist measurement must be between 40cm and 200cm")
        
        if 'hips' in data and not (50 <= data['hips'] <= 200):
            raise serializers.ValidationError("Hips measurement must be between 50cm and 200cm")
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AvatarCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating avatar with minimal required fields."""
    
    class Meta:
        model = Avatar
        fields = ('name', 'height', 'chest', 'waist', 'hips', 'weight', 
                 'shoulder_width', 'arm_length', 'inseam', 'neck',
                 'skin_tone', 'hair_color', 'hair_style', 'body_type')
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # If this is the first avatar, make it active
        if not Avatar.objects.filter(user=validated_data['user']).exists():
            validated_data['is_active'] = True
        return super().create(validated_data)


class AvatarGenerationLogSerializer(serializers.ModelSerializer):
    """Serializer for avatar generation logs."""
    
    class Meta:
        model = AvatarGenerationLog
        fields = '__all__'
        read_only_fields = '__all__'