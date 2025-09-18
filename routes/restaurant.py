# routes/restaurant.py
## HTTP 인터페이스(컨트롤러/라우팅 레이어)
## 요청 검증(Pydantic) → DB 레이어 호출 → 응답 모델로 직렬화 → HTTP 상태코드/에러 변환

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
        res_data = db_manager.get_all_restaurants()
        restaurants = []
        for res_row in res_data:
            res = RestaurantResponse(
                    id=res_row[0],
                    name=res_row[1],
                    description=res_row[2],
                    category=res_row[3],
                    rating=res_row[4],
                    address=res_row[5],
                    create_time=res_row[6],
                )
            
        return RestaurantListResponse(
            status="success",
            restaurants=items,
            total_count=len(restaurants),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
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
