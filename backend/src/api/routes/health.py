"""
Health check routes
"""
from fastapi import APIRouter
from ..models.search_models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Hedwig paper search service is running"
    )


@router.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """Root endpoint"""
    return HealthResponse(
        status="healthy",
        message="Welcome to Hedwig - Research Paper Search API"
    )
