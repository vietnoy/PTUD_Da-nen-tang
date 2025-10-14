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


# Food data structure (for nested Food object in recipes)
class RecipeFoodData(BaseModel):
    id: int
    name: str
    image_url: str = Field(..., alias="imageUrl")
    type: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    food_category_id: int = Field(..., alias="FoodCategoryId")
    user_id: int = Field(..., alias="UserId")
    unit_of_measurement_id: int = Field(..., alias="UnitOfMeasurementId")


# Recipe data structure
class RecipeData(BaseModel):
    id: int
    name: str
    description: str
    html_content: str = Field(..., alias="htmlContent")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    food_id: int = Field(..., alias="FoodId")
    food: Optional[RecipeFoodData] = Field(None, alias="Food")  # Nested food object


# Create recipe endpoint schemas
class CreateRecipeRequest(BaseModel):
    food_name: str = Field(..., alias="foodName", min_length=1)
    name: str = Field(..., min_length=1)
    html_content: str = Field(..., alias="htmlContent")
    description: str = Field(...)


class CreateRecipeResponse(BaseResponse):
    new_recipe: RecipeData = Field(..., alias="newRecipe")


# Update recipe endpoint schemas
class UpdateRecipeRequest(BaseModel):
    recipe_id: str = Field(..., alias="recipeId")
    new_html_content: str = Field(..., alias="newHtmlContent")
    new_description: str = Field(..., alias="newDescription")
    new_food_name: str = Field(..., alias="newFoodName", min_length=1)
    new_name: str = Field(..., alias="newName", min_length=1)


class UpdateRecipeResponse(BaseResponse):
    recipe: RecipeData


# Delete recipe endpoint schemas
class DeleteRecipeRequest(BaseModel):
    recipe_id: str = Field(..., alias="recipeId")


class DeleteRecipeResponse(BaseResponse):
    pass  # Only base response structure needed


# Get recipes by food ID endpoint schemas
class GetRecipesByFoodIdRequest(BaseModel):
    food_id: Optional[int] = Field(None, alias="foodId")  # Query parameter


class GetRecipesByFoodIdResponse(BaseResponse):
    recipes: List[RecipeData] = []
