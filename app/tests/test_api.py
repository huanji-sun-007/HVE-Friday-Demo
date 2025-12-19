"""
Integration tests for API endpoints.

Tests complete request/response cycles through the API.
"""

import pytest
from fastapi import status


class TestHealthEndpoints:
    """Test health check and root endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data


class TestItemEndpoints:
    """Test item CRUD endpoints."""
    
    def test_create_item(self, client, sample_item_data):
        """Test creating an item via API."""
        response = client.post("/api/v1/items", json=sample_item_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_item_data["name"]
        assert data["price"] == sample_item_data["price"]
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_item_invalid_data(self, client):
        """Test creating item with invalid data returns 422."""
        invalid_data = {
            "name": "",  # Empty name
            "price": -10.00  # Negative price
        }
        response = client.post("/api/v1/items", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_item_missing_required_fields(self, client):
        """Test creating item without required fields."""
        response = client.post("/api/v1/items", json={"name": "Test"})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_item(self, client, sample_item_data):
        """Test retrieving an item by ID."""
        # Create item
        create_response = client.post("/api/v1/items", json=sample_item_data)
        item_id = create_response.json()["id"]
        
        # Get item
        response = client.get(f"/api/v1/items/{item_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == sample_item_data["name"]
    
    def test_get_item_not_found(self, client):
        """Test getting non-existent item returns 404."""
        response = client.get("/api/v1/items/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_item_invalid_id(self, client):
        """Test getting item with invalid ID format."""
        response = client.get("/api/v1/items/invalid")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_list_items_empty(self, client):
        """Test listing items when none exist."""
        response = client.get("/api/v1/items")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_list_items_with_data(self, client, sample_items_data):
        """Test listing multiple items."""
        # Create items
        for item_data in sample_items_data:
            client.post("/api/v1/items", json=item_data)
        
        # List items
        response = client.get("/api/v1/items")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_list_items_with_pagination(self, client, sample_items_data):
        """Test pagination parameters."""
        # Create items
        for item_data in sample_items_data:
            client.post("/api/v1/items", json=item_data)
        
        # Get first page
        response = client.get("/api/v1/items?skip=0&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        
        # Get second page
        response = client.get("/api/v1/items?skip=2&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
    
    def test_list_items_with_price_filters(self, client, sample_items_data):
        """Test price filtering."""
        # Create items
        for item_data in sample_items_data:
            client.post("/api/v1/items", json=item_data)
        
        # Filter by min price
        response = client.get("/api/v1/items?min_price=20.00")
        assert response.status_code == status.HTTP_200_OK
        items = response.json()
        assert len(items) == 2
        assert all(item["price"] >= 20.00 for item in items)
        
        # Filter by max price
        response = client.get("/api/v1/items?max_price=30.00")
        assert response.status_code == status.HTTP_200_OK
        items = response.json()
        assert len(items) == 2
        assert all(item["price"] <= 30.00 for item in items)
    
    def test_update_item(self, client, sample_item_data):
        """Test updating an item."""
        # Create item
        create_response = client.post("/api/v1/items", json=sample_item_data)
        item_id = create_response.json()["id"]
        
        # Update item
        update_data = {"name": "Updated Name", "price": 49.99}
        response = client.put(f"/api/v1/items/{item_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Updated Name"
        assert data["price"] == 49.99
    
    def test_update_item_partial(self, client, sample_item_data):
        """Test partial update."""
        # Create item
        create_response = client.post("/api/v1/items", json=sample_item_data)
        item_id = create_response.json()["id"]
        original_name = create_response.json()["name"]
        
        # Update only quantity
        update_data = {"quantity": 100}
        response = client.put(f"/api/v1/items/{item_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == 100
        assert data["name"] == original_name  # Unchanged
    
    def test_update_item_not_found(self, client):
        """Test updating non-existent item returns 404."""
        update_data = {"name": "Updated"}
        response = client.put("/api/v1/items/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_item_invalid_data(self, client, sample_item_data):
        """Test updating with invalid data."""
        # Create item
        create_response = client.post("/api/v1/items", json=sample_item_data)
        item_id = create_response.json()["id"]
        
        # Try to update with negative price
        update_data = {"price": -10.00}
        response = client.put(f"/api/v1/items/{item_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_delete_item(self, client, sample_item_data):
        """Test deleting an item."""
        # Create item
        create_response = client.post("/api/v1/items", json=sample_item_data)
        item_id = create_response.json()["id"]
        
        # Delete item
        response = client.delete(f"/api/v1/items/{item_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify item is deleted
        get_response = client.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_item_not_found(self, client):
        """Test deleting non-existent item returns 404."""
        response = client.delete("/api/v1/items/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_complete_crud_workflow(self, client):
        """Test complete CRUD workflow."""
        # Create
        create_data = {
            "name": "Workflow Item",
            "description": "Testing CRUD",
            "price": 29.99,
            "quantity": 10
        }
        create_response = client.post("/api/v1/items", json=create_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        item_id = create_response.json()["id"]
        
        # Read
        read_response = client.get(f"/api/v1/items/{item_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["name"] == "Workflow Item"
        
        # Update
        update_data = {"name": "Updated Workflow Item"}
        update_response = client.put(f"/api/v1/items/{item_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["name"] == "Updated Workflow Item"
        
        # Delete
        delete_response = client.delete(f"/api/v1/items/{item_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deletion
        final_response = client.get(f"/api/v1/items/{item_id}")
        assert final_response.status_code == status.HTTP_404_NOT_FOUND


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation endpoints."""
    
    def test_openapi_json(self, client):
        """Test OpenAPI JSON is accessible."""
        response = client.get("/openapi.json")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_endpoint(self, client):
        """Test Swagger UI is accessible."""
        response = client.get("/docs")
        
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_endpoint(self, client):
        """Test ReDoc is accessible."""
        response = client.get("/redoc")
        
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
