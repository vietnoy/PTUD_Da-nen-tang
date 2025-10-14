from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# Unit data structure
class UnitData(BaseModel):
    id: int
    unit_name: str = Field(..., alias="unitName")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")


# Create unit endpoint schemas
class CreateUnitRequest(BaseModel):
    unit_name: str = Field(..., alias="unitName", min_length=1)


class CreateUnitResponse(BaseResponse):
    unit: UnitData


# Get all units endpoint schemas
class GetAllUnitsRequest(BaseModel):
    unit_name: Optional[str] = Field(None, alias="unitName")  # Optional query parameter


class GetAllUnitsResponse(BaseResponse):
    units: List[UnitData] = []


# Edit unit endpoint schemas
class EditUnitRequest(BaseModel):
    old_name: str = Field(..., alias="oldName", min_length=1)
    new_name: str = Field(..., alias="newName", min_length=1)


class EditUnitResponse(BaseResponse):
    pass  # Only base response structure needed


# Delete unit endpoint schemas
class DeleteUnitRequest(BaseModel):
    unit_name: str = Field(..., alias="unitName", min_length=1)


class DeleteUnitResponse(BaseResponse):
    pass  # Only base response structure needed
