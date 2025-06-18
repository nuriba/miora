from celery import shared_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import time
import logging
from .models import Avatar, AvatarGenerationLog
from .services import AvatarGenerationService

logger = logging.getLogger('miora.avatars')


@shared_task(bind=True, max_retries=3)
def generate_avatar_from_photo(self, avatar_id, photo_data):
    """Generate 3D avatar from uploaded photo."""
    try:
        avatar = Avatar.objects.get(id=avatar_id)
        log = AvatarGenerationLog.objects.filter(
            avatar=avatar,
            generation_method='photo'
        ).latest('created_at')
        
        start_time = time.time()
        
        # Update log status
        log.status = 'processing'
        log.save()
        
        # Initialize service
        service = AvatarGenerationService()
        
        # Process photo and generate 3D model
        result = service.generate_from_photo(photo_data)
        
        if result['success']:
            # Save 3D model file
            model_path = f'avatars/{avatar.user.id}/{avatar.id}/model.glb'
            model_file = ContentFile(result['model_data'])
            avatar.model_file_url = default_storage.save(model_path, model_file)
            
            # Save thumbnail
            thumbnail_path = f'avatars/{avatar.user.id}/{avatar.id}/thumbnail.png'
            thumbnail_file = ContentFile(result['thumbnail_data'])
            avatar.thumbnail_url = default_storage.save(thumbnail_path, thumbnail_file)
            
            # Update measurements if detected
            if result.get('measurements'):
                for key, value in result['measurements'].items():
                    if hasattr(avatar, key):
                        setattr(avatar, key, value)
            
            avatar.save()
            
            # Update log
            processing_time = int((time.time() - start_time) * 1000)
            log.processing_time_ms = processing_time
            log.success = True
            log.metadata = result.get('metadata', {})
            log.save()
            
            logger.info(f'Avatar {avatar_id} generated successfully in {processing_time}ms')
            return {'success': True, 'avatar_id': str(avatar_id)}
        
        else:
            raise Exception(result.get('error', 'Avatar generation failed'))
            
    except Avatar.DoesNotExist:
        logger.error(f'Avatar {avatar_id} not found')
        return {'success': False, 'error': 'Avatar not found'}
        
    except Exception as e:
        logger.error(f'Avatar generation failed for {avatar_id}: {str(e)}')
        
        # Update log with error
        if 'log' in locals():
            log.success = False
            log.error_message = str(e)
            log.save()
        
        # Retry the task
        raise self.retry(exc=e, countdown=60)  # Retry after 1 minute


@shared_task
def update_avatar_measurements(avatar_id, measurements):
    """Update avatar measurements."""
    try:
        avatar = Avatar.objects.get(id=avatar_id)
        
        for key, value in measurements.items():
            if hasattr(avatar, key):
                setattr(avatar, key, value)
        
        avatar.save()
        
        logger.info(f'Avatar {avatar_id} measurements updated')
        return {'success': True}
        
    except Avatar.DoesNotExist:
        logger.error(f'Avatar {avatar_id} not found')
        return {'success': False, 'error': 'Avatar not found'}