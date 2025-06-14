"""
Miora ML/CV Service
Python-based service for avatar generation, garment processing, and 3D operations

This service handles:
- Avatar generation from photos (AVR-01, AVR-02)
- Garment 3D reconstruction (GIC-01 to GIC-14)
- Size recommendation engine (SRE-01 to SRE-08)
- Cloth simulation support (VTO-01 to VTO-10)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.exceptions import MLServiceException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logging.info("Starting Miora ML Service...")
    
    # Initialize ML models (lazy loading for faster startup)
    logging.info("ML Service ready for processing")
    
    yield
    
    # Shutdown
    logging.info("Shutting down ML Service...")


def create_application() -> FastAPI:
    """Create and configure FastAPI ML service application"""
    
    app = FastAPI(
        title="Miora ML Service",
        description="Machine Learning and Computer Vision service for Miora platform",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # CORS middleware - restrictive in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["POST", "GET"],  # Limited methods for security
        allow_headers=["*"],
    )
    
    # Exception handlers
    @app.exception_handler(MLServiceException)
    async def ml_exception_handler(request, exc: MLServiceException):
        return {
            "error": exc.message,
            "details": exc.details,
            "status_code": exc.status_code
        }
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy", 
            "service": "miora-ml-service",
            "version": "1.0.0"
        }
    
    return app


# Create the application instance
app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    ) 