"""Chat schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MessageRequest(BaseModel):
    """Message request"""

    content: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    """Message response"""

    id: str
    conversation_id: str
    sender_id: str
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Conversation response"""

    id: str
    listing_id: str
    buyer_id: str
    seller_id: str
    last_message_at: datetime
    created_at: datetime
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Conversation list response (lightweight)"""

    id: str
    listing_id: str
    buyer_id: str
    seller_id: str
    last_message_at: datetime
    created_at: datetime
    listing_title: str
    other_party: dict  # User info


class ConversationDetailResponse(ConversationResponse):
    """Conversation detail response"""

    buyer: dict  # UserResponse
    seller: dict  # UserResponse
