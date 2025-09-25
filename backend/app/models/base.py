"""SQLAlchemy declarative base and shared metadata."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


__all__ = ["Base"]
