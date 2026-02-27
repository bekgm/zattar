"""Listing schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ListingCondition(str, Enum):
    """Listing condition"""

    NEW = "new"
    USED = "used"


class ListingStatus(str, Enum):
    """Listing status"""

    ACTIVE = "active"
    SOLD = "sold"
    ARCHIVED = "archived"


class ImageResponse(BaseModel):
    """Image response"""

    id: str
    image_url: str
    order: int

    class Config:
        from_attributes = True


class ListingCreateRequest(BaseModel):
    """Create listing request"""

    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10, max_length=5000)
    price: float = Field(..., gt=0)
    city: str
    category_id: str
    condition: ListingCondition
    image_urls: List[str] = Field(default=[], max_length=10)


class ListingUpdateRequest(BaseModel):
    """Update listing request"""

    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    price: Optional[float] = Field(None, gt=0)
    city: Optional[str] = None
    condition: Optional[ListingCondition] = None
    status: Optional[ListingStatus] = None


class ListingCardResponse(BaseModel):
    """Listing card response (for lists)"""

    id: str
    title: str
    price: float
    city: str
    condition: str
    view_count: int
    created_at: datetime
    seller: dict  # UserListingResponse
    images: List[ImageResponse] = []

    class Config:
        from_attributes = True


class ListingResponse(ListingCardResponse):
    """Listing response"""

    category_id: str
    status: str
    updated_at: datetime


class ListingDetailResponse(ListingResponse):
    """Listing detail response"""

    description: str
    seller: dict  # UserProfileResponse


class ListingSearchFilters(BaseModel):
    """Search and filter parameters"""

    query: Optional[str] = None
    city: Optional[str] = None
    category_id: Optional[str] = None
    condition: Optional[ListingCondition] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: str = "created_at"  # created_at, price, views
    sort_order: str = "desc"  # asc, desc
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
