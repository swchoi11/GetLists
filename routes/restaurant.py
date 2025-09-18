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
    """
    새로운 레스토랑을 생성합니다.

    Args:
        request: 레스토랑 생성 요청 데이터
            - name: 레스토랑명
            - description: 레스토랑 설명
            - category: 음식 카테고리
            - rating: 평점 (1-5)
            - address: 주소

    Returns:
        StandardResponse: 생성 성공 메시지와 레스토랑 ID

    Raises:
        HTTPException: 서버 에러 시 500 상태코드
    """
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
    """
    모든 레스토랑 목록을 조회합니다.

    Returns:
        RestaurantListResponse: 레스토랑 목록과 총 개수
            - status: 응답 상태
            - restaurants: 레스토랑 정보 리스트
            - total_count: 전체 레스토랑 수

    Raises:
        HTTPException: 서버 에러 시 500 상태코드
    """
    try:
        rows = db_manager.get_all_restaurants()
        restaurants = []
        for r in rows:
            restaurants.append(
                RestaurantResponse(
                    id=r[0],
                    name=r[1],
                    description=r[2],
                    category=r[3],
                    rating=r[4],
                    address=r[5],
                    create_time=r[6],
                ))
            
        return RestaurantListResponse(
            status="success",
            restaurants=restaurants,
            total_count=len(restaurants),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.put("/restaurants/{restaurant_id}", response_model=StandardResponse)
def update_restaurant(restaurant_id: int, request: RestaurantUpdateRequest):
    """
    특정 레스토랑 정보를 수정합니다.

    Args:
        restaurant_id: 수정할 레스토랑의 ID
        request: 레스토랑 수정 요청 데이터
            - name: 새로운 레스토랑명
            - description: 새로운 레스토랑 설명
            - category: 새로운 음식 카테고리
            - rating: 새로운 평점 (1-5)
            - address: 새로운 주소

    Returns:
        StandardResponse: 수정 성공 메시지

    Raises:
        HTTPException: 레스토랑을 찾을 수 없을 때 404, 서버 에러 시 500 상태코드
    """
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
    """
    특정 레스토랑을 삭제합니다.

    Args:
        restaurant_id: 삭제할 레스토랑의 ID

    Returns:
        StandardResponse: 삭제 성공 메시지

    Raises:
        HTTPException: 레스토랑을 찾을 수 없을 때 404, 서버 에러 시 500 상태코드
    """
    try:
        deleted = db_manager.delete_restaurant(restaurant_id)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return StandardResponse(status="success", message=f"Restaurant {restaurant_id} deleted")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
