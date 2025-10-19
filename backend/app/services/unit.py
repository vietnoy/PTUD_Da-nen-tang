from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import Unit
from ..schemas.Admin.UnitOfMeasurement.unitOfMeasurement import (
    BaseResponse,
    CreateUnitRequest,
    CreateUnitResponse,
    DeleteUnitRequest,
    DeleteUnitResponse,
    EditUnitRequest,
    EditUnitResponse,
    GetAllUnitsRequest,
    GetAllUnitsResponse,
    ResultMessage,
    UnitData,
)
from ..utils.responseCodeEnums import ResponseCode


class UnitService:
    """Service class for managing units of measurement."""

    @staticmethod
    def create_unit(db: Session, unit_data: CreateUnitRequest) -> CreateUnitResponse:
        """Create a new unit of measurement."""
        existing_unit = (
            db.query(Unit).filter(Unit.unit_name == unit_data.unit_name).first()
        )
        if existing_unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BaseResponse(
                    resultMessage=ResultMessage(
                        en="Unit with this name already exists",
                        vn=ResponseCode.UNIT_NAME_EXISTS.value[1],
                    ),
                    resultCode=ResponseCode.UNIT_NAME_EXISTS.value[0],
                ),
            )

        new_unit = Unit(unit_name=unit_data.unit_name)
        db.add(new_unit)
        db.commit()
        db.refresh(new_unit)

        return CreateUnitResponse(
            unit=UnitData(
                id=new_unit.id,
                unitName=new_unit.unit_name,
                createdAt=new_unit.created_at,
                updatedAt=new_unit.updated_at,
            ),
            resultMessage=ResultMessage(
                en="Unit created successfully",
                vn=ResponseCode.CREATE_UNIT_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.CREATE_UNIT_SUCCESS.value[0],
        )

    @staticmethod
    def delete_unit(db: Session, unit_data: DeleteUnitRequest) -> DeleteUnitResponse:
        """Delete a unit of measurement."""
        unit = db.query(Unit).filter(Unit.unit_name == unit_data.unit_name).first()
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BaseResponse(
                    resultMessage=ResultMessage(
                        en="Unit not found",
                        vn=ResponseCode.UNIT_NOT_FOUND_119.value[1],
                    ),
                    resultCode=ResponseCode.UNIT_NOT_FOUND_119.value[0],
                ),
            )

        db.delete(unit)
        db.commit()

        return DeleteUnitResponse(
            resultMessage=ResultMessage(
                en="Unit deleted successfully",
                vn=ResponseCode.DELETE_UNIT_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.DELETE_UNIT_SUCCESS.value[0],
        )

    @staticmethod
    def edit_unit(db: Session, unit_data: EditUnitRequest) -> EditUnitResponse:
        """Edit an existing unit of measurement."""
        unit = db.query(Unit).filter(Unit.unit_name == unit_data.old_name).first()
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BaseResponse(
                    resultMessage=ResultMessage(
                        en="Unit not found",
                        vn=ResponseCode.UNIT_NOT_FOUND_119.value[1],
                    ),
                    resultCode=ResponseCode.UNIT_NOT_FOUND_119.value[0],
                ),
            )

        unit.unit_name = unit_data.new_name
        db.commit()
        db.refresh(unit)

        return EditUnitResponse(
            resultMessage=ResultMessage(
                en="Unit updated successfully",
                vn=ResponseCode.UPDATE_UNIT_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.UPDATE_UNIT_SUCCESS.value[0],
        )

    @staticmethod
    def get_all_units(
        db: Session, query_params: GetAllUnitsRequest
    ) -> GetAllUnitsResponse:
        """Retrieves all units of measurement, optionally filtered by unit name."""
        query = db.query(Unit)
        if query_params.unit_name:
            query = query.filter(Unit.unit_name.ilike(f"%{query_params.unit_name}%"))

        units = query.all()

        unit_list = [
            UnitData(
                id=unit.id,
                unitName=unit.unit_name,
                createdAt=unit.created_at,
                updatedAt=unit.updated_at,
            )
            for unit in units
        ]

        return GetAllUnitsResponse(
            units=unit_list,
            resultMessage=ResultMessage(
                en="Units retrieved successfully",
                vn=ResponseCode.GET_UNITS_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.GET_UNITS_SUCCESS.value[0],
        )
