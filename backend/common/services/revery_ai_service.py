import os, requests

class ReveryAIService:
    def __init__(self):
        self.base = "https://api.revery.ai/v1"
        self.key  = os.getenv("REVERY_API_KEY")

    def try_on(self, model_img: str, garment_img: str, category: str):
        r = requests.post(
            f"{self.base}/try-on",
            headers={"Authorization": f"Bearer {self.key}"},
            json={
              "model_image": model_img,
              "garment_image": garment_img,
              "garment_category": category
            }, timeout=90
        )
        r.raise_for_status()
        return r.json() 