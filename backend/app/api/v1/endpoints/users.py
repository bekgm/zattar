"""User endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.services.user import UserService
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    UserProfileResponse,
    TokenResponse,
)
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    """Register new user"""
    service = UserService(session)
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """Login user"""
    service = UserService(session)
    return await service.login(data)


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """Get current user profile"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get user by ID"""
    service = UserService(session)
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/me/profile", response_model=UserProfileResponse)
async def update_profile(
    data: dict,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update current user profile"""
    service = UserService(session)
    return await service.update_profile(current_user.id, data)
