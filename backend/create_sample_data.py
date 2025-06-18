import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from avatars.models import Avatar
from garments.models import Garment, BrandSizeChart

User = get_user_model()

print("Creating sample data...")

# Create a test user
try:
    user = User.objects.create_user(
        email='demo@miora.com',
        password='demo123'
    )
    print(f"✓ Created user: {user.email}")
except:
    user = User.objects.get(email='demo@miora.com')
    print(f"✓ User already exists: {user.email}")

# Create an avatar
avatar, created = Avatar.objects.get_or_create(
    user=user,
    name="Demo Avatar",
    defaults={
        'is_active': True,
        'height': 175,
        'weight': 70,
        'chest': 95,
        'waist': 80,
        'hips': 95,
        'body_type': 'average'
    }
)
print(f"✓ {'Created' if created else 'Found'} avatar: {avatar.name}")

# Create sample garments
garments_data = [
    {
        'name': "Classic White Shirt",
        'brand': "MioraStyle",
        'category': "shirt",
        'color': "white",
        'price': 79.99
    },
    {
        'name': "Slim Fit Jeans",
        'brand': "MioraStyle", 
        'category': "jeans",
        'color': "blue",
        'price': 99.99
    },
    {
        'name': "Summer Dress",
        'brand': "MioraStyle",
        'category': "dress", 
        'color': "floral",
        'price': 119.99
    }
]

for garment_data in garments_data:
    garment, created = Garment.objects.get_or_create(
        user=user,
        name=garment_data['name'],
        defaults={
            'brand': garment_data['brand'],
            'category': garment_data['category'],
            'gender': 'unisex',
            'original_image_url': f"https://example.com/{garment_data['category']}.jpg",
            'price': garment_data['price'],
            'color': garment_data['color'],
            'processing_status': 'completed'
        }
    )
    print(f"✓ {'Created' if created else 'Found'} garment: {garment.name}")

print("\n✅ Sample data created successfully!")
print("\nYou can log in with:")
print("  Demo User: demo@miora.com / demo123") 