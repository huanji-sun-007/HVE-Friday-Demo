"""Dependency injection for FastAPI routes."""

from typing import Generator

from app.services.item_service import ItemService, item_service


def get_item_service() -> Generator[ItemService, None, None]:
    """Dependency to get the ItemService instance.
    
    This demonstrates dependency injection pattern in FastAPI.
    In a real application, this would manage database sessions,
    API clients, or other resources that need lifecycle management.
    
    Yields:
        ItemService: The service instance
    """
    yield item_service
