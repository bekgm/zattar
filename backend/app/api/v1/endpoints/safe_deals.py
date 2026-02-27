"""Safe Deal endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.services.safe_deal import SafeDealService
from app.schemas.safe_deal import (
    SafeDealInitiateRequest,
    SafeDealResponse,
    SafeDealDetailResponse,
    SafeDealTransitionRequest,
)
from app.models.user import User

router = APIRouter()


@router.post("", response_model=SafeDealResponse, status_code=status.HTTP_201_CREATED)
async def initiate_safe_deal(
    data: SafeDealInitiateRequest,
    listing_id: str,
    seller_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Initiate safe deal"""
    service = SafeDealService(session)
    deal = await service.initiate_deal(
        listing_id, current_user.id, seller_id, data
    )
    return deal


@router.get("/{deal_id}", response_model=SafeDealDetailResponse)
async def get_deal(
    deal_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get deal details"""
    service = SafeDealService(session)
    deal = await service.get_deal(deal_id)
    return deal


@router.post("/{deal_id}/transition", response_model=SafeDealResponse)
async def transition_deal(
    deal_id: str,
    data: SafeDealTransitionRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Transition deal to new status"""
    service = SafeDealService(session)
    deal = await service.transition_deal(deal_id, current_user.id, data)
    return deal


@router.get("/buyer/deals", response_model=list[SafeDealResponse])
async def get_buyer_deals(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get buyer deals"""
    service = SafeDealService(session)
    deals = await service.get_buyer_deals(current_user.id, skip, limit)
    return deals


@router.get("/seller/deals", response_model=list[SafeDealResponse])
async def get_seller_deals(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get seller deals"""
    service = SafeDealService(session)
    deals = await service.get_seller_deals(current_user.id, skip, limit)
    return deals
