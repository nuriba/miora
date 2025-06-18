from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import OutfitPost, StyleChallenge, ChallengeParticipation
from .serializers import (
    OutfitPostSerializer,
    StyleChallengeSerializer,
    ChallengeParticipationSerializer
)

# Create your views here.

class OutfitPostListCreateView(generics.ListCreateAPIView):
    queryset = OutfitPost.objects.all()
    serializer_class = OutfitPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OutfitPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OutfitPost.objects.all()
    serializer_class = OutfitPostSerializer
    permission_classes = [IsAuthenticated]

class OutfitPostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(OutfitPost, pk=pk)
        post.likes_count += 1
        post.save()
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

class OutfitPostShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(OutfitPost, pk=pk)
        post.shares_count += 1
        post.save()
        return Response({'status': 'shared'}, status=status.HTTP_200_OK)

class StyleChallengeListCreateView(generics.ListCreateAPIView):
    queryset = StyleChallenge.objects.all()
    serializer_class = StyleChallengeSerializer
    permission_classes = [IsAuthenticated]

class StyleChallengeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StyleChallenge.objects.all()
    serializer_class = StyleChallengeSerializer
    permission_classes = [IsAuthenticated]

class ChallengeJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        challenge = get_object_or_404(StyleChallenge, pk=pk)
        participation, created = ChallengeParticipation.objects.get_or_create(
            user=request.user,
            challenge=challenge
        )
        serializer = ChallengeParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class ChallengeSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        challenge = get_object_or_404(StyleChallenge, pk=pk)
        participation = get_object_or_404(
            ChallengeParticipation,
            user=request.user,
            challenge=challenge
        )
        
        outfit_post_id = request.data.get('outfit_post_id')
        if not outfit_post_id:
            return Response(
                {'error': 'outfit_post_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        outfit_post = get_object_or_404(OutfitPost, pk=outfit_post_id)
        participation.submission = outfit_post
        participation.status = 'submitted'
        participation.save()
        
        serializer = ChallengeParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_200_OK)
