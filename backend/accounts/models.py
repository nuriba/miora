import uuid, re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Username may contain letters, numbers and @/./+/-/_ only.'
)

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra):
        if not email:
            raise ValueError('Email required')
        if not username:
            raise ValueError('Username required')
        email = self.normalize_email(email)
        username = username.lower()

        user = self.model(email=email, username=username, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email        = models.EmailField(unique=True, max_length=255)
    username     = models.CharField(max_length=30, unique=True, validators=[username_validator])

    first_name   = models.CharField(max_length=50, blank=True)
    last_name    = models.CharField(max_length=50, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    date_of_birth= models.DateField(null=True, blank=True)
    gender       = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country      = models.CharField(max_length=2, blank=True)
    city         = models.CharField(max_length=100, blank=True)
    timezone     = models.CharField(max_length=50, default='UTC')

    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_verified  = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    # Legacy fields for backward compatibility
    last_login = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    objects      = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class OAuthAccount(models.Model):
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('apple', 'Apple'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oauth_accounts')
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    provider_account_id = models.CharField(max_length=255)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'oauth_accounts'
        unique_together = ['provider', 'provider_account_id']


class RevokedToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jti = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    revoked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'revoked_tokens'


class PasswordResetToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'password_reset_tokens'