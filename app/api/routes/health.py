"""
Health check endpoints.

Provides simple health check endpoints for monitoring and load balancers.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the application",
)
async def health_check() -> HealthResponse:
    """
    Check application health.
    
    Returns:
        Health status information
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=datetime.now(timezone.utc)
    )


@router.get(
    "/",
    summary="Root endpoint",
    description="Welcome endpoint with basic application information",
)
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message and basic info
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }
