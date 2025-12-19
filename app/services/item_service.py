"""
Item service containing business logic for item operations.

This module separates business logic from route handlers,
making the code more maintainable and testable.
"""

from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.schemas import ItemCreate, ItemUpdate, ItemResponse


# In-memory storage for demonstration purposes
# In production, replace with actual database operations
_items_db: dict[int, dict] = {}
_next_id: int = 1


class ItemService:
    """
    Service class for item-related operations.
    """
    
    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """
        Create a new item.
        
        Args:
            item_data: Item creation data
            
        Returns:
            Created item with metadata
        """
        global _next_id
        
        item_id = _next_id
        _next_id += 1
        
        now = datetime.now(timezone.utc)
        item_dict = {
            "id": item_id,
            "name": item_data.name,
            "description": item_data.description,
            "price": item_data.price,
            "quantity": item_data.quantity,
            "created_at": now,
            "updated_at": now,
        }
        
        _items_db[item_id] = item_dict
        return ItemResponse(**item_dict)
    
    async def get_item(self, item_id: int) -> ItemResponse:
        """
        Retrieve an item by ID.
        
        Args:
            item_id: Item identifier
            
        Returns:
            Item data
            
        Raises:
            HTTPException: If item not found
        """
        if item_id not in _items_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        
        return ItemResponse(**_items_db[item_id])
    
    async def get_items(
        self, 
        skip: int = 0, 
        limit: int = 100,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[ItemResponse]:
        """
        Retrieve multiple items with optional filtering.
        
        Args:
            skip: Number of items to skip (pagination)
            limit: Maximum number of items to return
            min_price: Filter items with price >= min_price
            max_price: Filter items with price <= max_price
            
        Returns:
            List of items
        """
        items = list(_items_db.values())
        
        # Apply price filters
        if min_price is not None:
            items = [item for item in items if item["price"] >= min_price]
        if max_price is not None:
            items = [item for item in items if item["price"] <= max_price]
        
        # Sort by ID for consistent ordering
        items.sort(key=lambda x: x["id"])
        
        # Apply pagination
        paginated_items = items[skip : skip + limit]
        
        return [ItemResponse(**item) for item in paginated_items]
    
    async def update_item(self, item_id: int, item_data: ItemUpdate) -> ItemResponse:
        """
        Update an existing item.
        
        Args:
            item_id: Item identifier
            item_data: Update data (only provided fields will be updated)
            
        Returns:
            Updated item
            
        Raises:
            HTTPException: If item not found
        """
        if item_id not in _items_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        
        item = _items_db[item_id]
        update_data = item_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            item[field] = value
        
        item["updated_at"] = datetime.now(timezone.utc)
        
        return ItemResponse(**item)
    
    async def delete_item(self, item_id: int) -> None:
        """
        Delete an item.
        
        Args:
            item_id: Item identifier
            
        Raises:
            HTTPException: If item not found
        """
        if item_id not in _items_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        
        del _items_db[item_id]
    
    async def clear_all_items(self) -> None:
        """
        Clear all items from storage.
        Primarily used for testing purposes.
        """
        global _next_id
        _items_db.clear()
        _next_id = 1
