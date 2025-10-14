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


# Food data structure (for nested Food object in meal plans)
class MealPlanFoodData(BaseModel):
    id: int
    name: str
    image_url: str = Field(..., alias="imageUrl")
    type: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    food_category_id: int = Field(..., alias="FoodCategoryId")
    user_id: int = Field(..., alias="UserId")
    unit_of_measurement_id: int = Field(..., alias="UnitOfMeasurementId")


# Meal plan data structure
class MealPlanData(BaseModel):
    id: int
    name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str  # Example: "NOT_PASS_YET"
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    food_id: int = Field(..., alias="FoodId")
    user_id: int = Field(..., alias="UserId")
    food: Optional[MealPlanFoodData] = Field(None, alias="Food")  # Nested food object


# Create meal plan endpoint schemas
class CreateMealPlanRequest(BaseModel):
    food_name: str = Field(..., alias="foodName", min_length=1)
    timestamp: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class CreateMealPlanResponse(BaseResponse):
    new_plan: MealPlanData = Field(..., alias="newPlan")


# Delete meal plan endpoint schemas
class DeleteMealPlanRequest(BaseModel):
    plan_id: str = Field(..., alias="planId")


class DeleteMealPlanResponse(BaseResponse):
    pass  # Only base response structure needed


# Update meal plan endpoint schemas
class UpdateMealPlanRequest(BaseModel):
    plan_id: str = Field(..., alias="planId")
    new_food_name: str = Field(..., alias="newFoodName", min_length=1)
    new_name: str = Field(..., alias="newName", min_length=1)


class UpdateMealPlanResponse(BaseResponse):
    plan: MealPlanData


# Get meal plans by date endpoint schemas
class GetMealPlansByDateRequest(BaseModel):
    date: Optional[str] = (
        None  # Query parameter - format could be "1/14/2024" or similar
    )
    # You can also add other filtering options like:
    # start_date: Optional[str] = Field(None, alias="startDate")
    # end_date: Optional[str] = Field(None, alias="endDate")


class GetMealPlansByDateResponse(BaseResponse):
    plans: List[MealPlanData] = []
