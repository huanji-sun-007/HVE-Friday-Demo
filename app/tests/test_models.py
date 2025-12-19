"""
Unit tests for Pydantic models/schemas.

Tests validation logic, constraints, and model behavior.
"""

import pytest
from pydantic import ValidationError

from app.models.schemas import ItemCreate, ItemUpdate, ItemResponse


class TestItemCreate:
    """Test ItemCreate model validation."""
    
    def test_valid_item_create(self):
        """Test creating a valid item."""
        item = ItemCreate(
            name="Test Item",
            description="Test description",
            price=19.99,
            quantity=5
        )
        
        assert item.name == "Test Item"
        assert item.description == "Test description"
        assert item.price == 19.99
        assert item.quantity == 5
    
    def test_item_create_with_defaults(self):
        """Test item creation with default values."""
        item = ItemCreate(
            name="Minimal Item",
            price=9.99
        )
        
        assert item.name == "Minimal Item"
        assert item.description is None
        assert item.price == 9.99
        assert item.quantity == 0
    
    def test_item_create_strips_whitespace(self):
        """Test that name whitespace is stripped."""
        item = ItemCreate(
            name="  Spaced Name  ",
            price=19.99
        )
        
        assert item.name == "Spaced Name"
    
    def test_item_create_empty_name_fails(self):
        """Test that empty name raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="", price=19.99)
        
        assert "name" in str(exc_info.value).lower()
    
    def test_item_create_whitespace_only_name_fails(self):
        """Test that whitespace-only name raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="   ", price=19.99)
        
        assert "name" in str(exc_info.value).lower()
    
    def test_item_create_negative_price_fails(self):
        """Test that negative price raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="Test", price=-10.00)
        
        assert "price" in str(exc_info.value).lower()
    
    def test_item_create_zero_price_fails(self):
        """Test that zero price raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="Test", price=0)
        
        assert "price" in str(exc_info.value).lower()
    
    def test_item_create_negative_quantity_fails(self):
        """Test that negative quantity raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="Test", price=19.99, quantity=-5)
        
        assert "quantity" in str(exc_info.value).lower()
    
    def test_item_create_name_too_long_fails(self):
        """Test that overly long name raises validation error."""
        with pytest.raises(ValidationError):
            ItemCreate(name="x" * 101, price=19.99)
    
    def test_item_create_description_too_long_fails(self):
        """Test that overly long description raises validation error."""
        with pytest.raises(ValidationError):
            ItemCreate(
                name="Test",
                description="x" * 501,
                price=19.99
            )


class TestItemUpdate:
    """Test ItemUpdate model validation."""
    
    def test_item_update_all_fields(self):
        """Test updating all fields."""
        item = ItemUpdate(
            name="Updated",
            description="New description",
            price=29.99,
            quantity=20
        )
        
        assert item.name == "Updated"
        assert item.description == "New description"
        assert item.price == 29.99
        assert item.quantity == 20
    
    def test_item_update_partial(self):
        """Test partial update with only some fields."""
        item = ItemUpdate(name="Updated Name")
        
        assert item.name == "Updated Name"
        assert item.description is None
        assert item.price is None
        assert item.quantity is None
    
    def test_item_update_empty(self):
        """Test creating empty update (no fields)."""
        item = ItemUpdate()
        
        assert item.name is None
        assert item.description is None
        assert item.price is None
        assert item.quantity is None
    
    def test_item_update_negative_price_fails(self):
        """Test that negative price raises validation error."""
        with pytest.raises(ValidationError):
            ItemUpdate(price=-10.00)


class TestItemResponse:
    """Test ItemResponse model."""
    
    def test_item_response_creation(self):
        """Test creating an item response."""
        from datetime import datetime, timezone
        
        now = datetime.now(timezone.utc)
        item = ItemResponse(
            id=1,
            name="Response Item",
            description="Test",
            price=19.99,
            quantity=5,
            created_at=now,
            updated_at=now
        )
        
        assert item.id == 1
        assert item.name == "Response Item"
        assert item.created_at == now
        assert item.updated_at == now
