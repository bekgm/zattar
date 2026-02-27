"""User model"""
from sqlalchemy import String, Float, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid


class User(Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    # Profile
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Rating
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_reviews: Mapped[int] = mapped_column(default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Email Verification
    verification_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    verification_token_expires: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Security
    failed_login_attempts: Mapped[int] = mapped_column(default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    listings: Mapped[list["Listing"]] = relationship(
        "Listing", back_populates="seller", cascade="all, delete-orphan"
    )
    conversations_as_buyer: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        foreign_keys="Conversation.buyer_id",
        back_populates="buyer",
        cascade="all, delete-orphan",
    )
    conversations_as_seller: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        foreign_keys="Conversation.seller_id",
        back_populates="seller",
        cascade="all, delete-orphan",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="sender", cascade="all, delete-orphan"
    )
    safe_deals_as_buyer: Mapped[list["SafeDeal"]] = relationship(
        "SafeDeal",
        foreign_keys="SafeDeal.buyer_id",
        back_populates="buyer",
        cascade="all, delete-orphan",
    )
    safe_deals_as_seller: Mapped[list["SafeDeal"]] = relationship(
        "SafeDeal",
        foreign_keys="SafeDeal.seller_id",
        back_populates="seller",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("idx_user_email_active", "email", "is_active"),
        Index("idx_user_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
