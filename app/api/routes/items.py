"""
Item management endpoints.

Provides CRUD operations for items with proper validation and error handling.
"""

from typing import List, Optional
from fastapi import APIRouter, status, Query, Path

from app.api.dependencies import ItemServiceDep
from app.models.schemas import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Create a new item with the provided data",
)
async def create_item(
    item: ItemCreate,
    service: ItemServiceDep,
) -> ItemResponse:
    """
    Create a new item.
    
    Args:
        item: Item creation data
        service: Injected item service
        
    Returns:
        Created item with generated ID and timestamps
    """
    return await service.create_item(item)


@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Get an item by ID",
    description="Retrieve a specific item by its unique identifier",
)
async def get_item(
    item_id: int = Path(..., gt=0, description="Item ID"),
    service: ItemServiceDep = None,
) -> ItemResponse:
    """
    Retrieve an item by ID.
    
    Args:
        item_id: Unique item identifier
        service: Injected item service
        
    Returns:
        Item data
        
    Raises:
        HTTPException: 404 if item not found
    """
    return await service.get_item(item_id)


@router.get(
    "/items",
    response_model=List[ItemResponse],
    summary="List items",
    description="Retrieve a list of items with optional filtering and pagination",
)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of items to return"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    service: ItemServiceDep = None,
) -> List[ItemResponse]:
    """
    List items with optional filtering.
    
    Args:
        skip: Number of items to skip (pagination)
        limit: Maximum items to return
        min_price: Filter items with price >= min_price
        max_price: Filter items with price <= max_price
        service: Injected item service
        
    Returns:
        List of items matching the criteria
    """
    return await service.get_items(
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
    )


@router.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Update an item",
    description="Update an existing item with the provided data",
)
async def update_item(
    item_id: int = Path(..., gt=0, description="Item ID"),
    item: ItemUpdate = None,
    service: ItemServiceDep = None,
) -> ItemResponse:
    """
    Update an existing item.
    
    Args:
        item_id: Item identifier
        item: Update data (only provided fields will be updated)
        service: Injected item service
        
    Returns:
        Updated item
        
    Raises:
        HTTPException: 404 if item not found
    """
    return await service.update_item(item_id, item)


@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    description="Delete an item by its unique identifier",
)
async def delete_item(
    item_id: int = Path(..., gt=0, description="Item ID"),
    service: ItemServiceDep = None,
) -> None:
    """
    Delete an item.
    
    Args:
        item_id: Item identifier
        service: Injected item service
        
    Raises:
        HTTPException: 404 if item not found
    """
    await service.delete_item(item_id)
