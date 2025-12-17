"""Dependency injection for FastAPI routes."""

from app.services.item_service import ItemService, item_service


def get_item_service() -> ItemService:
    """Dependency to get the ItemService instance.
    
    This demonstrates dependency injection pattern in FastAPI.
    In a real application, this would manage database sessions,
    API clients, or other resources that need lifecycle management.
    
    Returns:
        ItemService: The service instance
    """
    return item_service
