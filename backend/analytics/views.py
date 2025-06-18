from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import SizeAnalytics, FeatureUsage
from .serializers import (
    SizeAnalyticsSerializer,
    BrandAnalyticsRequestSerializer,
    FeatureUsageSerializer
)


class BrandAnalyticsView(APIView):
    """Get analytics for brand (anonymized)."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = BrandAnalyticsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        brand = serializer.validated_data['brand']
        date_from = serializer.validated_data.get('date_from', timezone.now().date() - timedelta(days=30))
        date_to = serializer.validated_data.get('date_to', timezone.now().date())
        category = serializer.validated_data.get('garment_category')
        
        # Build query
        query = Q(brand__iexact=brand) & Q(created_at__date__gte=date_from) & Q(created_at__date__lte=date_to)
        if category:
            query &= Q(garment_category=category)
        
        # Get analytics
        analytics = SizeAnalytics.objects.filter(query)
        
        # Aggregate data
        summary = {
            'brand': brand,
            'period': {
                'from': date_from,
                'to': date_to
            },
            'total_recommendations': analytics.count(),
            'size_distribution': analytics.values('recommended_size').annotate(
                count=Count('id'),
                avg_fit_score=Avg('fit_score')
            ),
            'return_rate': analytics.filter(return_reported=True).count() / max(analytics.count(), 1) * 100,
            'average_fit_score': analytics.aggregate(Avg('fit_score'))['fit_score__avg'] or 0,
            'body_type_distribution': analytics.values('body_type').annotate(count=Count('id'))
        }
        
        return Response(summary)


class TrackFeatureUsageView(generics.CreateAPIView):
    """Track feature usage."""
    serializer_class = FeatureUsageSerializer
    permission_classes = [permissions.AllowAny]  # Allow anonymous tracking
    
    def perform_create(self, serializer):
        # Add user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class UserStatsView(APIView):
    """Get user statistics."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        stats = {
            'avatars_count': user.avatars.count(),
            'garments_count': user.garments.filter(processing_status='completed').count(),
            'outfits_count': user.outfits.count(),
            'tryon_sessions_count': user.tryon_sessions.count(),
            'favorite_outfits_count': user.outfits.filter(is_favorite=True).count(),
            'recent_activity': {
                'last_tryon': user.tryon_sessions.order_by('-created_at').first(),
                'last_garment_added': user.garments.order_by('-created_at').first(),
                'last_outfit_saved': user.outfits.order_by('-created_at').first()
            }
        }
        
        # Serialize recent activity
        if stats['recent_activity']['last_tryon']:
            stats['recent_activity']['last_tryon'] = stats['recent_activity']['last_tryon'].created_at
        if stats['recent_activity']['last_garment_added']:
            stats['recent_activity']['last_garment_added'] = stats['recent_activity']['last_garment_added'].created_at
        if stats['recent_activity']['last_outfit_saved']:
            stats['recent_activity']['last_outfit_saved'] = stats['recent_activity']['last_outfit_saved'].created_at
        
        return Response(stats)