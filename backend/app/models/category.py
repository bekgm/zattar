"""Category model"""
from sqlalchemy import String, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
import uuid


class Category(Base):
    """Product category model"""

    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    icon_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    listings: Mapped[list["Listing"]] = relationship(
        "Listing", back_populates="category"
    )

    __table_args__ = (Index("idx_category_slug", "slug"),)

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name}, slug={self.slug})>"
