from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# Category data structure
class CategoryData(BaseModel):
    id: int
    name: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")


# Add category endpoint schemas
class AddCategoryRequest(BaseModel):
    name: str = Field(..., min_length=1)


class AddCategoryResponse(BaseResponse):
    unit: CategoryData  # Note: API response uses "unit" key instead of "category"


# Get all categories endpoint schemas
class GetAllCategoriesRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetAllCategoriesResponse(BaseResponse):
    categories: List[CategoryData] = []


# Edit category endpoint schemas
class EditCategoryRequest(BaseModel):
    old_name: str = Field(..., alias="oldName", min_length=1)
    new_name: str = Field(..., alias="newName", min_length=1)


class EditCategoryResponse(BaseResponse):
    pass  # Only base response structure needed


# Delete category endpoint schemas
class DeleteCategoryRequest(BaseModel):
    name: str = Field(..., min_length=1)


class DeleteCategoryResponse(BaseResponse):
    pass  # Only base response structure needed
