"""Pydantic models and schemas for request/response validation."""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Health status of the service")
    version: str = Field(..., description="Application version")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }
    )


class ItemBase(BaseModel):
    """Base model for Item."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: Optional[str] = Field(None, max_length=500, description="Description of the item")
    price: float = Field(..., gt=0, description="Price of the item (must be positive)")
    tax: Optional[float] = Field(None, ge=0, description="Tax amount (must be non-negative)")


class ItemCreate(ItemBase):
    """Model for creating a new item."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Example Item",
                "description": "This is an example item",
                "price": 29.99,
                "tax": 2.99
            }
        }
    )


class ItemResponse(ItemBase):
    """Model for item response."""
    
    id: int = Field(..., description="Unique identifier for the item")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Example Item",
                "description": "This is an example item",
                "price": 29.99,
                "tax": 2.99
            }
        }
    )


class MessageResponse(BaseModel):
    """Generic message response model."""
    
    message: str = Field(..., description="Response message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    
    detail: str = Field(..., description="Error detail message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "An error occurred"
            }
        }
    )
