import os, requests

class FloraFaunaService:
    def __init__(self):
        self.base = "https://api.flora-fauna.ai/v1"
        self.key = os.getenv("FLORA_FAUNA_API_KEY")

    def create_try_on(self, model_image: str, garment_image: str, garment_type: str):
        r = requests.post(
            f"{self.base}/try-on",
            headers={"Authorization": f"Bearer {self.key}"},
            json={
                "model_image": model_image,
                "garment_image": garment_image,
                "garment_type": garment_type
            }, 
            timeout=120
        )
        r.raise_for_status()
        return r.json() 