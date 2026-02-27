"""User service"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple
from app.repositories.user import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import ValidationError, ConflictError, UnauthorizedError
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse
from datetime import datetime


class UserService:
    """User business logic service"""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def register(self, data: UserRegisterRequest) -> TokenResponse:
        """Register new user"""
        # Check if email exists
        if await self.repository.get_by_email(data.email):
            raise ConflictError("Email already registered")

        # Check if username exists
        if await self.repository.get_by_username(data.username):
            raise ConflictError("Username already taken")

        # Check if phone exists
        if await self.repository.get_by_phone(data.phone):
            raise ConflictError("Phone number already registered")

        # Create user
        user = await self.repository.create({
            "email": data.email,
            "phone": data.phone,
            "username": data.username,
            "password_hash": hash_password(data.password),
        })

        # Create tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=60 * 30,  # 30 minutes
        )

    async def login(self, data: UserLoginRequest) -> TokenResponse:
        """Login user"""
        # Get user by email
        user = await self.repository.get_by_email(data.email)
        if not user:
            raise UnauthorizedError("Invalid email or password")

        # Check password
        if not verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        # Check if user is active
        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        # Update last login
        user.last_login = datetime.utcnow()
        await self.session.commit()

        # Create tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=60 * 30,
        )

    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return await self.repository.get_by_id(user_id)

    async def get_user_profile(self, user_id: str) -> Optional[User]:
        """Get user profile"""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found")
        return user

    async def update_profile(self, user_id: str, data: dict) -> User:
        """Update user profile"""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found")

        user = await self.repository.update(user_id, data)
        return user

    async def block_user(self, user_id: str) -> User:
        """Block user"""
        user = await self.repository.update(user_id, {"is_blocked": True})
        if not user:
            raise ValidationError("User not found")
        return user
