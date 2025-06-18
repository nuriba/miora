from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """Get and update user profile."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class PublicProfileView(generics.RetrieveAPIView):
    """Get public profile by user ID."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        profile = get_object_or_404(UserProfile, user__id=user_id)
        
        # Check privacy settings
        if profile.privacy_level == 'private' and profile.user != self.request.user:
            self.permission_denied(
                self.request,
                message="This profile is private."
            )
        
        return profile