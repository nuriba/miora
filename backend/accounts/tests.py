from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
import json

User = get_user_model()


class UserModelTest(TestCase):
    """Test the enhanced User model."""
    
    def test_create_user_with_username(self):
        """Test creating a user with username."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123!@#'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123!@#'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123!@#'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.check_password('adminpass123!@#'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_username_validator(self):
        """Test username validation."""
        # Valid usernames
        valid_usernames = ['user123', 'test_user', 'user.name', 'user+tag', 'user@domain']
        for username in valid_usernames:
            user = User(email='test@example.com', username=username)
            user.full_clean()  # Should not raise ValidationError

    def test_user_string_representation(self):
        """Test string representation of user."""
        user = User(email='test@example.com', username='testuser')
        self.assertEqual(str(user), 'test@example.com')

    def test_additional_fields(self):
        """Test additional user profile fields."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123!@#',
            first_name='John',
            last_name='Doe',
            display_name='Johnny',
            date_of_birth=date(1990, 1, 1),
            gender='male',
            phone_number='+1234567890',
            country='US',
            city='New York',
            timezone='America/New_York'
        )
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.display_name, 'Johnny')
        self.assertEqual(user.date_of_birth, date(1990, 1, 1))
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertEqual(user.country, 'US')
        self.assertEqual(user.city, 'New York')
        self.assertEqual(user.timezone, 'America/New_York')


class UserRegistrationAPITest(APITestCase):
    """Test user registration API."""

    def test_successful_registration(self):
        """Test successful user registration."""
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPass123!@#',
            'password_confirm': 'NewPass123!@#',
            'first_name': 'New',
            'last_name': 'User',
            'date_of_birth': '1995-05-15',
            'terms_accepted': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check user was created
        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.date_of_birth, date(1995, 5, 15))

    def test_registration_password_mismatch(self):
        """Test registration with password mismatch."""
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPass123!@#',
            'password_confirm': 'DifferentPass123!@#',
            'terms_accepted': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_weak_password(self):
        """Test registration with weak password."""
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'weak',  # Too weak
            'password_confirm': 'weak',
            'terms_accepted': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_underage_user(self):
        """Test registration with underage user."""
        url = reverse('accounts:register')
        data = {
            'email': 'child@example.com',
            'username': 'child',
            'password': 'ChildPass123!@#',
            'password_confirm': 'ChildPass123!@#',
            'date_of_birth': (date.today() - timedelta(days=365*10)).isoformat(),  # 10 years old
            'terms_accepted': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_of_birth', response.data)

    def test_registration_without_terms(self):
        """Test registration without accepting terms."""
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPass123!@#',
            'password_confirm': 'NewPass123!@#',
            'terms_accepted': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('terms_accepted', response.data)

    def test_duplicate_email_registration(self):
        """Test registration with duplicate email."""
        # Create initial user
        User.objects.create_user(
            email='existing@example.com',
            username='existing',
            password='ExistingPass123!@#'
        )
        
        url = reverse('accounts:register')
        data = {
            'email': 'existing@example.com',  # Duplicate email
            'username': 'newuser',
            'password': 'NewPass123!@#',
            'password_confirm': 'NewPass123!@#',
            'terms_accepted': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_registration(self):
        """Test registration with duplicate username."""
        # Create initial user
        User.objects.create_user(
            email='existing@example.com',
            username='existing',
            password='ExistingPass123!@#'
        )
        
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'existing',  # Duplicate username
            'password': 'NewPass123!@#',
            'password_confirm': 'NewPass123!@#',
            'terms_accepted': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UsernameCheckAPITest(APITestCase):
    """Test username availability checking."""

    def setUp(self):
        User.objects.create_user(
            email='existing@example.com',
            username='existing',
            password='ExistingPass123!@#'
        )

    def test_available_username(self):
        """Test checking available username."""
        url = reverse('accounts:check_username')
        response = self.client.get(url, {'username': 'available'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

    def test_taken_username(self):
        """Test checking taken username."""
        url = reverse('accounts:check_username')
        response = self.client.get(url, {'username': 'existing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_case_insensitive_username_check(self):
        """Test that username check is case insensitive."""
        url = reverse('accounts:check_username')
        response = self.client.get(url, {'username': 'EXISTING'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_username_check_without_parameter(self):
        """Test username check without username parameter."""
        url = reverse('accounts:check_username')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class CustomPasswordValidatorTest(TestCase):
    """Test custom password validator."""

    def setUp(self):
        from accounts.validators import CustomPasswordValidator
        self.validator = CustomPasswordValidator()

    def test_valid_password(self):
        """Test valid password passes validation."""
        valid_password = 'ValidPass123!@#'
        try:
            self.validator.validate(valid_password)
        except ValidationError:
            self.fail("Valid password should not raise ValidationError")

    def test_short_password(self):
        """Test short password fails validation."""
        short_password = 'Short1!'
        with self.assertRaises(ValidationError):
            self.validator.validate(short_password)

    def test_password_without_uppercase(self):
        """Test password without uppercase fails validation."""
        password = 'nouppercasepass123!@#'
        with self.assertRaises(ValidationError):
            self.validator.validate(password)

    def test_password_without_lowercase(self):
        """Test password without lowercase fails validation."""
        password = 'NOLOWERCASEPASS123!@#'
        with self.assertRaises(ValidationError):
            self.validator.validate(password)

    def test_password_without_digit(self):
        """Test password without digit fails validation."""
        password = 'NoDigitsPass!@#'
        with self.assertRaises(ValidationError):
            self.validator.validate(password)

    def test_password_without_special_char(self):
        """Test password without special character fails validation."""
        password = 'NoSpecialChar123'
        with self.assertRaises(ValidationError):
            self.validator.validate(password)

    def test_validator_help_text(self):
        """Test validator help text."""
        help_text = self.validator.get_help_text()
        self.assertIn('Password', help_text)
        self.assertIn('8', help_text)


class UserAuthenticationTest(APITestCase):
    """Test user authentication with enhanced user model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='TestPass123!@#'
        )

    def test_login_with_email(self):
        """Test login using email."""
        url = reverse('accounts:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPass123!@#'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        url = reverse('accounts:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_access(self):
        """Test accessing user profile endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('accounts:user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_profile_update(self):
        """Test updating user profile."""
        self.client.force_authenticate(user=self.user)
        url = reverse('accounts:user_profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'display_name': 'Updated Display',
            'city': 'Updated City'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.display_name, 'Updated Display')
        self.assertEqual(self.user.city, 'Updated City')
