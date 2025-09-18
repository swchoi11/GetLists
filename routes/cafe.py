from fastapi import APIRouter, HTTPException
from typing import List
from models.models import CafeCreateRequest, CafeUpdateRequest, CafeResponse, StandardResponse, CafeListResponse
from database import db_cafe as db_manager

router = APIRouter()

@router.post("/cafes", response_model=StandardResponse)
def create_cafe(request: CafeCreateRequest):
    """
    새로운 카페를 생성합니다.

    Args:
        request: 카페 생성 요청 데이터
            - cafe_name: 카페명
            - description: 카페 설명
            - rating: 평점 (1-5)

    Returns:
        StandardResponse: 생성 성공 메시지와 카페 ID

    Raises:
        HTTPException: 서버 에러 시 500 상태코드
    """
    try:
        cafe_id = db_manager.add_cafe(
            cafe_name=request.cafe_name,
            description=request.description,
            rating=request.rating
        )
        return StandardResponse(
            status="success",
            message=f"Cafe created successfully with ID: {cafe_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cafes", response_model=CafeListResponse)
def get_all_cafes():
    """
    모든 카페 목록을 조회합니다.

    Returns:
        CafeListResponse: 카페 목록과 총 개수
            - status: 응답 상태
            - cafes: 카페 정보 리스트
            - total_count: 전체 카페 수

    Raises:
        HTTPException: 서버 에러 시 500 상태코드
    """
    try:
        cafes_data = db_manager.get_all_cafes()
        cafes = []
        for cafe_row in cafes_data:
            cafe = CafeResponse(
                id=cafe_row[0],
                cafe_name=cafe_row[1],
                description=cafe_row[2],
                rating=cafe_row[3],
                create_time=cafe_row[4]
            )
            cafes.append(cafe)
        
        return CafeListResponse(
            status="success",
            cafes=cafes,
            total_count=len(cafes)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cafes/{cafe_id}", response_model=StandardResponse)
def update_cafe(cafe_id: int, request: CafeUpdateRequest):
    """
    특정 카페 정보를 수정합니다.

    Args:
        cafe_id: 수정할 카페의 ID
        request: 카페 수정 요청 데이터
            - cafe_name: 새로운 카페명
            - description: 새로운 카페 설명
            - rating: 새로운 평점 (1-5)

    Returns:
        StandardResponse: 수정 성공 메시지

    Raises:
        HTTPException: 서버 에러 시 500 상태코드
    """
    try:
        db_manager.update_cafe(
            cafe_id=cafe_id,
            cafe_name=request.cafe_name,
            description=request.description,
            rating=request.rating
        )
        return StandardResponse(
            status="success",
            message=f"Cafe {cafe_id} updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cafes/{cafe_id}", response_model=StandardResponse)
def delete_cafe(cafe_id: int):
    """
    특정 카페를 삭제합니다.

    Args:
        cafe_id: 삭제할 카페의 ID

    Returns:
        StandardResponse: 삭제 성공 메시지

    Raises:
        HTTPException: 서버 에러 시 500 상태코드
    """
    try:
        db_manager.delete_cafe(cafe_id)
        return StandardResponse(
            status="success",
            message=f"Cafe {cafe_id} deleted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
