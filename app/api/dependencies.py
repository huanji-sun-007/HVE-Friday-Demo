"""
Dependency injection utilities.

This module provides common dependencies used across route handlers.
"""

from typing import Annotated
from fastapi import Depends

from app.services.item_service import ItemService


def get_item_service() -> ItemService:
    """
    Dependency for injecting ItemService.
    
    Returns:
        ItemService instance
    """
    return ItemService()


# Type alias for dependency injection
ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
