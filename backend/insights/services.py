from datetime import datetime, timedelta
from collections import Counter
from django.db.models import Count, Avg
from .models import StyleAnalytics, WearEvent, StyleMilestone
from garments.models import Garment
from try_on.models import TryOnSession, Outfit

class StyleAnalyticsService:
    def __init__(self, user):
        self.user = user
        self.analytics, _ = StyleAnalytics.objects.get_or_create(user=user)

    def update_color_analytics(self):
        """Update color preference analytics based on user's garments and wear events."""
        garments = Garment.objects.filter(user=self.user)
        wear_events = WearEvent.objects.filter(user=self.user)
        
        # Analyze dominant colors
        color_counts = Counter()
        for garment in garments:
            if garment.color:
                color_counts[garment.color] += 1
        
        # Weight by wear frequency
        for event in wear_events:
            if event.garment.color:
                color_counts[event.garment.color] += 2
        
        self.analytics.dominant_colors = list(color_counts.keys())[:10]
        self.analytics.color_frequency = dict(color_counts.most_common(20))
        
        # Analyze color combinations from outfits
        combinations = []
        # Get color combinations from outfits instead
        outfits = Outfit.objects.filter(user=self.user)
        for outfit in outfits:
            outfit_colors = []
            for outfit_garment in outfit.garments.all():
                if outfit_garment.garment.color:
                    outfit_colors.append(outfit_garment.garment.color)
            if len(outfit_colors) >= 2:
                # Create combinations of colors in the outfit
                for i in range(len(outfit_colors)):
                    for j in range(i + 1, len(outfit_colors)):
                        combo = sorted([outfit_colors[i], outfit_colors[j]])
                        combinations.append(tuple(combo))
        
        combo_counts = Counter(combinations)
        self.analytics.favorite_color_combinations = [
            list(combo) for combo, _ in combo_counts.most_common(10)
        ]

    def update_style_preferences(self):
        """Analyze style evolution and preferences."""
        garments = Garment.objects.filter(user=self.user).order_by('created_at')
        
        # Style preferences based on category since 'style' field doesn't exist
        style_counts = Counter(garment.category for garment in garments if garment.category)
        self.analytics.preferred_styles = list(style_counts.keys())[:10]
        
        # Style evolution timeline
        timeline = []
        for i in range(0, len(garments), max(1, len(garments) // 12)):  # 12 data points
            month_garments = garments[i:i+max(1, len(garments) // 12)]
            month_styles = Counter(g.category for g in month_garments if g.category)
            if month_styles:
                timeline.append({
                    'period': month_garments.first().created_at.strftime('%Y-%m'),
                    'dominant_style': month_styles.most_common(1)[0][0],
                    'style_diversity': len(month_styles)
                })
        
        self.analytics.style_evolution_timeline = timeline

    def update_fit_preferences(self):
        """Analyze fit and size preferences."""
        garments = Garment.objects.filter(user=self.user)
        wear_events = WearEvent.objects.filter(user=self.user)
        
        # Fit preferences based on ratings (using category as proxy for fit)
        fit_ratings = {}
        for event in wear_events:
            fit = event.garment.category  # Using category as proxy
            if fit:
                if fit not in fit_ratings:
                    fit_ratings[fit] = []
                fit_ratings[fit].append(event.rating)
        
        preferred_fits = {
            fit: sum(ratings) / len(ratings)
            for fit, ratings in fit_ratings.items()
        }
        self.analytics.preferred_fits = preferred_fits
        
        # Size consistency - using available_sizes field
        size_data = {}
        for garment in garments:
            category = garment.category
            if category and garment.available_sizes:
                if category not in size_data:
                    size_data[category] = Counter()
                # Count each available size
                for size in garment.available_sizes:
                    size_data[category][size] += 1
        
        self.analytics.size_consistency = {
            category: dict(sizes.most_common())
            for category, sizes in size_data.items()
        }

    def update_brand_analytics(self):
        """Analyze brand preferences and loyalty."""
        garments = Garment.objects.filter(user=self.user)
        
        brand_counts = Counter(garment.brand for garment in garments if garment.brand)
        self.analytics.top_brands = [
            {'brand': brand, 'count': count}
            for brand, count in brand_counts.most_common(10)
        ]
        
        # Brand loyalty score (0-1)
        total_garments = len(garments)
        if total_garments > 0:
            top_brand_count = brand_counts.most_common(1)[0][1] if brand_counts else 0
            self.analytics.brand_loyalty_score = top_brand_count / total_garments

    def update_seasonal_analytics(self):
        """Analyze seasonal preferences and weather adaptation."""
        wear_events = WearEvent.objects.filter(user=self.user)
        
        seasonal_data = {'spring': [], 'summer': [], 'fall': [], 'winter': []}
        weather_ratings = {}
        
        for event in wear_events:
            month = event.date_worn.month
            season = self._get_season(month)
            seasonal_data[season].append(event.garment.category)
            
            if event.weather:
                if event.weather not in weather_ratings:
                    weather_ratings[event.weather] = []
                weather_ratings[event.weather].append(event.rating)
        
        # Most worn categories by season
        seasonal_preferences = {}
        for season, items in seasonal_data.items():
            if items:
                category_counts = Counter(items)
                seasonal_preferences[season] = dict(category_counts.most_common(5))
        
        self.analytics.seasonal_preferences = seasonal_preferences
        
        # Weather adaptation score
        avg_weather_ratings = [
            sum(ratings) / len(ratings)
            for ratings in weather_ratings.values() if ratings
        ]
        self.analytics.weather_adaptation_score = (
            sum(avg_weather_ratings) / len(avg_weather_ratings)
            if avg_weather_ratings else 0.0
        ) / 5.0  # Normalize to 0-1

    def update_sustainability_metrics(self):
        """Calculate sustainability metrics."""
        garments = Garment.objects.filter(user=self.user)
        wear_events = WearEvent.objects.filter(user=self.user)
        
        # Garment reuse rate
        total_garments = len(garments)
        worn_garments = len(set(event.garment_id for event in wear_events))
        self.analytics.garment_reuse_rate = (
            worn_garments / total_garments if total_garments > 0 else 0.0
        )
        
        # Cost per wear
        cost_per_wear = {}
        for garment in garments:
            wear_count = wear_events.filter(garment=garment).count()
            if wear_count > 0 and garment.price:
                cost_per_wear[garment.id] = garment.price / wear_count
        
        self.analytics.cost_per_wear = cost_per_wear
        
        # Overall sustainability score (0-1)
        reuse_score = min(self.analytics.garment_reuse_rate, 1.0)
        avg_cost_per_wear = sum(cost_per_wear.values()) / len(cost_per_wear) if cost_per_wear else 100
        cost_efficiency_score = max(0, 1 - (avg_cost_per_wear / 100))  # Normalize assuming $100 is poor
        
        self.analytics.sustainability_score = (reuse_score + cost_efficiency_score) / 2

    def update_all_analytics(self):
        """Update all analytics for the user."""
        self.update_color_analytics()
        self.update_style_preferences()
        self.update_fit_preferences()
        self.update_brand_analytics()
        self.update_seasonal_analytics()
        self.update_sustainability_metrics()
        self.analytics.save()

    def _get_season(self, month):
        """Map month to season."""
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'

class MilestoneService:
    def __init__(self, user):
        self.user = user

    def check_and_create_milestones(self):
        """Check for new milestones and create them."""
        self._check_first_outfit_milestone()
        self._check_style_evolution_milestone()
        self._check_sustainability_milestone()
        self._check_brand_diversity_milestone()
        self._check_color_mastery_milestone()

    def _check_first_outfit_milestone(self):
        """Check if user created their first outfit."""
        if not StyleMilestone.objects.filter(
            user=self.user, 
            milestone_type='first_outfit'
        ).exists():
            # Check if user has any try-on sessions
            if TryOnSession.objects.filter(user=self.user).exists():
                StyleMilestone.objects.create(
                    user=self.user,
                    milestone_type='first_outfit',
                    title='First Virtual Try-On',
                    description='Congratulations on your first virtual try-on session!',
                    achieved_at=datetime.now(),
                    data={'session_count': 1}
                )

    def _check_style_evolution_milestone(self):
        """Check for style evolution milestones."""
        analytics = StyleAnalytics.objects.filter(user=self.user).first()
        if analytics and len(analytics.style_evolution_timeline) >= 6:
            if not StyleMilestone.objects.filter(
                user=self.user,
                milestone_type='style_evolution'
            ).exists():
                StyleMilestone.objects.create(
                    user=self.user,
                    milestone_type='style_evolution',
                    title='Style Evolution Expert',
                    description='Your style has evolved significantly over time!',
                    achieved_at=datetime.now(),
                    data={'timeline_length': len(analytics.style_evolution_timeline)}
                )

    def _check_sustainability_milestone(self):
        """Check for sustainability milestones."""
        analytics = StyleAnalytics.objects.filter(user=self.user).first()
        if analytics and analytics.sustainability_score >= 0.8:
            if not StyleMilestone.objects.filter(
                user=self.user,
                milestone_type='sustainability_goal'
            ).exists():
                StyleMilestone.objects.create(
                    user=self.user,
                    milestone_type='sustainability_goal',
                    title='Sustainability Champion',
                    description='You have achieved an excellent sustainability score!',
                    achieved_at=datetime.now(),
                    data={'score': analytics.sustainability_score}
                )

    def _check_brand_diversity_milestone(self):
        """Check for brand diversity milestones."""
        analytics = StyleAnalytics.objects.filter(user=self.user).first()
        if analytics and len(analytics.top_brands) >= 10:
            if not StyleMilestone.objects.filter(
                user=self.user,
                milestone_type='brand_diversity'
            ).exists():
                StyleMilestone.objects.create(
                    user=self.user,
                    milestone_type='brand_diversity',
                    title='Brand Explorer',
                    description='You have explored a diverse range of brands!',
                    achieved_at=datetime.now(),
                    data={'brand_count': len(analytics.top_brands)}
                )

    def _check_color_mastery_milestone(self):
        """Check for color combination mastery."""
        analytics = StyleAnalytics.objects.filter(user=self.user).first()
        if analytics and len(analytics.favorite_color_combinations) >= 15:
            if not StyleMilestone.objects.filter(
                user=self.user,
                milestone_type='color_mastery'
            ).exists():
                StyleMilestone.objects.create(
                    user=self.user,
                    milestone_type='color_mastery',
                    title='Color Combination Master',
                    description='You have mastered the art of color combinations!',
                    achieved_at=datetime.now(),
                    data={'combination_count': len(analytics.favorite_color_combinations)}
                ) 