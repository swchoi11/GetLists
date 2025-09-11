# routes/restaurant.py

from fastapi import APIRouter, HTTPException
from models.models import (
    RestaurantCreateRequest,
    RestaurantUpdateRequest,
    RestaurantResponse,
    StandardResponse,
    RestaurantListResponse,
)
from database import db_restaurant as db_manager

router = APIRouter()

@router.post("/restaurants", response_model=StandardResponse)
def create_restaurant(request: RestaurantCreateRequest):
    try:
        restaurant_id = db_manager.add_restaurant(
            name=request.name,
            description=request.description,
            category=request.category,
            rating=request.rating,
            address=request.address,
        )
        return StandardResponse(
            status="success",
            message=f"Restaurant created successfully with ID: {restaurant_id}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/restaurants", response_model=RestaurantListResponse)
def get_all_restaurants():
    try:
        rows = db_manager.get_all_restaurants()
        items = []
        for r in rows:
            items.append(
                RestaurantResponse(
                    id=r[0],
                    name=r[1],
                    description=r[2],
                    category=r[3],
                    rating=r[4],
                    address=r[5],
                    create_time=r[6],
                )
            )
        return RestaurantListResponse(
            status="success",
            restaurants=items,
            total_count=len(items),
        )
    except Exception as e:
        raise HTTPException(status_code=500, deta
        
@router.put("/restaurants/{restaurant_id}", response_model=StandardResponse)
def update_restaurant(restaurant_id: int, request: RestaurantUpdateRequest):
    try:
        exists = db_manager.get_restaurant_by_id(restaurant_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        updated = db_manager.update_restaurant(
            restaurant_id,
            name=request.name,
            description=request.description,
            category=request.category,
            rating=request.rating,
            address=request.address,
        )
        if updated == 0:
            return StandardResponse(status="success", message="No fields to update")
        return StandardResponse(status="success", message=f"Restaurant {restaurant_id} updated")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/restaurants/{restaurant_id}", response_model=StandardResponse)
def delete_restaurant(restaurant_id: int):
    try:
        deleted = db_manager.delete_restaurant(restaurant_id)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return StandardResponse(status="success", message=f"Restaurant {restaurant_id} deleted")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))