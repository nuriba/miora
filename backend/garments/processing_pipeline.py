from common.services.remove_bg_service import RemoveBgService
from common.services.cloudinary_service import upload_image
from common.services.huggingface_fashion_service import FashionInsightsService

class GarmentProcessingPipeline:
    def __init__(self):
        self._bg = RemoveBgService()
        self._hf = FashionInsightsService()

    def process(self, garment):
        original = garment.file.read()
        bg_removed = self._bg.remove(original)
        cdn_resp   = upload_image(bg_removed, public_id=str(garment.id))
        garment.cleaned_image_url = cdn_resp["secure_url"]

        preds = self._hf.detect(garment.cleaned_image_url)
        garment.features = preds  # JSONField
        garment.save(update_fields=['cleaned_image_url','features']) 