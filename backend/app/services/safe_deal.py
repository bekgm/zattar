"""Safe Deal service"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
from app.repositories.safe_deal import SafeDealRepository
from app.models.safe_deal import SafeDeal, SafeDealStatus
from app.core.exceptions import ValidationError, ForbiddenError
from app.schemas.safe_deal import SafeDealInitiateRequest, SafeDealTransitionRequest
from app.config import settings


class SafeDealService:
    """Safe Deal business logic service"""

    def __init__(self, session: AsyncSession):
        self.repository = SafeDealRepository(session)
        self.session = session

    async def initiate_deal(
        self, listing_id: str, buyer_id: str, seller_id: str, data: SafeDealInitiateRequest
    ) -> SafeDeal:
        """Initiate safe deal"""
        # Check if deal already exists and is pending
        existing = await self.repository.get_pending_for_buyer(buyer_id, listing_id)
        if existing:
            raise ValidationError("You already have a pending deal for this listing")

        # Create deal with expiration
        expires_at = datetime.utcnow() + timedelta(
            days=settings.SAFE_DEAL_TIMEOUT_DAYS
        )

        deal = await self.repository.create({
            "listing_id": listing_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "amount": data.amount,
            "currency": data.currency,
            "status": SafeDealStatus.PENDING,
            "expires_at": expires_at,
        })
        return deal

    async def get_deal(self, deal_id: str) -> Optional[SafeDeal]:
        """Get deal by ID"""
        deal = await self.repository.get_by_id(deal_id)
        if not deal:
            raise ValidationError("Safe deal not found")
        return deal

    async def transition_deal(
        self, deal_id: str, user_id: str, data: SafeDealTransitionRequest
    ) -> SafeDeal:
        """Transition deal to new status"""
        deal = await self.repository.get_by_id(deal_id)
        if not deal:
            raise ValidationError("Safe deal not found")

        # Authorize user (must be buyer or seller)
        if user_id not in [deal.buyer_id, deal.seller_id]:
            raise ForbiddenError("You are not part of this deal")

        # Authority checks based on status transition
        if data.status == SafeDealStatus.SHIPPED:
            # Only seller can mark as shipped
            if user_id != deal.seller_id:
                raise ForbiddenError("Only seller can mark deal as shipped")

        elif data.status == SafeDealStatus.COMPLETED:
            # Only buyer can confirm completion
            if user_id != deal.buyer_id:
                raise ForbiddenError("Only buyer can confirm delivery")

        elif data.status == SafeDealStatus.DISPUTED:
            # Either party can dispute
            pass

        elif data.status == SafeDealStatus.CANCELLED:
            # Can cancel only if pending (both parties could cancel at pending stage)
            if deal.status != SafeDealStatus.PENDING:
                raise ValidationError("Deal can only be cancelled in pending state")

        # Validate transition
        if not deal.can_transition_to(data.status):
            raise ValidationError(
                f"Cannot transition from {deal.status} to {data.status}"
            )

        # Update status
        deal.transition_to(data.status)
        
        if data.shipping_number:
            deal.shipping_number = data.shipping_number
        if data.dispatch_note:
            deal.dispatch_note = data.dispatch_note
        if data.dispute_reason:
            deal.dispute_reason = data.dispute_reason

        await self.session.commit()
        return deal

    async def get_buyer_deals(
        self, buyer_id: str, skip: int = 0, limit: int = 50
    ) -> List[SafeDeal]:
        """Get deals for buyer"""
        return await self.repository.get_by_buyer(buyer_id, skip, limit)

    async def get_seller_deals(
        self, seller_id: str, skip: int = 0, limit: int = 50
    ) -> List[SafeDeal]:
        """Get deals for seller"""
        return await self.repository.get_by_seller(seller_id, skip, limit)

    async def auto_complete_expired_deals(self) -> int:
        """Auto-complete expired pending deals"""
        expired_deals = await self.repository.get_expired()
        count = 0

        for deal in expired_deals:
            deal.transition_to(SafeDealStatus.COMPLETED)
            count += 1

        if count > 0:
            await self.session.commit()

        return count
