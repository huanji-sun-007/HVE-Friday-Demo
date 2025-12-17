"""Tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_redirect():
    """Test that root endpoint redirects to docs."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_create_item():
    """Test creating an item."""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 19.99,
        "tax": 1.99
    }
    response = client.post("/api/v1/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert "id" in data


def test_get_item():
    """Test retrieving an item."""
    # First create an item
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 19.99
    }
    create_response = client.post("/api/v1/items", json=item_data)
    created_item = create_response.json()
    
    # Then retrieve it
    response = client.get(f"/api/v1/items/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_item["id"]
    assert data["name"] == item_data["name"]


def test_get_nonexistent_item():
    """Test retrieving a non-existent item."""
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404


def test_list_items():
    """Test listing items."""
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_item():
    """Test updating an item."""
    # First create an item
    item_data = {
        "name": "Original Name",
        "description": "Original description",
        "price": 10.00
    }
    create_response = client.post("/api/v1/items", json=item_data)
    created_item = create_response.json()
    
    # Update the item
    update_data = {
        "name": "Updated Name",
        "description": "Updated description",
        "price": 20.00
    }
    response = client.put(f"/api/v1/items/{created_item['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]


def test_delete_item():
    """Test deleting an item."""
    # First create an item
    item_data = {
        "name": "To Delete",
        "price": 5.00
    }
    create_response = client.post("/api/v1/items", json=item_data)
    created_item = create_response.json()
    
    # Delete the item
    response = client.delete(f"/api/v1/items/{created_item['id']}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/items/{created_item['id']}")
    assert get_response.status_code == 404


def test_item_validation():
    """Test item validation with invalid data."""
    # Test with negative price
    invalid_data = {
        "name": "Invalid Item",
        "price": -10.00
    }
    response = client.post("/api/v1/items", json=invalid_data)
    assert response.status_code == 422
    
    # Test with empty name
    invalid_data = {
        "name": "",
        "price": 10.00
    }
    response = client.post("/api/v1/items", json=invalid_data)
    assert response.status_code == 422
