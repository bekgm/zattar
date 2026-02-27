"""Listing endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.services.listing import ListingService
from app.schemas.listing import (
    ListingCreateRequest,
    ListingUpdateRequest,
    ListingResponse,
    ListingDetailResponse,
    ListingCardResponse,
)
from app.models.user import User

router = APIRouter()


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    data: ListingCreateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create new listing"""
    service = ListingService(session)
    listing = await service.create_listing(current_user.id, data)
    return listing


@router.get("/{listing_id}", response_model=ListingDetailResponse)
async def get_listing(
    listing_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get listing by ID"""
    service = ListingService(session)
    listing = await service.get_listing(listing_id)
    # Increment view count
    listing = await service.increment_view_count(listing_id)
    return listing


@router.get("", response_model=list[ListingCardResponse])
async def search_listings(
    query: str = Query(None),
    city: str = Query(None),
    category_id: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Search listings"""
    service = ListingService(session)
    listings = await service.search_listings(
        query=query,
        city=city,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit,
    )
    return listings


@router.patch("/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: str,
    data: ListingUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update listing"""
    service = ListingService(session)
    listing = await service.update_listing(listing_id, current_user.id, data)
    return listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
    listing_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Delete listing"""
    service = ListingService(session)
    await service.delete_listing(listing_id, current_user.id)


@router.post("/{listing_id}/mark-sold", response_model=ListingResponse)
async def mark_listing_sold(
    listing_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Mark listing as sold"""
    service = ListingService(session)
    listing = await service.mark_as_sold(listing_id, current_user.id)
    return listing


@router.get("/user/{user_id}", response_model=list[ListingCardResponse])
async def get_user_listings(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get listings by user"""
    service = ListingService(session)
    listings = await service.get_user_listings(user_id, skip, limit)
    return listings
