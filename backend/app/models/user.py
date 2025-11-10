"""User-related database models."""
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    type: Mapped[str | None] = mapped_column(String(20))
    language: Mapped[str] = mapped_column(String(5), default="en")
    gender: Mapped[str | None] = mapped_column(String(10))
    country_code: Mapped[str | None] = mapped_column(String(10))
    timezone: Mapped[int] = mapped_column(Integer, default=0)
    birth_date: Mapped[date | None] = mapped_column(Date)
    photo_url: Mapped[str | None] = mapped_column(String(500))
    avatar_url: Mapped[str | None] = mapped_column(String(500))  # Keep for backwards compatibility
    is_activated: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Keep for backwards compatibility
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    device_id: Mapped[str | None] = mapped_column(String(255))
    belongs_to_group_admin_id: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def password(self) -> str:
        """Password property for schema compatibility (always returns empty string)."""
        return ""