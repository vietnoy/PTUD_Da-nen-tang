from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from .base import BaseResponse


class MealPlanData(BaseModel):
    id: int
    food_id: int = Field(..., alias="foodId")
    food_name: str = Field(..., alias="foodName")
    group_id: int = Field(..., alias="groupId")
    meal_type: str = Field(..., alias="mealType")
    meal_date: date = Field(..., alias="mealDate")
    serving_size: Decimal | None = Field(None, alias="servingSize")
    unit_id: int | None = Field(None, alias="unitId")
    unit_name: str | None = Field(None, alias="unitName")
    note: str | None = None
    is_prepared: bool = Field(..., alias="isPrepared")
    prepared_at: datetime | None = Field(None, alias="preparedAt")
    created_by: int = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CreateMealPlanRequest(BaseModel):
    food_name: str = Field(..., min_length=1, max_length=100, alias="foodName")
    meal_type: str = Field(..., min_length=1, max_length=20, alias="mealType")
    meal_date: date = Field(..., alias="mealDate")
    serving_size: Decimal | None = Field(None, gt=0, alias="servingSize")
    unit_name: str | None = Field(None, max_length=20, alias="unitName")
    note: str | None = Field(None, max_length=500)


class CreateMealPlanResponse(BaseResponse):
    meal_plan: MealPlanData = Field(..., alias="mealPlan")

    model_config = {"by_alias": True, "populate_by_name": True}


class GetMealPlansRequest(BaseModel):
    start_date: date | None = Field(None, alias="startDate")
    end_date: date | None = Field(None, alias="endDate")
    meal_type: str | None = Field(None, alias="mealType")


class GetMealPlansResponse(BaseResponse):
    meal_plans: list[MealPlanData] = Field(..., alias="mealPlans")

    model_config = {"by_alias": True, "populate_by_name": True}


class GetMealPlanByIdRequest(BaseModel):
    id: int = Field(..., gt=0)


class GetMealPlanByIdResponse(BaseResponse):
    meal_plan: MealPlanData = Field(..., alias="mealPlan")

    model_config = {"by_alias": True, "populate_by_name": True}


class UpdateMealPlanRequest(BaseModel):
    id: int = Field(..., gt=0)
    new_food_name: str | None = Field(None, min_length=1, max_length=100, alias="newFoodName")
    new_meal_type: str | None = Field(None, min_length=1, max_length=20, alias="newMealType")
    new_meal_date: date | None = Field(None, alias="newMealDate")
    new_serving_size: Decimal | None = Field(None, gt=0, alias="newServingSize")
    is_prepared: bool | None = Field(None, alias="isPrepared")


class UpdateMealPlanResponse(BaseResponse):
    meal_plan: MealPlanData = Field(..., alias="mealPlan")

    model_config = {"by_alias": True, "populate_by_name": True}


class DeleteMealPlanRequest(BaseModel):
    id: int = Field(..., gt=0)


class DeleteMealPlanResponse(BaseResponse):
    pass
