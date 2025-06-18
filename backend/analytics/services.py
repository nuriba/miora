from datetime import datetime
from typing import Dict, Any
import logging
from .models import SizeAnalytics

logger = logging.getLogger('miora.analytics')


class AnalyticsService:
    """Service for analytics tracking."""
    
    @staticmethod
    def track_size_recommendation(garment, avatar, recommendation):
        """Track size recommendation for analytics."""
        try:
            # Anonymize measurements
            height_range = AnalyticsService._get_range(avatar.height, 10)
            weight_range = AnalyticsService._get_range(avatar.weight, 10) if avatar.weight else None
            
            SizeAnalytics.objects.create(
                brand=garment.brand or 'Unknown',
                garment_category=garment.category,
                recommended_size=recommendation.recommended_size,
                fit_score=recommendation.confidence_score,
                height_range=height_range,
                weight_range=weight_range,
                body_type=avatar.body_type or 'average'
            )
            
        except Exception as e:
            logger.error(f'Failed to track size recommendation: {str(e)}')
    
    @staticmethod
    def track_size_feedback(recommendation):
        """Track user feedback on size recommendation."""
        try:
            # Find related analytics entry
            analytics = SizeAnalytics.objects.filter(
                recommended_size=recommendation.recommended_size,
                garment_category=recommendation.garment.category,
                brand=recommendation.garment.brand,
                created_at__date=datetime.now().date()
            ).first()
            
            if analytics:
                analytics.actual_size = recommendation.user_selected_size
                
                # Mark as return if user selected different size or reported issue
                if (recommendation.user_selected_size != recommendation.recommended_size or
                    recommendation.user_feedback in ['too_small', 'too_large']):
                    analytics.return_reported = True
                
                analytics.save()
                
        except Exception as e:
            logger.error(f'Failed to track size feedback: {str(e)}')
    
    @staticmethod
    def _get_range(value: float, step: int) -> str:
        """Convert value to range string."""
        if not value:
            return 'Unknown'
        
        lower = int(value // step) * step
        upper = lower + step
        return f"{lower}-{upper}"