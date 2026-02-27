"""Repository pattern implementation"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Generic, TypeVar, List, Optional
from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Base repository for all models"""

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities"""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, obj_in: dict) -> T:
        """Create entity"""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: str, obj_in: dict) -> Optional[T]:
        """Update entity"""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: str) -> bool:
        """Delete entity"""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        
        await self.session.delete(db_obj)
        await self.session.commit()
        return True

    async def exists(self, **filters) -> bool:
        """Check if entity exists"""
        query = select(self.model)
        for key, value in filters.items():
            query = query.where(getattr(self.model, key) == value)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
