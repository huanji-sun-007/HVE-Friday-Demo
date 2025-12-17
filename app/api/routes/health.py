"""Health check endpoint."""

from fastapi import APIRouter, status

from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check the health status of the API server",
    tags=["System"]
)
async def health_check() -> HealthResponse:
    """Health check endpoint to verify the API is running.
    
    Returns:
        HealthResponse: Current health status and version information
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version
    )
