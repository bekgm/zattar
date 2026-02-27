"""User schemas"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegisterRequest(BaseModel):
    """User registration request"""

    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)


class UserLoginRequest(BaseModel):
    """User login request"""

    email: EmailStr
    password: str


class UserBaseResponse(BaseModel):
    """Base user response"""

    id: str
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(UserBaseResponse):
    """User response"""

    rating: float
    total_reviews: int
    is_verified: bool
    created_at: datetime


class UserProfileResponse(UserResponse):
    """User profile response (full details)"""

    phone: str
    bio: Optional[str] = None
    is_active: bool
    updated_at: datetime
    last_login: Optional[datetime] = None


class UserListingResponse(UserBaseResponse):
    """User response for listing context"""

    rating: float


class TokenResponse(BaseModel):
    """Token response"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
