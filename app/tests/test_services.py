"""
Unit tests for ItemService.

Tests business logic and service layer operations.
"""

import pytest
from fastapi import HTTPException

from app.services.item_service import ItemService
from app.models.schemas import ItemCreate, ItemUpdate


@pytest.mark.asyncio
class TestItemService:
    """Test ItemService operations."""
    
    async def test_create_item(self, item_service, sample_item_data):
        """Test creating a new item."""
        item_data = ItemCreate(**sample_item_data)
        item = await item_service.create_item(item_data)
        
        assert item.id == 1
        assert item.name == sample_item_data["name"]
        assert item.description == sample_item_data["description"]
        assert item.price == sample_item_data["price"]
        assert item.quantity == sample_item_data["quantity"]
        assert item.created_at is not None
        assert item.updated_at is not None
    
    async def test_create_multiple_items(self, item_service, sample_items_data):
        """Test creating multiple items with incrementing IDs."""
        items = []
        for item_data in sample_items_data:
            item = await item_service.create_item(ItemCreate(**item_data))
            items.append(item)
        
        assert len(items) == 3
        assert items[0].id == 1
        assert items[1].id == 2
        assert items[2].id == 3
    
    async def test_get_item_success(self, item_service, sample_item_data):
        """Test retrieving an existing item."""
        created = await item_service.create_item(ItemCreate(**sample_item_data))
        retrieved = await item_service.get_item(created.id)
        
        assert retrieved.id == created.id
        assert retrieved.name == created.name
        assert retrieved.price == created.price
    
    async def test_get_item_not_found(self, item_service):
        """Test that getting non-existent item raises 404."""
        with pytest.raises(HTTPException) as exc_info:
            await item_service.get_item(999)
        
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()
    
    async def test_get_items_empty(self, item_service):
        """Test listing items when none exist."""
        items = await item_service.get_items()
        
        assert items == []
    
    async def test_get_items_with_data(self, item_service, sample_items_data):
        """Test listing all items."""
        # Create items
        for item_data in sample_items_data:
            await item_service.create_item(ItemCreate(**item_data))
        
        items = await item_service.get_items()
        
        assert len(items) == 3
        assert items[0].name == "Item 1"
        assert items[1].name == "Item 2"
        assert items[2].name == "Item 3"
    
    async def test_get_items_with_pagination(self, item_service, sample_items_data):
        """Test pagination parameters."""
        # Create items
        for item_data in sample_items_data:
            await item_service.create_item(ItemCreate(**item_data))
        
        # Get first page
        page1 = await item_service.get_items(skip=0, limit=2)
        assert len(page1) == 2
        assert page1[0].name == "Item 1"
        
        # Get second page
        page2 = await item_service.get_items(skip=2, limit=2)
        assert len(page2) == 1
        assert page2[0].name == "Item 3"
    
    async def test_get_items_with_min_price_filter(self, item_service, sample_items_data):
        """Test filtering by minimum price."""
        # Create items with prices: 10.00, 25.50, 99.99
        for item_data in sample_items_data:
            await item_service.create_item(ItemCreate(**item_data))
        
        items = await item_service.get_items(min_price=20.00)
        
        assert len(items) == 2
        assert all(item.price >= 20.00 for item in items)
    
    async def test_get_items_with_max_price_filter(self, item_service, sample_items_data):
        """Test filtering by maximum price."""
        # Create items with prices: 10.00, 25.50, 99.99
        for item_data in sample_items_data:
            await item_service.create_item(ItemCreate(**item_data))
        
        items = await item_service.get_items(max_price=30.00)
        
        assert len(items) == 2
        assert all(item.price <= 30.00 for item in items)
    
    async def test_get_items_with_price_range_filter(self, item_service, sample_items_data):
        """Test filtering by price range."""
        # Create items with prices: 10.00, 25.50, 99.99
        for item_data in sample_items_data:
            await item_service.create_item(ItemCreate(**item_data))
        
        items = await item_service.get_items(min_price=20.00, max_price=50.00)
        
        assert len(items) == 1
        assert items[0].price == 25.50
    
    async def test_update_item_success(self, item_service, sample_item_data):
        """Test updating an item."""
        created = await item_service.create_item(ItemCreate(**sample_item_data))
        
        update_data = ItemUpdate(name="Updated Name", price=39.99)
        updated = await item_service.update_item(created.id, update_data)
        
        assert updated.id == created.id
        assert updated.name == "Updated Name"
        assert updated.price == 39.99
        assert updated.description == created.description  # Unchanged
        assert updated.quantity == created.quantity  # Unchanged
        assert updated.updated_at > created.updated_at
    
    async def test_update_item_partial(self, item_service, sample_item_data):
        """Test partial update (only some fields)."""
        created = await item_service.create_item(ItemCreate(**sample_item_data))
        
        update_data = ItemUpdate(quantity=50)
        updated = await item_service.update_item(created.id, update_data)
        
        assert updated.quantity == 50
        assert updated.name == created.name  # Unchanged
        assert updated.price == created.price  # Unchanged
    
    async def test_update_item_not_found(self, item_service):
        """Test that updating non-existent item raises 404."""
        with pytest.raises(HTTPException) as exc_info:
            update_data = ItemUpdate(name="Updated")
            await item_service.update_item(999, update_data)
        
        assert exc_info.value.status_code == 404
    
    async def test_delete_item_success(self, item_service, sample_item_data):
        """Test deleting an item."""
        created = await item_service.create_item(ItemCreate(**sample_item_data))
        
        await item_service.delete_item(created.id)
        
        # Verify item is deleted
        with pytest.raises(HTTPException):
            await item_service.get_item(created.id)
    
    async def test_delete_item_not_found(self, item_service):
        """Test that deleting non-existent item raises 404."""
        with pytest.raises(HTTPException) as exc_info:
            await item_service.delete_item(999)
        
        assert exc_info.value.status_code == 404
    
    async def test_clear_all_items(self, item_service, sample_items_data):
        """Test clearing all items."""
        # Create items
        for item_data in sample_items_data:
            await item_service.create_item(ItemCreate(**item_data))
        
        await item_service.clear_all_items()
        
        items = await item_service.get_items()
        assert items == []
