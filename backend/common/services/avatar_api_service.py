from .avaturn_service import AvaturnService

class AvatarAPIService:
    def __init__(self):
        self.avaturn = AvaturnService()

    def create_from_photo(self, rpm_avatar_url: str, measurements: dict):
        return self.avaturn.adjust_body(rpm_avatar_url, measurements) 