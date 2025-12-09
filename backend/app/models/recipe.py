from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    html_content: Mapped[str] = mapped_column(Text)
    food_id: Mapped[int | None] = mapped_column(ForeignKey("foods.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    prep_time_minutes: Mapped[int | None] = mapped_column(Integer)
    cook_time_minutes: Mapped[int | None] = mapped_column(Integer)
    servings: Mapped[int | None] = mapped_column(Integer)
    difficulty: Mapped[str | None] = mapped_column(String(20))
    image_url: Mapped[str | None] = mapped_column(String(500))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
