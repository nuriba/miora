import os
from transformers import pipeline

class FashionInsightsService:
    def __init__(self):
        self.token = os.getenv("HUGGINGFACE_TOKEN") or None
        self.classifier = pipeline("image-classification",
                                   model="valentinafeve/yolos-fashionpedia",
                                   token=self.token)

    def detect(self, img_path: str):
        return self.classifier(img_path) 