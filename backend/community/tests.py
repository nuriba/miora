from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import OutfitPost, StyleChallenge, ChallengeParticipation

User = get_user_model()

class CommunityModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_outfit_post_creation(self):
        post = OutfitPost.objects.create(
            user=self.user,
            caption='Test outfit post',
            hashtags=['#style', '#fashion']
        )
        self.assertEqual(post.caption, 'Test outfit post')
        self.assertEqual(post.hashtags, ['#style', '#fashion'])
        self.assertEqual(post.likes_count, 0)

    def test_style_challenge_creation(self):
        challenge = StyleChallenge.objects.create(
            title='Summer Style Challenge',
            description='Create the perfect summer outfit',
            theme='summer'
        )
        self.assertEqual(challenge.title, 'Summer Style Challenge')
        self.assertEqual(challenge.theme, 'summer')

class CommunityAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_outfit_post(self):
        data = {
            'caption': 'My new outfit!',
            'hashtags': ['#new', '#style'],
            'location': 'New York'
        }
        response = self.client.post('/api/v1/community/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
