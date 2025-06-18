import os, requests, logging
logger = logging.getLogger(__name__)

class AvaturnService:
    BASE = "https://api.avaturn.me/v1"
    def __init__(self):
        self.key = os.getenv("AVATURN_API_KEY")

    def adjust_body(self, rpm_avatar_url: str, measurements: dict):
        r = requests.post(
            f"{self.BASE}/avatars",
            headers={"Authorization": f"Bearer {self.key}"},
            json={"url": rpm_avatar_url, **measurements},
            timeout=60,
        )
        r.raise_for_status()
        return r.json() 