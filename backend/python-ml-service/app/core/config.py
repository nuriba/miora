"""
Configuration settings for Miora ML Service
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SERVICE_NAME: str = "miora-ml-service"
    VERSION: str = "1.0.0"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8080",  # Spring Boot backend
        "http://localhost:3000",  # Frontend dev
        "http://localhost:5173",  # Vite dev server
    ]
    
    # File storage settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/tmp/miora/uploads")
    AVATAR_OUTPUT_DIR: str = os.getenv("AVATAR_OUTPUT_DIR", "/tmp/miora/avatars")
    GARMENT_OUTPUT_DIR: str = os.getenv("GARMENT_OUTPUT_DIR", "/tmp/miora/garments")
    
    # Processing limits
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_DIMENSION: int = 2048
    PROCESSING_TIMEOUT: int = 300  # 5 minutes
    
    # Avatar generation settings
    AVATAR_MESH_QUALITY: str = os.getenv("AVATAR_MESH_QUALITY", "medium")  # low, medium, high
    TARGET_MESH_VERTICES: int = 40000  # As per GIC-04 requirement
    
    # ML Model settings
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "/tmp/miora/models")
    USE_GPU: bool = os.getenv("USE_GPU", "True").lower() == "true"
    
    # Background processing
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Communication with Spring Boot backend
    SPRING_BOOT_BASE_URL: str = os.getenv("SPRING_BOOT_BASE_URL", "http://localhost:8080")
    SPRING_BOOT_API_KEY: str = os.getenv("SPRING_BOOT_API_KEY", "")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Size recommendation settings
    SIZE_CHART_CACHE_TTL: int = 3600  # 1 hour cache for size charts
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings() 