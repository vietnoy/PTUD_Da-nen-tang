"""API package."""

from fastapi import APIRouter

from .auth import router as auth_router
from .category import router as category_router
from .group import router as group_router
from .unit import router as unit_router
from .users import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(group_router)
api_router.include_router(unit_router)
api_router.include_router(category_router)
__all__ = ["api_router"]
