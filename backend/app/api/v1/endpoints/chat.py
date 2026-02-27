"""Chat endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.services.chat import ChatService
from app.schemas.chat import (
    ConversationResponse,
    ConversationDetailResponse,
    MessageRequest,
    MessageResponse,
)
from app.models.user import User

router = APIRouter()


@router.post("/conversations/{listing_id}/{seller_id}", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def start_conversation(
    listing_id: str,
    seller_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Start or get conversation"""
    service = ChatService(session)
    conversation = await service.get_or_create_conversation(
        listing_id, current_user.id, seller_id
    )
    return conversation


@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get user conversations"""
    service = ChatService(session)
    conversations = await service.get_user_conversations(
        current_user.id, skip, limit
    )
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get conversation details"""
    service = ChatService(session)
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    conversation_id: str,
    data: MessageRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Send message"""
    service = ChatService(session)
    message = await service.send_message(conversation_id, current_user.id, data)
    return message


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get conversation messages"""
    service = ChatService(session)
    messages = await service.get_conversation_messages(
        conversation_id, skip, limit
    )
    return messages


@router.post("/conversations/{conversation_id}/mark-read")
async def mark_as_read(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Mark conversation as read"""
    service = ChatService(session)
    count = await service.mark_conversation_as_read(
        conversation_id, current_user.id
    )
    return {"marked_as_read": count}
