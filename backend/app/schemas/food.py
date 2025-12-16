from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseResponse


# Food data schema
class FoodData(BaseModel):
    """Food data structure for responses"""

    id: int
    name: str
    category_name: str | None = None
    unit_name: str | None = None
    category_id: int | None = None
    unit_id: int | None = None
    group_id: int | None = None
    description: str | None = None
    image_url: str | None = None
    brand: str | None = None
    default_shelf_life_days: int | None = None
    storage_instructions: str | None = None
    created_by: int
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


# Create food endpoint schemas
class CreateFoodRequest(BaseModel):
    """Request body for creating a new food item."""

    name: str = Field(..., min_length=1, max_length=100)
    category_name: str | None = None
    unit_name: str | None = None
    group_id: int | None = None
    description: str | None = Field(None, max_length=500)
    image_url: str | None = Field(None, max_length=500)
    brand: str | None = Field(None, max_length=50)
    default_shelf_life_days: int | None = None
    storage_instructions: str | None = Field(None, max_length=500)


class CreateFoodResponse(BaseResponse):
    """Response after successful food creation."""

    food: FoodData


# Get foods endpoint schemas
class GetAllFoodsRequest(BaseModel):
    """Request for getting all foods (empty body)."""

    pass


class GetAllFoodsResponse(BaseResponse):
    """Response for getting all foods."""

    foods: list[FoodData]


# Edit food endpoint schemas
class EditFoodByNameRequest(BaseModel):
    """Request body for editing a food item by name."""

    food_name: str = Field(..., alias="foodName")
    name: str | None = Field(None, min_length=1, max_length=100)
    category_name: str | None = None
    unit_name: str | None = None
    group_id: int | None = None
    description: str | None = Field(None, max_length=500)
    image_url: str | None = Field(None, max_length=500)
    brand: str | None = Field(None, max_length=50)
    default_shelf_life_days: int | None = None
    storage_instructions: str | None = Field(None, max_length=500)

    model_config = {"populate_by_name": True}


class EditFoodByNameResponse(BaseResponse):
    """Response after successful food editing."""

    food: FoodData


# Delete food endpoint schemas
class DeleteFoodByNameRequest(BaseModel):
    """Request body for deleting a food item by name."""

    food_name: str = Field(..., alias="foodName")

    model_config = {"populate_by_name": True}


class DeleteFoodByNameResponse(BaseResponse):
    """Response after successful food deletion."""

    pass


class GetFoodsByNamesRequest(BaseModel):
    """Request body for getting foods by a list of IDs."""

    food_names: list[str] = Field(..., alias="foodNames")

    model_config = {"populate_by_name": True}


class GetFoodsByNamesResponse(BaseResponse):
    """Response for getting foods by a list of IDs."""

    foods: list[FoodData]


__all__ = [
    "FoodData",
    "CreateFoodRequest",
    "CreateFoodResponse",
    "GetAllFoodsRequest",
    "GetAllFoodsResponse",
    "EditFoodByNameRequest",
    "EditFoodByNameResponse",
    "DeleteFoodByNameRequest",
    "DeleteFoodByNameResponse",
    "GetFoodsByNamesRequest",
    "GetFoodsByNamesResponse",
]
