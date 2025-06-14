"""
Avatar processing endpoints
Handles avatar generation, measurement extraction, and 3D model creation
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from app.services.avatar_service import AvatarService
from app.core.exceptions import AvatarProcessingException, InvalidImageException

router = APIRouter()
logger = logging.getLogger(__name__)


class AvatarGenerationRequest(BaseModel):
    """Request model for avatar generation"""
    user_id: int
    avatar_name: str
    generation_method: str  # 'selfie', 'multi_angle', 'manual_entry'
    measurements: Optional[Dict[str, float]] = None  # Manual measurements if provided


class AvatarGenerationResponse(BaseModel):
    """Response model for avatar generation"""
    processing_id: str
    status: str
    message: str
    estimated_completion_time: Optional[int] = None  # seconds


class AvatarStatusResponse(BaseModel):
    """Response model for avatar processing status"""
    processing_id: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    progress: int  # 0-100
    message: str
    result: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None


@router.post("/generate", response_model=AvatarGenerationResponse)
async def generate_avatar(
    background_tasks: BackgroundTasks,
    request: AvatarGenerationRequest,
    image: Optional[UploadFile] = File(None)
):
    """
    Generate 3D avatar from photo or manual measurements
    
    Supports requirements:
    - AVR-01: Auto-generate avatar from selfie/scan
    - AVR-02: Detect facial landmarks, output SMPL-X mesh
    - AVR-03: Manual entry of measurements
    - AVR-04: Live preview refresh ≤100ms, ≥30fps
    """
    try:
        avatar_service = AvatarService()
        
        # Validate request
        if request.generation_method in ['selfie', 'multi_angle'] and not image:
            raise HTTPException(
                status_code=400,
                detail="Image file is required for photo-based avatar generation"
            )
        
        if request.generation_method == 'manual_entry' and not request.measurements:
            raise HTTPException(
                status_code=400,
                detail="Measurements are required for manual avatar generation"
            )
        
        # Start avatar generation process
        processing_result = await avatar_service.start_avatar_generation(
            user_id=request.user_id,
            avatar_name=request.avatar_name,
            generation_method=request.generation_method,
            image_file=image,
            measurements=request.measurements,
            background_tasks=background_tasks
        )
        
        return AvatarGenerationResponse(
            processing_id=processing_result["processing_id"],
            status="started",
            message="Avatar generation started successfully",
            estimated_completion_time=processing_result.get("estimated_time", 30)
        )
        
    except InvalidImageException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except AvatarProcessingException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error in avatar generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status/{processing_id}", response_model=AvatarStatusResponse)
async def get_avatar_status(processing_id: str):
    """
    Get the status of avatar generation process
    
    Supports real-time status updates for AVR-04 requirement
    """
    try:
        avatar_service = AvatarService()
        status_info = await avatar_service.get_processing_status(processing_id)
        
        return AvatarStatusResponse(
            processing_id=processing_id,
            status=status_info["status"],
            progress=status_info["progress"],
            message=status_info["message"],
            result=status_info.get("result"),
            error_details=status_info.get("error_details")
        )
        
    except Exception as e:
        logger.error(f"Error getting avatar status: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve status")


@router.post("/extract-measurements")
async def extract_measurements_from_image(image: UploadFile = File(...)):
    """
    Extract body measurements from uploaded image
    
    Supports requirement AVR-11: Auto measures within ±5cm of manual baseline
    """
    try:
        avatar_service = AvatarService()
        measurements = await avatar_service.extract_measurements(image)
        
        return {
            "measurements": measurements,
            "confidence_scores": measurements.get("confidence", {}),
            "accuracy_estimate": "±5cm"
        }
        
    except InvalidImageException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error extracting measurements: {str(e)}")
        raise HTTPException(status_code=500, detail="Measurement extraction failed")


@router.post("/validate-measurements")
async def validate_measurements(measurements: Dict[str, float]):
    """
    Validate body measurements for consistency
    
    Supports requirement AVR-05: Flag improbable ratios
    """
    try:
        avatar_service = AvatarService()
        validation_result = await avatar_service.validate_measurements(measurements)
        
        return {
            "is_valid": validation_result["is_valid"],
            "warnings": validation_result.get("warnings", []),
            "suggestions": validation_result.get("suggestions", []),
            "corrected_measurements": validation_result.get("corrected_measurements")
        }
        
    except Exception as e:
        logger.error(f"Error validating measurements: {str(e)}")
        raise HTTPException(status_code=500, detail="Validation failed") 