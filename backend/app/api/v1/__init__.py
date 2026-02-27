"""V1 API routes"""
from fastapi import APIRouter
from .endpoints.users import router as users_router
from .endpoints.listings import router as listings_router
from .endpoints.chat import router as chat_router
from .endpoints.safe_deals import router as safe_deals_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(listings_router, prefix="/listings", tags=["listings"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(safe_deals_router, prefix="/safe-deals", tags=["safe-deals"])

__all__ = ["api_router"]
