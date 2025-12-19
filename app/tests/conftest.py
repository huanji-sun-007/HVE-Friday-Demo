"""
Pytest configuration and fixtures.

This module provides common fixtures and configuration for all tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.item_service import ItemService


@pytest.fixture
def client():
    """
    Provide a test client for the FastAPI application.
    Clears items database before each test for isolation.
    """
    from app.services.item_service import _items_db
    import app.services.item_service as service_module
    
    # Clear state before test
    _items_db.clear()
    service_module._next_id = 1
    
    test_client = TestClient(app)
    yield test_client
    
    # Clear state after test
    _items_db.clear()
    service_module._next_id = 1


@pytest.fixture
def item_service():
    """
    Provide a fresh ItemService instance for each test.
    Clears all items before and after each test.
    """
    from app.services.item_service import _items_db, _next_id
    import app.services.item_service as service_module
    
    # Clear state before test
    _items_db.clear()
    service_module._next_id = 1
    
    service = ItemService()
    yield service
    
    # Clear state after test
    _items_db.clear()
    service_module._next_id = 1


@pytest.fixture
def sample_item_data():
    """
    Provide sample item data for testing.
    """
    return {
        "name": "Test Item",
        "description": "A test item for unit tests",
        "price": 29.99,
        "quantity": 10
    }


@pytest.fixture
def sample_items_data():
    """
    Provide multiple sample items for testing.
    """
    return [
        {
            "name": "Item 1",
            "description": "First test item",
            "price": 10.00,
            "quantity": 5
        },
        {
            "name": "Item 2",
            "description": "Second test item",
            "price": 25.50,
            "quantity": 15
        },
        {
            "name": "Item 3",
            "description": "Third test item",
            "price": 99.99,
            "quantity": 2
        }
    ]
