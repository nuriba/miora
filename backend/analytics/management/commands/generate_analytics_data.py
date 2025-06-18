from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from analytics.models import SizeAnalytics


class Command(BaseCommand):
    help = 'Generate sample analytics data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of data to generate'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        brands = ['MioraStyle', 'FashionBrand', 'TrendyWear', 'ClassicFit']
        categories = ['shirt', 'pants', 'dress', 'jacket', 'jeans']
        sizes = ['S', 'M', 'L', 'XL']
        
        # Generate data for each day
        for day in range(days):
            date = timezone.now() - timedelta(days=day)
            
            # Generate 10-50 entries per day
            for _ in range(random.randint(10, 50)):
                SizeAnalytics.objects.create(
                    brand=random.choice(brands),
                    garment_category=random.choice(categories),
                    recommended_size=random.choice(sizes),
                    actual_size=random.choice(sizes) if random.random() > 0.3 else None,
                    fit_score=random.uniform(70, 95),
                    return_reported=random.random() < 0.1,  # 10% return rate
                    height_range=f"{random.choice([160, 170, 180])}-{random.choice([170, 180, 190])}",
                    weight_range=f"{random.choice([60, 70, 80])}-{random.choice([70, 80, 90])}",
                    body_type=random.choice(['athletic', 'average', 'slim']),
                    created_at=date
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Generated analytics data for {days} days')
        )