class SizeRecommendationService:
    STANDARD = {'shirt': {'S': 90, 'M': 98, 'L': 106, 'XL': 114}}
    @classmethod
    def recommend(cls, chest_cm: float, garment='shirt'):
        chart = cls.STANDARD.get(garment, {})
        if not chart: return None
        return min(chart.items(), key=lambda kv: abs(kv[1]-chest_cm))[0] 