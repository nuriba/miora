from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
import hashlib

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)
from .models import PasswordResetToken

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view with additional user data."""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        # Send verification email (in production)
        # self.send_verification_email(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_email(self, user):
        """Send email verification link."""
        # Implementation for email verification
        pass


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """Change password for authenticated user."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'detail': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    """Request password reset."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate reset token
        token = get_random_string(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        # Save token
        PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        
        # Send email (console in development)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        send_mail(
            'Password Reset Request',
            f'Click here to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return Response({
            'detail': 'Password reset email sent.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """Confirm password reset with token."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token_hash=token_hash,
                used=False,
                expires_at__gt=timezone.now()
            )
        except PasswordResetToken.DoesNotExist:
            return Response({
                'detail': 'Invalid or expired token.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset password
        user = reset_token.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Mark token as used
        reset_token.used = True
        reset_token.save()
        
        return Response({
            'detail': 'Password reset successfully.'
        }, status=status.HTTP_200_OK)


class CheckUsernameView(APIView):
    """Check if username is available."""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        username = request.query_params.get('username', '').lower()
        if not username:
            return Response({'error': 'Username parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        available = not User.objects.filter(username=username).exists()
        return Response({'available': available})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout user by blacklisting refresh token."""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'detail': 'Successfully logged out.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'detail': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)