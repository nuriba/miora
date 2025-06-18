from typing import Dict, Any, List
from django.db.models import Avg
import numpy as np
import logging

logger = logging.getLogger('miora.try_on')


class VirtualTryOnService:
    """Service for virtual try-on simulation."""
    
    def simulate(self, session) -> Dict[str, Any]:
        """Run virtual try-on simulation."""
        try:
            avatar = session.avatar
            garments = session.garments.all().order_by('layer_order')
            
            # Initialize simulation
            simulation_results = []
            overall_fit_scores = []
            
            for session_garment in garments:
                garment = session_garment.garment
                
                # Simulate garment on avatar
                result = self._simulate_garment(
                    avatar,
                    garment,
                    session_garment.selected_size,
                    session_garment.layer_order
                )
                
                simulation_results.append(result)
                overall_fit_scores.append(result['fit_score'])
            
            # Calculate overall scores
            overall_fit_score = np.mean(overall_fit_scores) if overall_fit_scores else 0
            confidence = self._calculate_confidence(simulation_results)
            
            return {
                'success': True,
                'overall_fit_score': round(overall_fit_score, 2),
                'confidence': round(confidence, 2),
                'garment_results': simulation_results
            }
            
        except Exception as e:
            logger.error(f'Try-on simulation error: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'overall_fit_score': 0,
                'confidence': 0
            }
    
    def _simulate_garment(self, avatar, garment, size: str, layer: int) -> Dict[str, Any]:
        """Simulate single garment on avatar."""
        # Get garment measurements for size
        size_measurements = self._get_size_measurements(garment, size)
        
        # Calculate fit score
        fit_score = self._calculate_fit_score(
            avatar,
            garment,
            size_measurements
        )
        
        # Simulate cloth physics (placeholder)
        physics_result = self._simulate_physics(
            avatar,
            garment,
            size_measurements,
            layer
        )
        
        return {
            'garment_id': str(garment.id),
            'size': size,
            'fit_score': fit_score,
            'physics': physics_result,
            'issues': self._detect_fit_issues(fit_score, physics_result)
        }
    
    def _get_size_measurements(self, garment, size: str) -> Dict[str, float]:
        """Get measurements for specific size."""
        if garment.size_chart and size in garment.size_chart:
            return garment.size_chart[size]
        
        # Fallback to standard sizes
        standard_sizes = {
            'S': {'chest': 90, 'waist': 75, 'hips': 90},
            'M': {'chest': 95, 'waist': 80, 'hips': 95},
            'L': {'chest': 100, 'waist': 85, 'hips': 100},
            'XL': {'chest': 105, 'waist': 90, 'hips': 105}
        }
        
        return standard_sizes.get(size, standard_sizes['M'])
    
    def _calculate_fit_score(self, avatar, garment, size_measurements: Dict[str, float]) -> float:
        """Calculate fit score based on measurements."""
        scores = []
        
        # Compare measurements
        measurement_pairs = [
            ('chest', 'chest'),
            ('waist', 'waist'),
            ('hips', 'hips')
        ]
        
        for avatar_attr, size_attr in measurement_pairs:
            if hasattr(avatar, avatar_attr) and size_attr in size_measurements:
                avatar_value = float(getattr(avatar, avatar_attr))
                size_value = float(size_measurements[size_attr])
                
                # Calculate difference percentage
                diff_percent = abs(avatar_value - size_value) / avatar_value * 100
                
                # Convert to score (0-100)
                if diff_percent <= 2:
                    score = 100
                elif diff_percent <= 5:
                    score = 90
                elif diff_percent <= 10:
                    score = 70
                elif diff_percent <= 15:
                    score = 50
                else:
                    score = 30
                
                scores.append(score)
        
        return np.mean(scores) if scores else 50
    
    def _simulate_physics(self, avatar, garment, size_measurements: Dict[str, float], 
                         layer: int) -> Dict[str, Any]:
        """Simulate cloth physics."""
        # Placeholder physics simulation
        # In reality, would use a physics engine
        
        return {
            'drape_quality': 0.85,
            'stretch_areas': [],
            'collision_areas': [],
            'movement_restriction': 0.1
        }
    
    def _calculate_confidence(self, results: List[Dict[str, Any]]) -> float:
        """Calculate confidence in simulation results."""
        if not results:
            return 0
        
        # Factors affecting confidence
        confidence_factors = []
        
        for result in results:
            # Higher fit scores increase confidence
            fit_confidence = result['fit_score'] / 100
            
            # Good physics simulation increases confidence
            physics_confidence = result['physics']['drape_quality']
            
            confidence_factors.append((fit_confidence + physics_confidence) / 2)
        
        return np.mean(confidence_factors) * 100
    
    def _detect_fit_issues(self, fit_score: float, physics_result: Dict[str, Any]) -> List[str]:
        """Detect potential fit issues."""
        issues = []
        
        if fit_score < 50:
            issues.append('Poor overall fit')
        elif fit_score < 70:
            issues.append('Marginal fit')
        
        if physics_result['stretch_areas']:
            issues.append('Excessive stretching detected')
        
        if physics_result['collision_areas']:
            issues.append('Clipping detected')
        
        if physics_result['movement_restriction'] > 0.3:
            issues.append('May restrict movement')
        
        return issues