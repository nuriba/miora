import hashlib
import secrets
from typing import Dict, Any
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    """Hash a token using SHA256."""
    return hashlib.sha256(token.encode()).hexdigest()


def process_uploaded_image(image_file, max_size: tuple = (1920, 1920), 
                          quality: int = 85) -> ContentFile:
    """Process uploaded image - resize and optimize."""
    # Open image
    image = Image.open(image_file)
    
    # Convert RGBA to RGB if necessary
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    
    # Resize if too large
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save to bytes
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return ContentFile(output.read())


def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
    """Generate unique filename."""
    import uuid
    ext = original_filename.split('.')[-1] if '.' in original_filename else 'jpg'
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}{unique_id}.{ext}"


def calculate_file_hash(file_content: bytes) -> str:
    """Calculate SHA256 hash of file content."""
    return hashlib.sha256(file_content).hexdigest()


def validate_image_file(file) -> Dict[str, Any]:
    """Validate uploaded image file."""
    errors = []
    
    # Check file size (10MB max)
    if file.size > 10 * 1024 * 1024:
        errors.append('File size exceeds 10MB limit')
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp']
    if file.content_type not in allowed_types:
        errors.append(f'Invalid file type. Allowed: {", ".join(allowed_types)}')
    
    # Try to open as image
    try:
        image = Image.open(file)
        image.verify()
        
        # Check dimensions
        if image.width < 200 or image.height < 200:
            errors.append('Image dimensions must be at least 200x200 pixels')
        if image.width > 8000 or image.height > 8000:
            errors.append('Image dimensions must not exceed 8000x8000 pixels')
    except Exception:
        errors.append('Invalid image file')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


class S3Storage:
    """Utility class for S3 operations."""
    
    @staticmethod
    def upload_file(file_content: bytes, key: str, content_type: str = 'image/jpeg') -> str:
        """Upload file to S3."""
        from django.conf import settings
        import boto3
        
        if not settings.DEBUG:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key,
                Body=file_content,
                ContentType=content_type,
                CacheControl='max-age=86400'
            )
            
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}"
        else:
            # Local storage in development
            return default_storage.save(key, ContentFile(file_content))
    
    @staticmethod
    def delete_file(key: str) -> bool:
        """Delete file from S3."""
        from django.conf import settings
        import boto3
        
        try:
            if not settings.DEBUG:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                s3_client.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key
                )
            else:
                default_storage.delete(key)
            
            return True
        except Exception:
            return False