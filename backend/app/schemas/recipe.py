from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseResponse


class RecipeData(BaseModel):
    id: int
    name: str
    description: str
    html_content: str = Field(..., alias="htmlContent")
    food_id: int | None = Field(None, alias="foodId")
    food_name: str | None = Field(None, alias="foodName")
    group_id: int = Field(..., alias="groupId")
    prep_time_minutes: int | None = Field(None, alias="prepTimeMinutes")
    cook_time_minutes: int | None = Field(None, alias="cookTimeMinutes")
    servings: int | None = None
    difficulty: str | None = None
    image_url: str | None = Field(None, alias="imageUrl")
    is_public: bool = Field(..., alias="isPublic")
    created_by: int = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CreateRecipeResponse(BaseResponse):
    recipe: RecipeData

    model_config = {"by_alias": True, "populate_by_name": True}


class GetRecipesRequest(BaseModel):
    pass


class GetRecipesResponse(BaseResponse):
    recipes: list[RecipeData]

    model_config = {"by_alias": True, "populate_by_name": True}


class GetRecipeByIdRequest(BaseModel):
    id: int = Field(..., gt=0)


class GetRecipeByIdResponse(BaseResponse):
    recipe: RecipeData

    model_config = {"by_alias": True, "populate_by_name": True}


class UpdateRecipeResponse(BaseResponse):
    recipe: RecipeData

    model_config = {"by_alias": True, "populate_by_name": True}


class DeleteRecipeRequest(BaseModel):
    id: int = Field(..., gt=0)


class DeleteRecipeResponse(BaseResponse):
    pass
