"""Listing model"""
from sqlalchemy import (
    String,
    Text,
    Float,
    Integer,
    DateTime,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid
import enum


class ListingCondition(str, enum.Enum):
    """Listing condition enum"""

    NEW = "new"
    USED = "used"


class ListingStatus(str, enum.Enum):
    """Listing status enum"""

    ACTIVE = "active"
    SOLD = "sold"
    ARCHIVED = "archived"


class Listing(Base):
    """Listing model"""

    __tablename__ = "listings"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    seller_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    category_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("categories.id"), index=True
    )

    # Content
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, index=True)

    # Metadata
    city: Mapped[str] = mapped_column(String(100), index=True)
    condition: Mapped[ListingCondition] = mapped_column(
        Enum(ListingCondition), default=ListingCondition.USED
    )
    status: Mapped[ListingStatus] = mapped_column(
        Enum(ListingStatus), default=ListingStatus.ACTIVE, index=True
    )

    # Engagement
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    # Full-text search support (PostgreSQL)
    search_vector: Mapped[str | None] = mapped_column(String, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    seller: Mapped["User"] = relationship("User", back_populates="listings")
    category: Mapped["Category"] = relationship("Category", back_populates="listings")
    images: Mapped[list["ListingImage"]] = relationship(
        "ListingImage", back_populates="listing", cascade="all, delete-orphan"
    )
    views: Mapped[list["ListingView"]] = relationship(
        "ListingView", back_populates="listing", cascade="all, delete-orphan"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="listing", cascade="all, delete-orphan"
    )
    safe_deals: Mapped[list["SafeDeal"]] = relationship(
        "SafeDeal", back_populates="listing", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_listing_seller_status", "seller_id", "status"),
        Index("idx_listing_category_status", "category_id", "status"),
        Index("idx_listing_city_status", "city", "status"),
        Index("idx_listing_created_at", "created_at"),
        Index("idx_listing_price", "price"),
    )

    def __repr__(self) -> str:
        return f"<Listing(id={self.id}, title={self.title}, seller_id={self.seller_id})>"


class ListingImage(Base):
    """Listing image model"""

    __tablename__ = "listing_images"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    listing_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("listings.id"), index=True
    )
    image_url: Mapped[str] = mapped_column(String(500))
    s3_key: Mapped[str] = mapped_column(String(500), unique=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    listing: Mapped["Listing"] = relationship("Listing", back_populates="images")

    __table_args__ = (Index("idx_listing_image_order", "listing_id", "order"),)

    def __repr__(self) -> str:
        return f"<ListingImage(id={self.id}, listing_id={self.listing_id})>"


class ListingView(Base):
    """Listing view tracking model"""

    __tablename__ = "listing_views"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    listing_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("listings.id"), index=True
    )
    viewed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    # Relationships
    listing: Mapped["Listing"] = relationship("Listing", back_populates="views")

    __table_args__ = (Index("idx_listing_view_listing_date", "listing_id", "viewed_at"),)

    def __repr__(self) -> str:
        return f"<ListingView(id={self.id}, listing_id={self.listing_id})>"
