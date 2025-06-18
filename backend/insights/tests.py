from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import StyleAnalytics, WearEvent, StyleMilestone
from .services import StyleAnalyticsService, MilestoneService
from garments.models import Garment

User = get_user_model()

class StyleAnalyticsServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.service = StyleAnalyticsService(self.user)

    def test_analytics_creation(self):
        self.assertIsNotNone(self.service.analytics)
        self.assertEqual(self.service.analytics.user, self.user)

    def test_update_all_analytics(self):
        self.service.update_all_analytics()
        analytics = StyleAnalytics.objects.get(user=self.user)
        self.assertIsNotNone(analytics.last_updated)

class InsightsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_analytics(self):
        response = self.client.get('/api/v1/insights/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_analytics(self):
        response = self.client.post('/api/v1/insights/analytics/update/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_wear_event(self):
        garment = Garment.objects.create(
            user=self.user,
            name='Test Shirt',
            category='shirt'
        )
        data = {
            'garment': garment.id,
            'date_worn': '2024-01-01',
            'occasion': 'work',
            'rating': 5
        }
        response = self.client.post('/api/v1/insights/wear-events/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 