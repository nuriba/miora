from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SizeRecommendation
from .serializers import (
    SizeRecommendationSerializer,
    SizeRecommendationRequestSerializer,
    SizeRecommendationFeedbackSerializer
)
from .services import SizeRecommendationService
from analytics.services import AnalyticsService


class GetSizeRecommendationView(APIView):
    """Get size recommendation for avatar-garment combination."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = SizeRecommendationRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        avatar = serializer.validated_data['avatar']
        garment = serializer.validated_data['garment']
        fit_preference = serializer.validated_data['fit_preference']
        
        # Get recommendation
        service = SizeRecommendationService()
        result = service.get_recommendation(
            avatar=avatar,
            garment=garment,
            fit_preference=fit_preference
        )
        
        # Save recommendation
        recommendation = SizeRecommendation.objects.create(
            user=request.user,
            avatar=avatar,
            garment=garment,
            recommended_size=result['recommended_size'],
            confidence_score=result['confidence_score'],
            alternative_size=result.get('alternative_size', ''),
            fit_preference=fit_preference
        )
        
        # Track anonymous analytics
        AnalyticsService.track_size_recommendation(
            garment=garment,
            avatar=avatar,
            recommendation=recommendation
        )
        
        return Response({
            'recommendation': SizeRecommendationSerializer(recommendation).data,
            'details': result
        })


class ProvideFeedbackView(APIView):
    """Provide feedback on size recommendation."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = SizeRecommendationFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        recommendation_id = serializer.validated_data['recommendation_id']
        
        try:
            recommendation = SizeRecommendation.objects.get(
                id=recommendation_id,
                user=request.user
            )
        except SizeRecommendation.DoesNotExist:
            return Response({
                'detail': 'Recommendation not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update recommendation
        recommendation.user_selected_size = serializer.validated_data['user_selected_size']
        recommendation.user_feedback = serializer.validated_data['user_feedback']
        recommendation.save()
        
        # Update analytics
        AnalyticsService.track_size_feedback(recommendation)
        
        return Response({
            'detail': 'Feedback recorded successfully.',
            'recommendation': SizeRecommendationSerializer(recommendation).data
        })


class RecommendationHistoryView(generics.ListAPIView):
    """Get user's recommendation history."""
    serializer_class = SizeRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SizeRecommendation.objects.filter(
            user=self.request.user
        ).select_related('avatar', 'garment').order_by('-created_at')
