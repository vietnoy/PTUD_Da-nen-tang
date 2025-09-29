"""Food-related database models."""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(String(7))  # hex color
    icon: Mapped[str | None] = mapped_column(String(50))
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    symbol: Mapped[str | None] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(20))  # weight, volume, count, length
    base_unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"))
    conversion_factor: Mapped[Decimal | None] = mapped_column(Numeric(10, 6))
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    image_url: Mapped[str | None] = mapped_column(String(500))
    barcode: Mapped[str | None] = mapped_column(String(50))
    brand: Mapped[str | None] = mapped_column(String(50))
    default_shelf_life_days: Mapped[int | None] = mapped_column(Integer)
    storage_instructions: Mapped[str | None] = mapped_column(Text)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FridgeItem(Base):
    __tablename__ = "fridge_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(8, 3))
    unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"))
    note: Mapped[str | None] = mapped_column(Text)
    purchase_date: Mapped[date | None] = mapped_column(Date)
    use_within_date: Mapped[date] = mapped_column(Date)
    location: Mapped[str | None] = mapped_column(String(50))  # fridge, pantry, freezer
    is_opened: Mapped[bool] = mapped_column(Boolean, default=False)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cost: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())