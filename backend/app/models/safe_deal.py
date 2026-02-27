"""Safe Deal model with state machine pattern"""
from sqlalchemy import String, Float, DateTime, ForeignKey, Enum, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid
import enum


class SafeDealStatus(str, enum.Enum):
    """Safe Deal status enum - State Machine Pattern"""

    PENDING = "pending"  # Initial state
    SHIPPED = "shipped"  # Seller marks as shipped
    COMPLETED = "completed"  # Buyer confirms delivery
    DISPUTED = "disputed"  # Dispute initiated
    CANCELLED = "cancelled"  # Deal cancelled


class SafeDeal(Base):
    """Safe Deal (Escrow) model"""

    __tablename__ = "safe_deals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    listing_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("listings.id"), index=True
    )
    buyer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )
    seller_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )

    # Financial
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3), default="KZT")

    # Status - State Machine
    status: Mapped[SafeDealStatus] = mapped_column(
        Enum(SafeDealStatus), default=SafeDealStatus.PENDING, index=True
    )

    # Tracking
    shipping_number: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dispatch_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    dispute_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    disputed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    listing: Mapped["Listing"] = relationship("Listing", back_populates="safe_deals")
    buyer: Mapped["User"] = relationship(
        "User",
        foreign_keys=[buyer_id],
        back_populates="safe_deals_as_buyer",
    )
    seller: Mapped["User"] = relationship(
        "User",
        foreign_keys=[seller_id],
        back_populates="safe_deals_as_seller",
    )

    __table_args__ = (
        Index("idx_safe_deal_buyer_status", "buyer_id", "status"),
        Index("idx_safe_deal_seller_status", "seller_id", "status"),
        Index("idx_safe_deal_listing", "listing_id"),
        Index("idx_safe_deal_expires", "expires_at"),
    )

    def __repr__(self) -> str:
        return f"<SafeDeal(id={self.id}, listing_id={self.listing_id}, status={self.status})>"

    def can_transition_to(self, new_status: SafeDealStatus) -> bool:
        """
        Check if transition is valid according to state machine.
        
        State transitions:
        PENDING -> SHIPPED, CANCELLED, DISPUTED
        SHIPPED -> COMPLETED, DISPUTED, CANCELLED
        COMPLETED -> DISPUTED
        DISPUTED -> (terminal state)
        CANCELLED -> (terminal state)
        """
        valid_transitions = {
            SafeDealStatus.PENDING: [
                SafeDealStatus.SHIPPED,
                SafeDealStatus.CANCELLED,
                SafeDealStatus.DISPUTED,
            ],
            SafeDealStatus.SHIPPED: [
                SafeDealStatus.COMPLETED,
                SafeDealStatus.DISPUTED,
                SafeDealStatus.CANCELLED,
            ],
            SafeDealStatus.COMPLETED: [SafeDealStatus.DISPUTED],
            SafeDealStatus.DISPUTED: [],
            SafeDealStatus.CANCELLED: [],
        }
        return new_status in valid_transitions.get(self.status, [])

    def transition_to(self, new_status: SafeDealStatus) -> bool:
        """Transition to a new status if valid"""
        if self.can_transition_to(new_status):
            self.status = new_status
            if new_status == SafeDealStatus.SHIPPED:
                self.shipped_at = datetime.utcnow()
            elif new_status == SafeDealStatus.COMPLETED:
                self.completed_at = datetime.utcnow()
            elif new_status == SafeDealStatus.DISPUTED:
                self.disputed_at = datetime.utcnow()
            return True
        return False
