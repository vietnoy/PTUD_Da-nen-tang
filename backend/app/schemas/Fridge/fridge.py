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


# Unit of measurement data structure (for nested Food object)
class UnitOfMeasurementData(BaseModel):
    id: int
    unit_name: str = Field(..., alias="unitName")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")


# Food category data structure (for nested Food object)
class FoodCategoryData(BaseModel):
    id: int
    name: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")


# Food data structure (for nested Food object in fridge items)
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


# Fridge item data structure
class FridgeItemData(BaseModel):
    id: int
    expired_date: datetime = Field(default_factory=datetime.now, alias="expiredDate")
    quantity: int
    note: str
    start_date: datetime = Field(default_factory=datetime.now, alias="startDate")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    food_id: int = Field(..., alias="FoodId")
    user_id: int = Field(..., alias="UserId")
    food: Optional[FoodData] = Field(None, alias="Food")  # Nested food object


# Create fridge item endpoint schemas
class CreateFridgeItemRequest(BaseModel):
    food_name: str = Field(..., alias="foodName", min_length=1)
    use_within: str = Field(..., alias="useWithin")  # Duration in minutes
    quantity: str = Field(..., min_length=1)  # String as per API docs


class CreateFridgeItemResponse(BaseResponse):
    new_fridge_item: FridgeItemData = Field(..., alias="newFridgeItem")


# Update fridge item endpoint schemas
class UpdateFridgeItemRequest(BaseModel):
    item_id: str = Field(..., alias="itemId")
    new_note: str = Field(..., alias="newNote")
    new_quantity: str = Field(..., alias="newQuantity")
    new_use_within: str = Field(..., alias="newUseWithin")
    new_food_name: str = Field(..., alias="newFoodName", min_length=1)


class UpdateFridgeItemResponse(BaseResponse):
    updated_fridge_item: FridgeItemData = Field(..., alias="updatedFridgeItem")


# Delete fridge item endpoint schemas
class DeleteFridgeItemRequest(BaseModel):
    food_name: str = Field(..., alias="foodName", min_length=1)


class DeleteFridgeItemResponse(BaseResponse):
    pass  # Only base response structure needed


# Get all fridge items endpoint schemas
class GetAllFridgeItemsRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetAllFridgeItemsResponse(BaseResponse):
    fridge_items: List[FridgeItemData] = Field([], alias="fridgeItems")


# Get specific fridge item endpoint schemas
class GetSpecificFridgeItemRequest(BaseModel):
    pass  # No body parameters needed, foodName is in URL path


class GetSpecificFridgeItemResponse(BaseResponse):
    item: FridgeItemData
