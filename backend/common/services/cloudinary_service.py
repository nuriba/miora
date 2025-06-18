import cloudinary.uploader

def upload_image(file_bytes: bytes, public_id: str) -> dict:
    return cloudinary.uploader.upload(
        file_bytes,
        public_id=public_id,
        folder="garments",
        overwrite=True,
        transformation=[
            {"width": 1000, "height": 1000, "crop": "pad"},
            {"quality": "auto", "fetch_format": "auto"},
        ],
    ) 