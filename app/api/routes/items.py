"""Items CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_item_service
from app.models.schemas import ErrorResponse, ItemCreate, ItemResponse, MessageResponse
from app.services.item_service import ItemService

router = APIRouter()


@router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Item",
    description="Create a new item with the provided details",
    responses={
        201: {"description": "Item created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input data"}
    },
    tags=["Items"]
)
async def create_item(
    item: ItemCreate,
    service: ItemService = Depends(get_item_service)
) -> ItemResponse:
    """Create a new item.
    
    Args:
        item: Item data to create
        service: Injected ItemService instance
        
    Returns:
        ItemResponse: The created item with assigned ID
    """
    return await service.create_item(item)


@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Item",
    description="Retrieve a specific item by ID",
    responses={
        200: {"description": "Item retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    },
    tags=["Items"]
)
async def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
) -> ItemResponse:
    """Get an item by ID.
    
    Args:
        item_id: The ID of the item to retrieve
        service: Injected ItemService instance
        
    Returns:
        ItemResponse: The requested item
        
    Raises:
        HTTPException: 404 if item not found
    """
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


@router.get(
    "/items",
    response_model=List[ItemResponse],
    status_code=status.HTTP_200_OK,
    summary="List Items",
    description="Retrieve a list of all items with pagination support",
    responses={
        200: {"description": "Items retrieved successfully"}
    },
    tags=["Items"]
)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    service: ItemService = Depends(get_item_service)
) -> List[ItemResponse]:
    """Get all items with pagination.
    
    Args:
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
        service: Injected ItemService instance
        
    Returns:
        List[ItemResponse]: List of items
    """
    return await service.get_all_items(skip=skip, limit=limit)


@router.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Item",
    description="Update an existing item with new data",
    responses={
        200: {"description": "Item updated successfully"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    },
    tags=["Items"]
)
async def update_item(
    item_id: int,
    item_data: ItemCreate,
    service: ItemService = Depends(get_item_service)
) -> ItemResponse:
    """Update an existing item.
    
    Args:
        item_id: The ID of the item to update
        item_data: New item data
        service: Injected ItemService instance
        
    Returns:
        ItemResponse: The updated item
        
    Raises:
        HTTPException: 404 if item not found
    """
    updated_item = await service.update_item(item_id, item_data)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return updated_item


@router.delete(
    "/items/{item_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Item",
    description="Delete an item by ID",
    responses={
        200: {"description": "Item deleted successfully"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    },
    tags=["Items"]
)
async def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
) -> MessageResponse:
    """Delete an item by ID.
    
    Args:
        item_id: The ID of the item to delete
        service: Injected ItemService instance
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: 404 if item not found
    """
    deleted = await service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return MessageResponse(message=f"Item with id {item_id} deleted successfully")
