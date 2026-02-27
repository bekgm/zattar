"""Chat repository"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import Optional, List
from app.models.chat import Conversation, Message
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    """Conversation repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Conversation)

    async def get_or_create(
        self, listing_id: str, buyer_id: str, seller_id: str
    ) -> Conversation:
        """Get or create conversation"""
        result = await self.session.execute(
            select(Conversation).where(
                and_(
                    Conversation.listing_id == listing_id,
                    Conversation.buyer_id == buyer_id,
                    Conversation.seller_id == seller_id,
                )
            )
        )
        conv = result.scalar_one_or_none()

        if not conv:
            conv = Conversation(
                listing_id=listing_id,
                buyer_id=buyer_id,
                seller_id=seller_id,
            )
            self.session.add(conv)
            await self.session.commit()
            await self.session.refresh(conv)

        return conv

    async def get_by_user(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get conversations for user (as buyer or seller)"""
        result = await self.session.execute(
            select(Conversation)
            .where(
                (Conversation.buyer_id == user_id)
                | (Conversation.seller_id == user_id)
            )
            .order_by(desc(Conversation.last_message_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_listing(self, listing_id: str) -> List[Conversation]:
        """Get all conversations for listing"""
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.listing_id == listing_id)
            .order_by(desc(Conversation.last_message_at))
        )
        return result.scalars().all()


class MessageRepository(BaseRepository[Message]):
    """Message repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Message)

    async def get_by_conversation(
        self, conversation_id: str, skip: int = 0, limit: int = 50
    ) -> List[Message]:
        """Get messages for conversation"""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def mark_as_read(self, conversation_id: str, user_id: str) -> int:
        """Mark messages as read for conversation"""
        # Update messages from other user
        result = await self.session.execute(
            select(Message)
            .where(
                and_(
                    Message.conversation_id == conversation_id,
                    Message.sender_id != user_id,
                    Message.is_read == False,
                )
            )
        )
        messages = result.scalars().all()
        
        for msg in messages:
            msg.is_read = True
        
        await self.session.commit()
        return len(messages)
