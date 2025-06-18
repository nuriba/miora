from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from avatars.models import Avatar
from garments.models import Garment

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users with sample data'
    
    def handle(self, *args, **options):
        # Create test users
        test_users = [
            {'email': 'test1@miora.com', 'password': 'testpass123'},
            {'email': 'test2@miora.com', 'password': 'testpass123'},
            {'email': 'demo@miora.com', 'password': 'demo123'},
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={'is_verified': True}
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.email}')
                )
                
                # Create avatar for the user
                avatar = Avatar.objects.create(
                    user=user,
                    name='Default Avatar',
                    is_active=True,
                    height=175,
                    chest=95,
                    waist=80,
                    hips=95
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created avatar for user: {user.email}')
                )
                
                # Create test garments for the user
                test_garments = [
                    {'name': 'Casual T-Shirt', 'category': 't-shirt', 'original_image_url': 'https://example.com/tshirt.jpg'},
                    {'name': 'Blue Jeans', 'category': 'jeans', 'original_image_url': 'https://example.com/jeans.jpg'},
                    {'name': 'Summer Dress', 'category': 'dress', 'original_image_url': 'https://example.com/dress.jpg'},
                ]
                
                for garment_data in test_garments:
                    Garment.objects.create(
                        user=user,
                        name=garment_data['name'],
                        category=garment_data['category'],
                        original_image_url=garment_data['original_image_url']
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created {garment_data["category"]} "{garment_data["name"]}" for user: {user.email}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user.email}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test users with avatars and garments')
        )