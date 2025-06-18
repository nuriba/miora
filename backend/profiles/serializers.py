from rest_framework import serializers
from .models import UserProfile
from accounts.serializers import UserSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = UserProfile
        fields = ('display_name', 'avatar_url', 'bio', 'language_preference', 'privacy_level')
    
    def validate_privacy_level(self, value):
        valid_levels = ['public', 'friends', 'private']
        if value not in valid_levels:
            raise serializers.ValidationError(f"Privacy level must be one of {valid_levels}")
        return value