from fastapi import APIRouter, HTTPException
from typing import List
from models.models import CafeCreateRequest, CafeResponse, StandardResponse, CafeListResponse
from database import db_manager

router = APIRouter()

@router.post("/cafes", response_model=StandardResponse)
def create_cafe(request: CafeCreateRequest):
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
