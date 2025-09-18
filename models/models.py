from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CafeCreateRequest(BaseModel):
    cafe_name: str
    description: Optional[str] = None
    rating: Optional[float] = None

class CafeUpdateRequest(BaseModel):
    cafe_name: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None

class CafeResponse(BaseModel):
    id: int
    cafe_name: str
    description: Optional[str] = None
    rating: Optional[float] = None
    create_time: str

class StandardResponse(BaseModel):
    status: str
    message: Optional[str] = None

class CafeListResponse(BaseModel):
    status: str
    cafes: list[CafeResponse]
    total_count: int

    