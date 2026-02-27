"""Dependency injection"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import decode_token
from app.models.user import User
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthCredentials = Depends(security),
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    # Get user from database
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    
    return user


async def get_current_user_optional(
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthCredentials = None,
) -> Optional[User]:
    """Get current user (optional)"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(session, credentials)
    except HTTPException:
        return None
