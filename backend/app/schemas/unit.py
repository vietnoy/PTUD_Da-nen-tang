"""Unit schemas for administration and food management."""

from pydantic import BaseModel, Field

from .base import BaseResponse


# Unit data schema
class UnitData(BaseModel):
    """Unit data structure for responses."""

    id: int
    name: str
    type: str
    base_unit_id: int | None = Field(None, alias="baseUnitId")
    conversion_factor: float | None = Field(None, alias="conversionFactor")
    created_at: str = Field(..., alias="createdAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


# Get units endpoint schemas
class CreateUnitRequest(BaseModel):
    """Request body for creating a new unit."""

    name: str = Field(..., min_length=1, max_length=20)
    type: str = Field(..., min_length=1, max_length=20)  # weight, volume, count, length
    base_unit_id: int | None = Field(None, alias="baseUnitId")
    conversion_factor: float | None = Field(None, alias="conversionFactor")


class CreateUnitResponse(BaseResponse):
    """Response after successful unit creation."""

    unit: UnitData


class GetAllUnitsRequest(BaseModel):
    """Request for getting all units (empty body)."""

    pass


class GetAllUnitsResponse(BaseResponse):
    """Response for getting all units."""

    units: list[UnitData]


class EditUnitByNameRequest(BaseModel):
    """Request body for editing a unit by name."""

    old_name: str = Field(..., min_length=1, max_length=20)
    new_name: str = Field(..., min_length=1, max_length=20)
    type: str = Field(..., min_length=1, max_length=20)
    base_unit_id: int | None = Field(None, alias="baseUnitId")
    conversion_factor: float | None = Field(None, alias="conversionFactor")


class EditUnitByNameResponse(BaseResponse):
    """Response after successful unit name edit."""

    pass


class DeleteUnitRequest(BaseModel):
    """Request body for deleting a unit by name."""

    name: str = Field(..., min_length=1, max_length=20)


class DeleteUnitResponse(BaseResponse):
    """Response after successful unit deletion."""

    pass
