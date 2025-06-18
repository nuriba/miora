import os, io, requests

class RemoveBgService:
    URL = "https://api.remove.bg/v1.0/removebg"
    def __init__(self):
        self.key = os.getenv("REMOVE_BG_API_KEY")
    def remove(self, image_bytes: bytes) -> bytes:
        r = requests.post(
            self.URL,
            headers={"X-Api-Key": self.key},
            files={"image_file": ("img.jpg", io.BytesIO(image_bytes))},
            data={"size": "auto"}, timeout=30
        )
        r.raise_for_status()
        return r.content 