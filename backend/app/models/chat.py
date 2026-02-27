"""Chat model"""
from sqlalchemy import String, DateTime, ForeignKey, Text, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
import uuid


class Conversation(Base):
    """Conversation model"""

    __tablename__ = "conversations"

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

    # Metadata
    last_message_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    # Relationships
    listing: Mapped["Listing"] = relationship("Listing", back_populates="conversations")
    buyer: Mapped["User"] = relationship(
        "User",
        foreign_keys=[buyer_id],
        back_populates="conversations_as_buyer",
    )
    seller: Mapped["User"] = relationship(
        "User",
        foreign_keys=[seller_id],
        back_populates="conversations_as_seller",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("listing_id", "buyer_id", "seller_id", name="unique_conversation"),
        Index("idx_conversation_participants", "buyer_id", "seller_id"),
        Index("idx_conversation_last_message", "last_message_at"),
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, listing_id={self.listing_id})>"


class Message(Base):
    """Message model"""

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.id"), index=True
    )
    sender_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )
    content: Mapped[str] = mapped_column(Text)

    # Read status
    is_read: Mapped[bool] = mapped_column(default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )
    sender: Mapped["User"] = relationship("User", back_populates="messages")

    __table_args__ = (
        Index("idx_message_conversation_created", "conversation_id", "created_at"),
        Index("idx_message_sender", "sender_id"),
        Index("idx_message_read", "is_read"),
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, conversation_id={self.conversation_id})>"
