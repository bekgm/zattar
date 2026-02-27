"""Listing service"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.repositories.listing import ListingRepository
from app.models.listing import Listing, ListingStatus
from app.core.exceptions import ValidationError, ForbiddenError
from app.schemas.listing import ListingCreateRequest, ListingUpdateRequest


class ListingService:
    """Listing business logic service"""

    def __init__(self, session: AsyncSession):
        self.repository = ListingRepository(session)
        self.session = session

    async def create_listing(
        self, seller_id: str, data: ListingCreateRequest
    ) -> Listing:
        """Create new listing"""
        listing = await self.repository.create({
            "seller_id": seller_id,
            "category_id": data.category_id,
            "title": data.title,
            "description": data.description,
            "price": data.price,
            "city": data.city,
            "condition": data.condition,
            "status": ListingStatus.ACTIVE,
        })
        return listing

    async def get_listing(self, listing_id: str) -> Optional[Listing]:
        """Get listing by ID"""
        listing = await self.repository.get_by_id(listing_id)
        if not listing:
            raise ValidationError("Listing not found")
        return listing

    async def update_listing(
        self, listing_id: str, seller_id: str, data: ListingUpdateRequest
    ) -> Listing:
        """Update listing - only seller can update"""
        listing = await self.repository.get_by_id(listing_id)
        if not listing:
            raise ValidationError("Listing not found")

        if listing.seller_id != seller_id:
            raise ForbiddenError("You can only update your own listings")

        update_data = data.dict(exclude_unset=True)
        listing = await self.repository.update(listing_id, update_data)
        return listing

    async def delete_listing(self, listing_id: str, seller_id: str) -> bool:
        """Delete listing - only seller can delete"""
        listing = await self.repository.get_by_id(listing_id)
        if not listing:
            raise ValidationError("Listing not found")

        if listing.seller_id != seller_id:
            raise ForbiddenError("You can only delete your own listings")

        return await self.repository.delete(listing_id)

    async def mark_as_sold(self, listing_id: str, seller_id: str) -> Listing:
        """Mark listing as sold"""
        listing = await self.repository.get_by_id(listing_id)
        if not listing:
            raise ValidationError("Listing not found")

        if listing.seller_id != seller_id:
            raise ForbiddenError("You can only mark your own listings as sold")

        listing = await self.repository.update(listing_id, {
            "status": ListingStatus.SOLD
        })
        return listing

    async def mark_as_archived(self, listing_id: str, seller_id: str) -> Listing:
        """Archive listing"""
        listing = await self.repository.get_by_id(listing_id)
        if not listing:
            raise ValidationError("Listing not found")

        if listing.seller_id != seller_id:
            raise ForbiddenError("You can only archive your own listings")

        listing = await self.repository.update(listing_id, {
            "status": ListingStatus.ARCHIVED
        })
        return listing

    async def increment_view_count(self, listing_id: str) -> Listing:
        """Increment view count"""
        listing = await self.repository.get_by_id(listing_id)
        if not listing:
            raise ValidationError("Listing not found")

        listing.view_count += 1
        await self.session.commit()
        return listing

    async def search_listings(
        self,
        query: str = None,
        city: str = None,
        category_id: str = None,
        min_price: float = None,
        max_price: float = None,
        condition: str = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Listing]:
        """Search listings"""
        return await self.repository.search(
            query=query,
            city=city,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            condition=condition,
            skip=skip,
            limit=limit,
        )

    async def get_user_listings(
        self, seller_id: str, skip: int = 0, limit: int = 20
    ) -> List[Listing]:
        """Get listings by seller"""
        return await self.repository.get_by_seller_id(
            seller_id, skip=skip, limit=limit
        )

    async def get_listings_by_category(
        self, category_id: str, skip: int = 0, limit: int = 20
    ) -> List[Listing]:
        """Get listings by category"""
        return await self.repository.get_by_category(
            category_id, skip=skip, limit=limit
        )
