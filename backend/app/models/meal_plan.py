from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    meal_type: Mapped[str] = mapped_column(String(20))
    meal_date: Mapped[date] = mapped_column(Date)
    serving_size: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"))
    note: Mapped[str | None] = mapped_column(Text)
    is_prepared: Mapped[bool] = mapped_column(Boolean, default=False)
    prepared_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
