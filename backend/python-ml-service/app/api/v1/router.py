"""
Main API router for Miora ML Service
"""

from fastapi import APIRouter
from app.api.v1.endpoints import avatar, garment, size_recommendation

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    avatar.router,
    prefix="/avatar",
    tags=["avatar"]
)

api_router.include_router(
    garment.router,
    prefix="/garment",
    tags=["garment"]
)

api_router.include_router(
    size_recommendation.router,
    prefix="/size",
    tags=["size-recommendation"]
) 