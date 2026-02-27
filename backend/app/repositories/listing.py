"""Listing repository"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from typing import Optional, List
from app.models.listing import Listing, ListingStatus, ListingCondition
from app.repositories.base import BaseRepository


class ListingRepository(BaseRepository[Listing]):
    """Listing repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Listing)

    async def get_active_listings(
        self, skip: int = 0, limit: int = 100
    ) -> List[Listing]:
        """Get active listings"""
        result = await self.session.execute(
            select(Listing)
            .where(Listing.status == ListingStatus.ACTIVE)
            .order_by(desc(Listing.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_seller_id(
        self, seller_id: str, skip: int = 0, limit: int = 100
    ) -> List[Listing]:
        """Get listings by seller"""
        result = await self.session.execute(
            select(Listing)
            .where(Listing.seller_id == seller_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_category(
        self,
        category_id: str,
        skip: int = 0,
        limit: int = 100,
        status: ListingStatus = ListingStatus.ACTIVE,
    ) -> List[Listing]:
        """Get listings by category"""
        result = await self.session.execute(
            select(Listing)
            .where(
                and_(
                    Listing.category_id == category_id,
                    Listing.status == status,
                )
            )
            .order_by(desc(Listing.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_city(
        self,
        city: str,
        skip: int = 0,
        limit: int = 100,
        status: ListingStatus = ListingStatus.ACTIVE,
    ) -> List[Listing]:
        """Get listings by city"""
        result = await self.session.execute(
            select(Listing)
            .where(
                and_(
                    Listing.city == city,
                    Listing.status == status,
                )
            )
            .order_by(desc(Listing.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search(
        self,
        query: str = None,
        city: str = None,
        category_id: str = None,
        min_price: float = None,
        max_price: float = None,
        condition: ListingCondition = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Listing]:
        """Search listings with filters"""
        filters = [Listing.status == ListingStatus.ACTIVE]

        if query:
            filters.append(
                or_(
                    Listing.title.ilike(f"%{query}%"),
                    Listing.description.ilike(f"%{query}%"),
                )
            )
        if city:
            filters.append(Listing.city == city)
        if category_id:
            filters.append(Listing.category_id == category_id)
        if condition:
            filters.append(Listing.condition == condition)
        if min_price is not None:
            filters.append(Listing.price >= min_price)
        if max_price is not None:
            filters.append(Listing.price <= max_price)

        result = await self.session.execute(
            select(Listing)
            .where(and_(*filters))
            .order_by(desc(Listing.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
