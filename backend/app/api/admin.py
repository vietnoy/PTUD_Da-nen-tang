"""
Admin API routes for managing units of measurement.
"""

from fastapi import APIRouter

from .unit import router as unit_router

router = APIRouter(prefix="/admin", tags=["Admin"])
router.include_router(unit_router)
