"""
Custom exceptions for Miora ML Service
"""

from typing import Optional


class MLServiceException(Exception):
    """Base exception for ML service operations"""
    
    def __init__(self, message: str, details: Optional[str] = None, status_code: int = 500):
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(self.message)


class AvatarProcessingException(MLServiceException):
    """Exception raised during avatar generation/processing"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, details, status_code=422)


class GarmentProcessingException(MLServiceException):
    """Exception raised during garment 3D reconstruction"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, details, status_code=422)


class InvalidImageException(MLServiceException):
    """Exception raised for invalid or corrupted images"""
    
    def __init__(self, message: str = "Invalid image format or corrupted file", details: Optional[str] = None):
        super().__init__(message, details, status_code=400)


class ProcessingTimeoutException(MLServiceException):
    """Exception raised when processing takes too long"""
    
    def __init__(self, message: str = "Processing timeout exceeded", details: Optional[str] = None):
        super().__init__(message, details, status_code=408)


class ModelNotLoadedException(MLServiceException):
    """Exception raised when ML model is not properly loaded"""
    
    def __init__(self, model_name: str, details: Optional[str] = None):
        message = f"Model '{model_name}' is not loaded or available"
        super().__init__(message, details, status_code=503)


class SizeRecommendationException(MLServiceException):
    """Exception raised during size recommendation processing"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, details, status_code=422) 