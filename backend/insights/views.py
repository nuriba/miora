from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import StyleAnalytics, WearEvent, StyleMilestone, TrendAnalysis
from .serializers import (
    StyleAnalyticsSerializer,
    WearEventSerializer,
    StyleMilestoneSerializer,
    TrendAnalysisSerializer
)
from .services import StyleAnalyticsService, MilestoneService

class StyleAnalyticsView(generics.RetrieveAPIView):
    serializer_class = StyleAnalyticsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        analytics, created = StyleAnalytics.objects.get_or_create(user=self.request.user)
        if created or not analytics.last_updated:
            # Update analytics if newly created or never updated
            service = StyleAnalyticsService(self.request.user)
            service.update_all_analytics()
            analytics.refresh_from_db()
        return analytics

class UpdateAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        service = StyleAnalyticsService(request.user)
        service.update_all_analytics()
        
        # Check for new milestones
        milestone_service = MilestoneService(request.user)
        milestone_service.check_and_create_milestones()
        
        return Response({'status': 'Analytics updated successfully'}, status=status.HTTP_200_OK)

class WearEventListCreateView(generics.ListCreateAPIView):
    serializer_class = WearEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WearEvent.objects.filter(user=self.request.user).order_by('-date_worn')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WearEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WearEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WearEvent.objects.filter(user=self.request.user)

class StyleMilestoneListView(generics.ListAPIView):
    serializer_class = StyleMilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StyleMilestone.objects.filter(user=self.request.user).order_by('-achieved_at')

class TrendAnalysisListView(generics.ListAPIView):
    serializer_class = TrendAnalysisSerializer
    permission_classes = [IsAuthenticated]
    queryset = TrendAnalysis.objects.all().order_by('-created_at')

class ColorAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analytics = StyleAnalytics.objects.filter(user=request.user).first()
        if not analytics:
            return Response({'error': 'No analytics data available'}, status=status.HTTP_404_NOT_FOUND)
        
        color_data = {
            'dominant_colors': analytics.dominant_colors,
            'color_frequency': analytics.color_frequency,
            'favorite_combinations': analytics.favorite_color_combinations
        }
        return Response(color_data)

class StyleEvolutionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analytics = StyleAnalytics.objects.filter(user=request.user).first()
        if not analytics:
            return Response({'error': 'No analytics data available'}, status=status.HTTP_404_NOT_FOUND)
        
        evolution_data = {
            'timeline': analytics.style_evolution_timeline,
            'preferred_styles': analytics.preferred_styles,
            'milestones': list(StyleMilestone.objects.filter(user=request.user).values())
        }
        return Response(evolution_data)

class SustainabilityInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analytics = StyleAnalytics.objects.filter(user=request.user).first()
        if not analytics:
            return Response({'error': 'No analytics data available'}, status=status.HTTP_404_NOT_FOUND)
        
        sustainability_data = {
            'reuse_rate': analytics.garment_reuse_rate,
            'cost_per_wear': analytics.cost_per_wear,
            'sustainability_score': analytics.sustainability_score,
            'most_worn_items': analytics.most_worn_items,
            'least_worn_items': analytics.least_worn_items
        }
        return Response(sustainability_data) 