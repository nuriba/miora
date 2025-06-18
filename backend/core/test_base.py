from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthenticatedAPITestCase(APITestCase):
    """Base test case with authentication helpers."""
    
    def setUp(self):
        """Set up test user and authentication."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.user.is_verified = True
        self.user.save()
        
        # Get tokens
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)
        
        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def create_user(self, email='another@example.com', password='pass123'):
        """Helper to create additional users."""
        user = User.objects.create_user(email=email, password=password)
        user.is_verified = True
        user.save()
        return user
    
    def authenticate_as(self, user):
        """Switch authentication to different user."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def logout(self):
        """Remove authentication."""
        self.client.credentials()