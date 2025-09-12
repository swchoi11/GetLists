# models/models.py
## request/response 정의

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StandardResponse(BaseModel):
    status: str
    message: Optional[str] = None

class RestaurantCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    address: Optional[str] = None

class RestaurantUpdateRequest(BaseModel):
    # 부분 업뎃 허용하기 위해 모두 optional
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    address: Optional[str] = None

class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    address: Optional[str] = None
    create_time: datetime

class RestaurantListResponse(BaseModel):
    status: str
    restaurants: list[RestaurantResponse]
    total_count: int