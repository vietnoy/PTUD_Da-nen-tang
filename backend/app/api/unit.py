"""Unit-related API routes."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import Unit, User
from ..schemas.base import ResultMessage
from ..schemas.unit import (
    CreateUnitRequest,
    CreateUnitResponse,
    DeleteUnitRequest,
    DeleteUnitResponse,
    EditUnitByNameRequest,
    EditUnitByNameResponse,
    GetAllUnitsResponse,
    GetUnitById,
    GetUnitByIdResponse,
    UnitData,
)
from ..utils.resultCode import ResultCode

router = APIRouter(prefix="/unit", tags=["Units"])


@router.post(
    "/", response_model=CreateUnitResponse, status_code=status.HTTP_201_CREATED
)
def create_unit(
    request: CreateUnitRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    unit = db.query(Unit).filter(Unit.name == request.name).first()
    if unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit with this name already exists",
        )

    if request.type not in ["weight", "volume", "count", "length"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid unit type. Must be one of: weight, volume, count, length",
        )

    if request.base_unit_id:
        base_unit = db.query(Unit).filter(Unit.id == request.base_unit_id).first()
        if not base_unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Base unit with this ID does not exist",
            )
    if bool(request.conversion_factor) != bool(request.base_unit_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both base_unit_id and conversion_factor must be provided together",
        )

    new_unit = Unit(
        name=request.name,
        type=request.type,
        base_unit_id=request.base_unit_id,
        conversion_factor=request.conversion_factor,
    )
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return CreateUnitResponse(
        unit=UnitData.model_validate(new_unit),
        resultCode=ResultCode.SUCCESS_UNIT_CREATED.value[0],
        resultMessage=ResultMessage(
            en="Unit created successfully", vn=ResultCode.SUCCESS_UNIT_CREATED.value[1]
        ),
    )


@router.get("/", response_model=GetAllUnitsResponse)
def get_all_units(
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    units = db.query(Unit).all()
    unit_data_list = [UnitData.model_validate(unit) for unit in units]
    return GetAllUnitsResponse(
        units=unit_data_list,
        resultCode=ResultCode.SUCCESS_UNITS_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Units retrieved successfully",
            vn=ResultCode.SUCCESS_UNITS_FETCHED.value[1],
        ),
    )


@router.put("/", response_model=EditUnitByNameResponse)
def edit_unit_by_name(
    request: EditUnitByNameRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    unit = db.query(Unit).filter(Unit.name == request.old_name).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit with this name does not exist",
        )
    check_new_unit = db.query(Unit).filter(Unit.name == request.new_name).first()
    if check_new_unit and request.new_name != request.old_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Another unit with the new name already exists",
        )
    if request.new_name:
        unit.name = request.new_name
    if request.base_unit_id is not None:
        unit.base_unit_id = request.base_unit_id
    if request.conversion_factor is not None:
        unit.conversion_factor = Decimal(request.conversion_factor)
    db.commit()
    db.refresh(unit)
    return EditUnitByNameResponse(
        resultCode=ResultCode.SUCCESS_UNIT_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Unit edited successfully", vn=ResultCode.SUCCESS_UNIT_UPDATED.value[1]
        ),
    )


@router.delete("/", response_model=DeleteUnitResponse)
def delete_unit(
    request: DeleteUnitRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    unit = db.query(Unit).filter(Unit.name == request.name).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit with this name does not exist",
        )
    # Check if there are any dependent unit or not
    dependent_unit = db.query(Unit).filter(Unit.base_unit_id == unit.id).first()
    if dependent_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete unit as it is a base unit for other units",
        )
    db.delete(unit)
    db.commit()
    return DeleteUnitResponse(
        resultCode=ResultCode.SUCCESS_UNIT_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Unit deleted successfully", vn=ResultCode.SUCCESS_UNIT_DELETED.value[1]
        ),
    )


@router.get("/id", response_model=GetUnitByIdResponse)
def get_unit_by_id(
    request: GetUnitById,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    unit = db.query(Unit).filter(Unit.id == request.unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit with this ID does not exist",
        )
    return GetUnitByIdResponse(
        unit=UnitData.model_validate(unit),
        resultCode=ResultCode.SUCCESS_UNIT_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Unit retrieved successfully",
            vn=ResultCode.SUCCESS_UNIT_FETCHED.value[1],
        ),
    )


__all__ = ["router"]
