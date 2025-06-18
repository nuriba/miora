from typing import Dict, Any, Optional
import numpy as np
from django.db.models import Avg, Count
import logging

logger = logging.getLogger('miora.recommendations')


class SizeRecommendationService:
    """Service for size recommendations."""
    
    def get_recommendation(self, avatar, garment, fit_preference: str = 'regular') -> Dict[str, Any]:
        """Get size recommendation for avatar-garment combination."""
        try:
            # Get available sizes
            available_sizes = self._get_available_sizes(garment)
            
            if not available_sizes:
                return {
                    'success': False,
                    'error': 'No size information available',
                    'recommended_size': '',
                    'confidence_score': 0
                }
            
            # Calculate fit scores for each size
            size_scores = {}
            for size in available_sizes:
                score = self.calculate_fit_score(avatar, garment, size, fit_preference)
                size_scores[size] = score
            
            # Find best size
            best_size = max(size_scores, key=size_scores.get)
            best_score = size_scores[best_size]
            
            # Find alternative if borderline
            alternative_size = self._find_alternative_size(
                size_scores,
                best_size,
                fit_preference
            )
            
            # Calculate confidence
            confidence = self._calculate_confidence(
                size_scores,
                best_size,
                garment
            )
            
            return {
                'success': True,
                'recommended_size': best_size,
                'fit_score': round(best_score, 2),
                'confidence_score': round(confidence, 2),
                'alternative_size': alternative_size,
                'size_scores': size_scores,
                'fit_preference': fit_preference
            }
            
        except Exception as e:
            logger.error(f'Size recommendation error: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'recommended_size': '',
                'confidence_score': 0
            }
    
    def calculate_fit_score(self, avatar, garment, size: str, 
                           fit_preference: str = 'regular') -> float:
        """Calculate fit score for specific size."""
        # Get size measurements
        size_measurements = self._get_size_measurements(garment, size)
        
        if not size_measurements:
            return 0
        
        # Base fit score
        base_score = self._calculate_base_fit_score(avatar, size_measurements)
        
        # Adjust for fit preference
        adjusted_score = self._adjust_for_preference(
            base_score,
            avatar,
            size_measurements,
            fit_preference
        )
        
        # Adjust for garment category
        final_score = self._adjust_for_category(
            adjusted_score,
            garment.category
        )
        
        return min(100, max(0, final_score))
    
    def _get_available_sizes(self, garment) -> list:
        """Get available sizes for garment."""
        if garment.available_sizes:
            return garment.available_sizes
        
        if garment.size_chart:
            return list(garment.size_chart.keys())
        
        # Default sizes
        return ['XS', 'S', 'M', 'L', 'XL']
    
    def _get_size_measurements(self, garment, size: str) -> Optional[Dict[str, float]]:
        """Get measurements for specific size."""
        # Check garment size chart
        if garment.size_chart and size in garment.size_chart:
            return garment.size_chart[size]
        
        # Check brand size chart
        from garments.models import BrandSizeChart
        try:
            brand_chart = BrandSizeChart.objects.get(
                brand=garment.brand,
                garment_type=garment.category,
                gender=garment.gender
            )
            if size in brand_chart.size_data:
                return brand_chart.size_data[size]
        except BrandSizeChart.DoesNotExist:
            pass
        
        # Fallback to standard sizes
        return self._get_standard_size_measurements(size, garment.category)
    
    def _get_standard_size_measurements(self, size: str, category: str) -> Dict[str, float]:
        """Get standard size measurements."""
        # Standard unisex sizes (simplified)
        standard_sizes = {
            'XS': {'chest': 85, 'waist': 70, 'hips': 85},
            'S': {'chest': 90, 'waist': 75, 'hips': 90},
            'M': {'chest': 95, 'waist': 80, 'hips': 95},
            'L': {'chest': 100, 'waist': 85, 'hips': 100},
            'XL': {'chest': 105, 'waist': 90, 'hips': 105},
            'XXL': {'chest': 110, 'waist': 95, 'hips': 110}
        }
        
        return standard_sizes.get(size, standard_sizes['M'])
    
    def _calculate_base_fit_score(self, avatar, size_measurements: Dict[str, float]) -> float:
        """Calculate base fit score."""
        scores = []
        weights = {
            'chest': 0.4,
            'waist': 0.3,
            'hips': 0.3
        }
        
        for measurement, weight in weights.items():
            if hasattr(avatar, measurement) and measurement in size_measurements:
                avatar_value = float(getattr(avatar, measurement))
                size_value = float(size_measurements[measurement])
                
                # Calculate fit score for this measurement
                diff_percent = abs(avatar_value - size_value) / avatar_value * 100
                
                if diff_percent <= 2:
                    score = 100
                elif diff_percent <= 5:
                    score = 85
                elif diff_percent <= 8:
                    score = 70
                elif diff_percent <= 12:
                    score = 50
                elif diff_percent <= 15:
                    score = 30
                else:
                    score = 10
                
                scores.append(score * weight)
        
        return sum(scores) / sum(weights.values()) if scores else 50
    
    def _adjust_for_preference(self, base_score: float, avatar, 
                              size_measurements: Dict[str, float], 
                              preference: str) -> float:
        """Adjust score based on fit preference."""
        adjustment = 0
        
        # Calculate average difference
        diffs = []
        for measurement in ['chest', 'waist', 'hips']:
            if hasattr(avatar, measurement) and measurement in size_measurements:
                avatar_value = float(getattr(avatar, measurement))
                size_value = float(size_measurements[measurement])
                diffs.append(size_value - avatar_value)
        
        avg_diff = np.mean(diffs) if diffs else 0
        
        if preference == 'slim':
            # Prefer slightly smaller sizes
            if avg_diff < 0:  # Size is smaller than avatar
                adjustment = 5
            elif avg_diff > 5:  # Size is much larger
                adjustment = -10
        elif preference == 'relaxed':
            # Prefer slightly larger sizes
            if avg_diff > 0 and avg_diff < 10:  # Size is slightly larger
                adjustment = 5
            elif avg_diff < -5:  # Size is much smaller
                adjustment = -10
        
        return base_score + adjustment
    
    def _adjust_for_category(self, score: float, category: str) -> float:
        """Adjust score based on garment category."""
        # Some categories are more forgiving
        category_adjustments = {
            't-shirt': 5,
            'sweater': 5,
            'jacket': 3,
            'coat': 3,
            'dress': 0,
            'shirt': -2,
            'pants': -2,
            'jeans': -3
        }
        
        adjustment = category_adjustments.get(category, 0)
        return score + adjustment
    
    def _find_alternative_size(self, size_scores: Dict[str, float], 
                               best_size: str, preference: str) -> Optional[str]:
        """Find alternative size for borderline cases."""
        # If best score is low, suggest alternative
        if size_scores[best_size] < 80:
            # Sort sizes by score
            sorted_sizes = sorted(size_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Get second best if close enough
            if len(sorted_sizes) > 1:
                second_best_size, second_best_score = sorted_sizes[1]
                if second_best_score > size_scores[best_size] - 10:
                    return second_best_size
        
        return None
    
    def _calculate_confidence(self, size_scores: Dict[str, float], 
                             best_size: str, garment) -> float:
        """Calculate confidence in recommendation."""
        confidence_factors = []
        
        # Factor 1: How good is the best score
        best_score = size_scores[best_size]
        if best_score >= 90:
            confidence_factors.append(1.0)
        elif best_score >= 80:
            confidence_factors.append(0.8)
        elif best_score >= 70:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Factor 2: How much better is best than alternatives
        sorted_scores = sorted(size_scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            score_gap = sorted_scores[0] - sorted_scores[1]
            if score_gap > 20:
                confidence_factors.append(1.0)
            elif score_gap > 10:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)
        
        # Factor 3: Do we have brand-specific size data
        if garment.size_chart:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.6)
        
        return np.mean(confidence_factors) * 100
