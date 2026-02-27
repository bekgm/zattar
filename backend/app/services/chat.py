"""Chat service"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.repositories.chat import ConversationRepository, MessageRepository
from app.models.chat import Conversation, Message
from app.core.exceptions import ValidationError, ForbiddenError
from app.schemas.chat import MessageRequest


class ChatService:
    """Chat business logic service"""

    def __init__(self, session: AsyncSession):
        self.conversation_repo = ConversationRepository(session)
        self.message_repo = MessageRepository(session)
        self.session = session

    async def get_or_create_conversation(
        self, listing_id: str, buyer_id: str, seller_id: str
    ) -> Conversation:
        """Get or create conversation"""
        return await self.conversation_repo.get_or_create(
            listing_id, buyer_id, seller_id
        )

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return await self.conversation_repo.get_by_id(conversation_id)

    async def get_user_conversations(
        self, user_id: str, skip: int = 0, limit: int = 50
    ) -> List[Conversation]:
        """Get conversations for user"""
        return await self.conversation_repo.get_by_user(user_id, skip, limit)

    async def send_message(
        self, conversation_id: str, sender_id: str, data: MessageRequest
    ) -> Message:
        """Send message in conversation"""
        conversation = await self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise ValidationError("Conversation not found")

        # Check if sender is participant
        if (
            sender_id != conversation.buyer_id
            and sender_id != conversation.seller_id
        ):
            raise ForbiddenError("You are not part of this conversation")

        # Create message
        message = await self.message_repo.create({
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "content": data.content,
        })

        # Update conversation last_message_at
        from datetime import datetime
        conversation.last_message_at = datetime.utcnow()
        await self.session.commit()

        return message

    async def get_conversation_messages(
        self, conversation_id: str, skip: int = 0, limit: int = 50
    ) -> List[Message]:
        """Get messages in conversation"""
        return await self.message_repo.get_by_conversation(
            conversation_id, skip, limit
        )

    async def mark_conversation_as_read(
        self, conversation_id: str, user_id: str
    ) -> int:
        """Mark conversation messages as read"""
        conversation = await self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            raise ValidationError("Conversation not found")

        if (
            user_id != conversation.buyer_id
            and user_id != conversation.seller_id
        ):
            raise ForbiddenError("You are not part of this conversation")

        return await self.message_repo.mark_as_read(conversation_id, user_id)
