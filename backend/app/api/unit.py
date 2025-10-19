from app.core.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas import (
    CreateUnitRequest,
    CreateUnitResponse,
    DeleteUnitRequest,
    DeleteUnitResponse,
    EditUnitRequest,
    EditUnitResponse,
    GetAllUnitsRequest,
    GetAllUnitsResponse,
)
from ..services.unit import UnitService

router = APIRouter(prefix="/units", tags=["Unit of Measurement"])


@router.post("/", response_model=CreateUnitResponse)
def create_unit(
    unit_data: CreateUnitRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new unit of measurement."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to create units.",
        )
    return UnitService.create_unit(db, unit_data)


@router.delete("/", response_model=DeleteUnitResponse)
def delete_unit(
    unit_data: DeleteUnitRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a unit of measurement."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to delete units.",
        )
    return UnitService.delete_unit(db, unit_data)


@router.put("/", response_model=EditUnitResponse)
def edit_unit(
    unit_data: EditUnitRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Edit an existing unit of measurement."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to edit units.",
        )
    return UnitService.edit_unit(db, unit_data)


@router.get("/", response_model=GetAllUnitsResponse)
def get_all_units(
    _=Depends(get_current_user),
    unit_name: str = None,  # type: ignore
    db: Session = Depends(get_db),
):
    """Retrieve all units of measurement, optionally filtered by unit name."""
    query_params = GetAllUnitsRequest(unitName=unit_name)
    return UnitService.get_all_units(db, query_params)
