"""Safe Deal repository"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import Optional, List
from app.models.safe_deal import SafeDeal, SafeDealStatus
from app.repositories.base import BaseRepository


class SafeDealRepository(BaseRepository[SafeDeal]):
    """Safe Deal repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, SafeDeal)

    async def get_by_buyer(
        self, buyer_id: str, skip: int = 0, limit: int = 100
    ) -> List[SafeDeal]:
        """Get safe deals for buyer"""
        result = await self.session.execute(
            select(SafeDeal)
            .where(SafeDeal.buyer_id == buyer_id)
            .order_by(desc(SafeDeal.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_seller(
        self, seller_id: str, skip: int = 0, limit: int = 100
    ) -> List[SafeDeal]:
        """Get safe deals for seller"""
        result = await self.session.execute(
            select(SafeDeal)
            .where(SafeDeal.seller_id == seller_id)
            .order_by(desc(SafeDeal.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_listing(self, listing_id: str) -> List[SafeDeal]:
        """Get safe deals for listing"""
        result = await self.session.execute(
            select(SafeDeal)
            .where(SafeDeal.listing_id == listing_id)
            .order_by(desc(SafeDeal.created_at))
        )
        return result.scalars().all()

    async def get_pending_for_buyer(
        self, buyer_id: str, listing_id: str
    ) -> Optional[SafeDeal]:
        """Get pending safe deal for buyer and listing"""
        result = await self.session.execute(
            select(SafeDeal).where(
                and_(
                    SafeDeal.buyer_id == buyer_id,
                    SafeDeal.listing_id == listing_id,
                    SafeDeal.status == SafeDealStatus.PENDING,
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_expired(self) -> List[SafeDeal]:
        """Get expired safe deals"""
        from datetime import datetime
        
        result = await self.session.execute(
            select(SafeDeal).where(
                and_(
                    SafeDeal.expires_at <= datetime.utcnow(),
                    SafeDeal.status == SafeDealStatus.PENDING,
                )
            )
        )
        return result.scalars().all()
