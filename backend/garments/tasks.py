from celery import shared_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import time
import logging
from PIL import Image
import io
from .models import Garment, GarmentProcessingLog
from .services import GarmentProcessingService

logger = logging.getLogger('miora.garments')


@shared_task(bind=True, max_retries=3)
def process_garment_image(self, garment_id, image_data=None):
    """Process garment image and generate 3D model."""
    try:
        garment = Garment.objects.get(id=garment_id)
        
        # Create processing log
        log = GarmentProcessingLog.objects.create(
            garment=garment,
            processing_step='image_processing',
            status='started'
        )
        
        start_time = time.time()
        
        # Update garment status
        garment.processing_status = 'processing'
        garment.save()
        
        # Initialize service
        service = GarmentProcessingService()
        
        # Load image
        if image_data:
            image = Image.open(io.BytesIO(image_data))
        else:
            # Load from existing URL
            image_file = default_storage.open(garment.original_image_url)
            image = Image.open(image_file)
        
        # Process image
        processed_result = service.process_image(image)
        
        if processed_result['success']:
            # Save processed image
            processed_path = f'garments/{garment.user.id}/{garment.id}/processed.jpg'
            processed_file = ContentFile(processed_result['processed_image'])
            garment.original_image_url = default_storage.save(processed_path, processed_file)
            
            # Generate thumbnail
            thumbnail_path = f'garments/{garment.user.id}/{garment.id}/thumbnail.jpg'
            thumbnail_file = ContentFile(processed_result['thumbnail'])
            garment.thumbnail_url = default_storage.save(thumbnail_path, thumbnail_file)
            
            # Extract metadata
            if processed_result.get('metadata'):
                garment.color = processed_result['metadata'].get('dominant_color', '')
                garment.pattern = processed_result['metadata'].get('pattern', '')
            
            garment.save()
            
            # Update log
            processing_time = int((time.time() - start_time) * 1000)
            log.processing_time_ms = processing_time
            log.status = 'completed'
            log.save()
            
            # Queue 3D generation
            generate_garment_3d_model.delay(garment_id)
            
            logger.info(f'Garment {garment_id} image processed in {processing_time}ms')
            return {'success': True, 'garment_id': str(garment_id)}
            
        else:
            raise Exception(processed_result.get('error', 'Image processing failed'))
            
    except Garment.DoesNotExist:
        logger.error(f'Garment {garment_id} not found')
        return {'success': False, 'error': 'Garment not found'}
        
    except Exception as e:
        logger.error(f'Garment processing failed for {garment_id}: {str(e)}')
        
        # Update status
        if 'garment' in locals():
            garment.processing_status = 'failed'
            garment.save()
        
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = str(e)
            log.save()
        
        # Retry the task
        raise self.retry(exc=e, countdown=120)  # Retry after 2 minutes


@shared_task(bind=True, max_retries=3)
def generate_garment_3d_model(self, garment_id):
    """Generate 3D model from processed garment image."""
    try:
        garment = Garment.objects.get(id=garment_id)
        
        # Create processing log
        log = GarmentProcessingLog.objects.create(
            garment=garment,
            processing_step='3d_generation',
            status='started'
        )
        
        start_time = time.time()
        
        # Initialize service
        service = GarmentProcessingService()
        
        # Load processed image
        image_file = default_storage.open(garment.original_image_url)
        image = Image.open(image_file)
        
        # Generate 3D model
        result = service.generate_3d_model(
            image,
            category=garment.category,
            metadata={
                'brand': garment.brand,
                'size_chart': garment.size_chart
            }
        )
        
        if result['success']:
            # Save 3D model
            model_path = f'garments/{garment.user.id}/{garment.id}/model.glb'
            model_file = ContentFile(result['model_data'])
            garment.model_3d_url = default_storage.save(model_path, model_file)
            
            # Save textures
            texture_urls = []
            for idx, texture_data in enumerate(result.get('textures', [])):
                texture_path = f'garments/{garment.user.id}/{garment.id}/texture_{idx}.png'
                texture_file = ContentFile(texture_data)
                texture_url = default_storage.save(texture_path, texture_file)
                texture_urls.append(texture_url)
            
            garment.texture_urls = texture_urls
            
            # Update material properties
            garment.material_properties = result.get('material_properties', {})
            
            # Mark as completed
            garment.processing_status = 'completed'
            garment.save()
            
            # Update log
            processing_time = int((time.time() - start_time) * 1000)
            log.processing_time_ms = processing_time
            log.status = 'completed'
            log.metadata = {'vertices': result.get('vertex_count', 0)}
            log.save()
            
            # Create validation log
            validate_garment_model.delay(garment_id)
            
            logger.info(f'3D model generated for garment {garment_id} in {processing_time}ms')
            return {'success': True, 'garment_id': str(garment_id)}
            
        else:
            raise Exception(result.get('error', '3D generation failed'))
            
    except Garment.DoesNotExist:
        logger.error(f'Garment {garment_id} not found')
        return {'success': False, 'error': 'Garment not found'}
        
    except Exception as e:
        logger.error(f'3D generation failed for garment {garment_id}: {str(e)}')
        
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = str(e)
            log.save()
        
        # Don't update garment status to failed yet, let retry handle it
        raise self.retry(exc=e, countdown=300)  # Retry after 5 minutes


@shared_task
def validate_garment_model(garment_id):
    """Validate generated 3D model."""
    try:
        garment = Garment.objects.get(id=garment_id)
        
        # Create validation log
        log = GarmentProcessingLog.objects.create(
            garment=garment,
            processing_step='validation',
            status='started'
        )
        
        # Initialize service
        service = GarmentProcessingService()
        
        # Validate model
        validation_result = service.validate_model(garment.model_3d_url)
        
        if validation_result['valid']:
            log.status = 'completed'
            log.metadata = validation_result.get('details', {})
        else:
            log.status = 'failed'
            log.error_message = validation_result.get('errors', [])
            
            # Mark garment for review
            garment.processing_status = 'needs_review'
            garment.save()
        
        log.save()
        
        logger.info(f'Validation completed for garment {garment_id}')
        return {'success': True, 'valid': validation_result['valid']}
        
    except Garment.DoesNotExist:
        logger.error(f'Garment {garment_id} not found')
        return {'success': False, 'error': 'Garment not found'}