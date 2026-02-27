"""Safe Deal schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class SafeDealStatus(str, Enum):
    """Safe Deal status"""

    PENDING = "pending"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"


class SafeDealInitiateRequest(BaseModel):
    """Initiate Safe Deal request"""

    listing_id: str
    amount: float = Field(..., gt=0)
    currency: str = "KZT"


class SafeDealTransitionRequest(BaseModel):
    """Transition Safe Deal to new status"""

    status: SafeDealStatus
    shipping_number: Optional[str] = None
    dispatch_note: Optional[str] = None
    dispute_reason: Optional[str] = None


class SafeDealResponse(BaseModel):
    """Safe Deal response"""

    id: str
    listing_id: str
    buyer_id: str
    seller_id: str
    amount: float
    currency: str
    status: str
    shipping_number: Optional[str] = None
    dispatch_note: Optional[str] = None
    dispute_reason: Optional[str] = None
    created_at: datetime
    shipped_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    disputed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SafeDealDetailResponse(SafeDealResponse):
    """Safe Deal detail response"""

    buyer: dict  # UserResponse
    seller: dict  # UserResponse
    listing: dict  # ListingCardResponse
