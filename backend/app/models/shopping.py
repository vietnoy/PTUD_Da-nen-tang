"""Shopping-related database models."""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    assign_to_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    due_date: Mapped[date | None] = mapped_column(Date)
    priority: Mapped[str] = mapped_column(String(10), default="medium")  # low, medium, high
    status: Mapped[str] = mapped_column(String(20), default="active")  # draft, active, completed, cancelled
    budget: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    total_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ShoppingTask(Base):
    __tablename__ = "shopping_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    list_id: Mapped[int] = mapped_column(ForeignKey("shopping_lists.id", ondelete="CASCADE"))
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(8, 3))
    unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"))
    note: Mapped[str | None] = mapped_column(Text)
    estimated_cost: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    actual_cost: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    priority: Mapped[str] = mapped_column(String(10), default="medium")  # low, medium, high
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    done_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    done_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())