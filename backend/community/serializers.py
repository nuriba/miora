from rest_framework import serializers
from .models import OutfitPost, StyleChallenge, ChallengeParticipation
from try_on.serializers import OutfitSerializer
from accounts.serializers import UserSerializer

class OutfitPostSerializer(serializers.ModelSerializer):
    outfit = OutfitSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = OutfitPost
        fields = '__all__'
        read_only_fields = ('likes_count', 'comments_count', 'shares_count', 'is_featured')

class StyleChallengeSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StyleChallenge
        fields = '__all__'
        read_only_fields = ('participants_count',)
    
    def get_participants_count(self, obj):
        return obj.participants.count()

class ChallengeParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    challenge = StyleChallengeSerializer(read_only=True)
    submission = OutfitPostSerializer(read_only=True)
    
    class Meta:
        model = ChallengeParticipation
        fields = '__all__'
        read_only_fields = ('status',) 