"""Example service layer with business logic."""

from typing import List, Optional

from app.models.schemas import ItemCreate, ItemResponse


class ItemService:
    """Service layer for Item operations.
    
    This demonstrates the separation of business logic from route handlers.
    In a real application, this would interact with a database or external services.
    """
    
    def __init__(self):
        """Initialize the service with in-memory storage."""
        self._items: List[ItemResponse] = []
        self._next_id: int = 1
    
    async def create_item(self, item: ItemCreate) -> ItemResponse:
        """Create a new item.
        
        Args:
            item: The item data to create
            
        Returns:
            ItemResponse: The created item with assigned ID
        """
        new_item = ItemResponse(
            id=self._next_id,
            name=item.name,
            description=item.description,
            price=item.price,
            tax=item.tax
        )
        self._items.append(new_item)
        self._next_id += 1
        return new_item
    
    async def get_item(self, item_id: int) -> Optional[ItemResponse]:
        """Get an item by ID.
        
        Args:
            item_id: The ID of the item to retrieve
            
        Returns:
            Optional[ItemResponse]: The item if found, None otherwise
        """
        for item in self._items:
            if item.id == item_id:
                return item
        return None
    
    async def get_all_items(self, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
        """Get all items with pagination.
        
        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List[ItemResponse]: List of items
        """
        return self._items[skip : skip + limit]
    
    async def update_item(self, item_id: int, item_data: ItemCreate) -> Optional[ItemResponse]:
        """Update an existing item.
        
        Args:
            item_id: The ID of the item to update
            item_data: The new item data
            
        Returns:
            Optional[ItemResponse]: The updated item if found, None otherwise
        """
        for idx, item in enumerate(self._items):
            if item.id == item_id:
                updated_item = ItemResponse(
                    id=item_id,
                    name=item_data.name,
                    description=item_data.description,
                    price=item_data.price,
                    tax=item_data.tax
                )
                self._items[idx] = updated_item
                return updated_item
        return None
    
    async def delete_item(self, item_id: int) -> bool:
        """Delete an item by ID.
        
        Args:
            item_id: The ID of the item to delete
            
        Returns:
            bool: True if item was deleted, False if not found
        """
        for idx, item in enumerate(self._items):
            if item.id == item_id:
                self._items.pop(idx)
                return True
        return False


# Global service instance
item_service = ItemService()
