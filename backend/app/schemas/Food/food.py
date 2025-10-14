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


# Unit of measurement data structure
class UnitOfMeasurementData(BaseModel):
    id: Optional[int] = None
    unit_name: str = Field(..., alias="unitName")
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, alias="createdAt"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, alias="updatedAt"
    )


# Food category data structure
class FoodCategoryData(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, alias="createdAt"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, alias="updatedAt"
    )


# Food data structure for responses
class FoodData(BaseModel):
    id: int
    name: str
    image_url: str = Field(..., alias="imageUrl")
    type: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    food_category_id: int = Field(..., alias="FoodCategoryId")
    user_id: int = Field(..., alias="UserId")
    unit_of_measurement_id: int = Field(..., alias="UnitOfMeasurementId")
    unit_of_measurement: Optional[UnitOfMeasurementData] = Field(
        None, alias="UnitOfMeasurement"
    )
    food_category: Optional[FoodCategoryData] = Field(None, alias="FoodCategory")


# Create food endpoint schemas
class CreateFoodRequest(BaseModel):
    name: str = Field(..., min_length=1)
    food_category_name: str = Field(..., alias="foodCategoryName", min_length=1)
    unit_name: str = Field(..., alias="unitName", min_length=1)
    # Note: image file is handled separately in FastAPI endpoint using File() parameter


class CreateFoodResponse(BaseResponse):
    new_food: FoodData = Field(..., alias="newFood")


# Update food endpoint schemas
class UpdateFoodRequest(BaseModel):
    name: str = Field(..., min_length=1)
    new_category: str = Field(..., alias="newCategory", min_length=1)
    new_unit: str = Field(..., alias="newUnit", min_length=1)
    # Note: image file is handled separately in FastAPI endpoint using File() parameter


class UpdateFoodResponse(BaseResponse):
    food: FoodData


# Delete food endpoint schemas
class DeleteFoodRequest(BaseModel):
    name: str = Field(..., min_length=1)


class DeleteFoodResponse(BaseResponse):
    pass  # Only base response structure needed


# Get all foods endpoint schemas
class GetAllFoodsRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetAllFoodsResponse(BaseResponse):
    foods: List[FoodData] = []


# Get units endpoint schemas
class GetUnitsRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetUnitsResponse(BaseResponse):
    units: List[UnitOfMeasurementData] = []


# Get categories endpoint schemas
class GetCategoriesRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetCategoriesResponse(BaseResponse):
    categories: List[FoodCategoryData] = []
