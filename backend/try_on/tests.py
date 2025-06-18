from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
import uuid

from avatars.models import Avatar
from garments.models import Garment
from .models import TryOnSession, TryOnSessionGarment, Outfit, OutfitGarment

User = get_user_model()


class TryOnModelsTest(TestCase):
    """Test try-on related models."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123!@#'
        )
        
        self.avatar = Avatar.objects.create(
            user=self.user,
            full_body_image_url='https://example.com/avatar.jpg',
            height=175.0,
            is_active=True
        )
        
        self.garment = Garment.objects.create(
            user=self.user,
            name='Test Shirt',
            category='shirt',
            original_image_url='https://example.com/shirt.jpg',
            cleaned_image_url='https://example.com/shirt_clean.jpg'
        )

    def test_try_on_session_creation(self):
        """Test creating a try-on session."""
        session = TryOnSession.objects.create(
            user=self.user,
            avatar=self.avatar,
            session_name='Test Session'
        )
        
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.avatar, self.avatar)
        self.assertEqual(session.session_name, 'Test Session')
        self.assertIsInstance(session.id, uuid.UUID)

    def test_try_on_session_garment_relationship(self):
        """Test try-on session to garment relationship."""
        session = TryOnSession.objects.create(
            user=self.user,
            avatar=self.avatar
        )
        
        session_garment = TryOnSessionGarment.objects.create(
            session=session,
            garment=self.garment,
            layer_order=1,
            selected_size='M'
        )
        
        self.assertEqual(session_garment.session, session)
        self.assertEqual(session_garment.garment, self.garment)
        self.assertEqual(session_garment.layer_order, 1)
        self.assertEqual(session_garment.selected_size, 'M')

    def test_outfit_creation(self):
        """Test creating an outfit."""
        outfit = Outfit.objects.create(
            user=self.user,
            avatar=self.avatar,
            name='Test Outfit',
            description='A test outfit',
            privacy_level='private',
            is_favorite=True
        )
        
        self.assertEqual(outfit.user, self.user)
        self.assertEqual(outfit.avatar, self.avatar)
        self.assertEqual(outfit.name, 'Test Outfit')
        self.assertEqual(outfit.description, 'A test outfit')
        self.assertEqual(outfit.privacy_level, 'private')
        self.assertTrue(outfit.is_favorite)

    def test_outfit_garment_relationship(self):
        """Test outfit to garment relationship."""
        outfit = Outfit.objects.create(
            user=self.user,
            avatar=self.avatar,
            name='Test Outfit'
        )
        
        outfit_garment = OutfitGarment.objects.create(
            outfit=outfit,
            garment=self.garment,
            layer_order=1,
            selected_size='L'
        )
        
        self.assertEqual(outfit_garment.outfit, outfit)
        self.assertEqual(outfit_garment.garment, self.garment)
        self.assertEqual(outfit_garment.layer_order, 1)
        self.assertEqual(outfit_garment.selected_size, 'L')


class TryOnSessionAPITest(APITestCase):
    """Test try-on session API endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123!@#'
        )
        
        self.avatar = Avatar.objects.create(
            user=self.user,
            full_body_image_url='https://example.com/avatar.jpg',
            height=175.0,
            is_active=True
        )
        
        self.garment = Garment.objects.create(
            user=self.user,
            name='Test Shirt',
            category='shirt',
            original_image_url='https://example.com/shirt.jpg'
        )
        
        self.client.force_authenticate(user=self.user)

    def test_list_try_on_sessions(self):
        """Test listing user's try-on sessions."""
        # Create a session
        session = TryOnSession.objects.create(
            user=self.user,
            avatar=self.avatar,
            session_name='Test Session'
        )
        
        url = reverse('try_on:tryon-session-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['session_name'], 'Test Session')

    @patch('try_on.services.VirtualTryOnService.simulate')
    @patch('recommendations.services.SizeRecommendationService.get_recommendation')
    def test_create_try_on_session(self, mock_size_rec, mock_vto):
        """Test creating a new try-on session."""
        # Mock services
        mock_vto.return_value = {'overall_fit_score': 0.85, 'confidence': 0.9}
        mock_size_rec.return_value = {'fit_score': 0.8, 'recommended_size': 'M'}
        
        url = reverse('try_on:tryon-session-list')
        data = {
            'avatar_id': str(self.avatar.id),
            'session_name': 'New Session',
            'garments': [
                {
                    'garment_id': str(self.garment.id),
                    'layer_order': 1,
                    'selected_size': 'M'
                }
            ]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check session was created
        session = TryOnSession.objects.get(id=response.data['id'])
        self.assertEqual(session.session_name, 'New Session')
        self.assertEqual(session.garments.count(), 1)

    def test_update_garment_size(self):
        """Test updating garment size in a session."""
        session = TryOnSession.objects.create(
            user=self.user,
            avatar=self.avatar,
            session_name='Test Session'
        )
        
        session_garment = TryOnSessionGarment.objects.create(
            session=session,
            garment=self.garment,
            layer_order=1,
            selected_size='M'
        )
        
        url = reverse('try_on:tryon-session-update-garment-size', kwargs={'pk': session.id})
        data = {
            'garment_id': str(self.garment.id),
            'size': 'L'
        }
        
        with patch('recommendations.services.SizeRecommendationService.calculate_fit_score') as mock_calc:
            mock_calc.return_value = 0.75
            response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check size was updated
        session_garment.refresh_from_db()
        self.assertEqual(session_garment.selected_size, 'L')

    def test_save_session_as_outfit(self):
        """Test saving a try-on session as an outfit."""
        session = TryOnSession.objects.create(
            user=self.user,
            avatar=self.avatar,
            session_name='Test Session'
        )
        
        TryOnSessionGarment.objects.create(
            session=session,
            garment=self.garment,
            layer_order=1,
            selected_size='M'
        )
        
        url = reverse('try_on:tryon-session-save-as-outfit', kwargs={'pk': session.id})
        data = {
            'name': 'Saved Outfit',
            'description': 'Outfit from session',
            'privacy_level': 'private',
            'is_favorite': True
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check outfit was created
        outfit = Outfit.objects.get(id=response.data['id'])
        self.assertEqual(outfit.name, 'Saved Outfit')
        self.assertEqual(outfit.garments.count(), 1)


class OutfitAPITest(APITestCase):
    """Test outfit API endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123!@#'
        )
        
        self.avatar = Avatar.objects.create(
            user=self.user,
            full_body_image_url='https://example.com/avatar.jpg',
            height=175.0,
            is_active=True
        )
        
        self.garment = Garment.objects.create(
            user=self.user,
            name='Test Shirt',
            category='shirt',
            original_image_url='https://example.com/shirt.jpg'
        )
        
        self.outfit = Outfit.objects.create(
            user=self.user,
            avatar=self.avatar,
            name='Test Outfit',
            privacy_level='private',
            is_favorite=False
        )
        
        self.client.force_authenticate(user=self.user)

    def test_list_outfits(self):
        """Test listing user's outfits."""
        url = reverse('try_on:outfit-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Outfit')

    def test_filter_outfits_by_privacy(self):
        """Test filtering outfits by privacy level."""
        # Create public outfit
        Outfit.objects.create(
            user=self.user,
            avatar=self.avatar,
            name='Public Outfit',
            privacy_level='public'
        )
        
        url = reverse('try_on:outfit-list')
        response = self.client.get(url, {'privacy': 'public'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['privacy_level'], 'public')

    def test_filter_favorite_outfits(self):
        """Test filtering favorite outfits."""
        # Make outfit favorite
        self.outfit.is_favorite = True
        self.outfit.save()
        
        url = reverse('try_on:outfit-list')
        response = self.client.get(url, {'favorites': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue(response.data['results'][0]['is_favorite'])

    def test_toggle_favorite_outfit(self):
        """Test toggling outfit favorite status."""
        url = reverse('try_on:outfit-toggle-favorite', kwargs={'pk': self.outfit.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_favorite'])
        
        # Check database
        self.outfit.refresh_from_db()
        self.assertTrue(self.outfit.is_favorite)

    def test_duplicate_outfit(self):
        """Test duplicating an outfit."""
        OutfitGarment.objects.create(
            outfit=self.outfit,
            garment=self.garment,
            layer_order=1,
            selected_size='M'
        )
        
        url = reverse('try_on:outfit-duplicate', kwargs={'pk': self.outfit.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check duplicate was created
        duplicate = Outfit.objects.get(id=response.data['id'])
        self.assertEqual(duplicate.name, f"{self.outfit.name} (Copy)")
        self.assertEqual(duplicate.garments.count(), 1)
        self.assertEqual(duplicate.privacy_level, 'private')
        self.assertFalse(duplicate.is_favorite)

    def test_create_try_on_from_outfit(self):
        """Test creating a try-on session from an outfit."""
        OutfitGarment.objects.create(
            outfit=self.outfit,
            garment=self.garment,
            layer_order=1,
            selected_size='M'
        )
        
        url = reverse('try_on:outfit-try-on', kwargs={'pk': self.outfit.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('session_id', response.data)
        
        # Check session was created
        session_id = response.data['session_id']
        session = TryOnSession.objects.get(id=session_id)
        self.assertEqual(session.avatar, self.outfit.avatar)
        self.assertEqual(session.garments.count(), 1)


class EnhancedTryOnAPITest(APITestCase):
    """Test enhanced try-on API with Flora Fauna and Revery AI."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123!@#'
        )
        
        self.avatar = Avatar.objects.create(
            user=self.user,
            full_body_image_url='https://example.com/avatar.jpg',
            height=175.0,
            is_active=True
        )
        
        self.garment = Garment.objects.create(
            user=self.user,
            name='Test Shirt',
            category='shirt',
            original_image_url='https://example.com/shirt.jpg',
            cleaned_image_url='https://example.com/shirt_clean.jpg'
        )
        
        self.client.force_authenticate(user=self.user)

    @patch('common.services.flora_fauna_service.FloraFaunaService.create_try_on')
    def test_enhanced_try_on_success(self, mock_flora):
        """Test successful enhanced try-on with Flora Fauna."""
        mock_flora.return_value = {'output_url': 'https://example.com/result.jpg'}
        
        url = reverse('try_on:enhanced_try_on')
        data = {
            'avatar_id': str(self.avatar.id),
            'garment_id': str(self.garment.id)
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image_url', response.data)
        self.assertEqual(response.data['image_url'], 'https://example.com/result.jpg')

    @patch('common.services.revery_ai_service.ReveryAIService.try_on')
    @patch('common.services.flora_fauna_service.FloraFaunaService.create_try_on')
    def test_enhanced_try_on_fallback(self, mock_flora, mock_revery):
        """Test enhanced try-on with fallback to Revery AI."""
        mock_flora.side_effect = Exception('Flora Fauna failed')
        mock_revery.return_value = {'result_url': 'https://example.com/revery_result.jpg'}
        
        url = reverse('try_on:enhanced_try_on')
        data = {
            'avatar_id': str(self.avatar.id),
            'garment_id': str(self.garment.id)
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image_url', response.data)
        self.assertEqual(response.data['image_url'], 'https://example.com/revery_result.jpg')

    @patch('common.services.revery_ai_service.ReveryAIService.try_on')
    @patch('common.services.flora_fauna_service.FloraFaunaService.create_try_on')
    def test_enhanced_try_on_both_fail(self, mock_flora, mock_revery):
        """Test enhanced try-on when both services fail."""
        mock_flora.side_effect = Exception('Flora Fauna failed')
        mock_revery.side_effect = Exception('Revery AI failed')
        
        url = reverse('try_on:enhanced_try_on')
        data = {
            'avatar_id': str(self.avatar.id),
            'garment_id': str(self.garment.id)
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    def test_enhanced_try_on_missing_params(self):
        """Test enhanced try-on with missing parameters."""
        url = reverse('try_on:enhanced_try_on')
        data = {'avatar_id': str(self.avatar.id)}  # Missing garment_id
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_enhanced_try_on_invalid_avatar(self):
        """Test enhanced try-on with invalid avatar ID."""
        url = reverse('try_on:enhanced_try_on')
        data = {
            'avatar_id': str(uuid.uuid4()),  # Non-existent avatar
            'garment_id': str(self.garment.id)
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_enhanced_try_on_unauthorized_avatar(self):
        """Test enhanced try-on with avatar belonging to another user."""
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='otherpass123!@#'
        )
        
        other_avatar = Avatar.objects.create(
            user=other_user,
            full_body_image_url='https://example.com/other_avatar.jpg',
            height=170.0,
            is_active=True
        )
        
        url = reverse('try_on:enhanced_try_on')
        data = {
            'avatar_id': str(other_avatar.id),
            'garment_id': str(self.garment.id)
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
