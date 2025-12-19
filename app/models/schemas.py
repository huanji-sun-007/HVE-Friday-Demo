"""
Pydantic models for request and response validation.

These models define the schema for API inputs and outputs,
providing automatic validation and documentation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ItemBase(BaseModel):
    """
    Base item schema with shared attributes.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    quantity: int = Field(default=0, ge=0, description="Item quantity in stock")
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        """Ensure name is not just whitespace."""
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()


class ItemCreate(ItemBase):
    """
    Schema for creating a new item.
    """
    pass


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing item.
    All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)


class ItemResponse(ItemBase):
    """
    Schema for item responses.
    Includes additional metadata fields.
    """
    id: int = Field(..., description="Unique item identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    """
    Schema for health check responses.
    """
    status: str = Field(..., description="Application status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(..., description="Current server timestamp")


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str = Field(..., description="Error detail message")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
