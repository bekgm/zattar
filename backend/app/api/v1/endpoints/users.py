"""User endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
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
from app.core.exceptions import ValidationError, ConflictError, UnauthorizedError
from pydantic import BaseModel

router = APIRouter()


class VerifyEmailRequest(BaseModel):
    """Verify email request"""
    token: str


class ResendVerificationEmailRequest(BaseModel):
    """Resend verification email request"""
    email: str


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


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmailRequest,
    session: AsyncSession = Depends(get_session),
):
    """Verify user email"""
    try:
        service = UserService(session)
        user = await service.verify_email(request.token)
        return {"message": "Email verified successfully", "user_id": user.id}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/resend-verification-email")
async def resend_verification_email(
    request: ResendVerificationEmailRequest,
    session: AsyncSession = Depends(get_session),
):
    """Resend verification email"""
    try:
        service = UserService(session)
        result = await service.resend_verification_email(request.email)
        if result:
            return {"message": "Verification email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send verification email")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
