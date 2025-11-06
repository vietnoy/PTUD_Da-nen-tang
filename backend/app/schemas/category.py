from pydantic import BaseModel, Field

from .base import BaseResponse


# Category data schema
class CategoryData(BaseModel):
    """Category data structure for responses."""

    id: int
    name: str
    description: str | None = None
    created_at: str = Field(..., alias="createdAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


# Create category endpoint schemas
class CreateCategoryRequest(BaseModel):
    """Request body for creating a new category."""

    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=500)


class CreateCategoryResponse(BaseResponse):
    """Response after successful category creation."""

    category: CategoryData


# Get categories endpoint schemas
class GetAllCategoriesRequest(BaseModel):
    """Request for getting all categories (empty body)."""

    pass


class GetAllCategoriesResponse(BaseResponse):
    """Response for getting all categories."""

    categories: list[CategoryData]


# Edit category endpoint schemas
class EditCategoryByNameRequest(BaseModel):
    """Request body for editing a category by name."""

    old_name: str = Field(..., min_length=1, max_length=50)
    new_name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=500)


class EditCategoryByNameResponse(BaseResponse):
    """Response after successful category editing."""

    category: CategoryData


# Delete category endpoint schemas
class DeleteCategoryByNameRequest(BaseModel):
    """Request body for deleting a category by name."""

    name: str = Field(..., min_length=1, max_length=50)


class DeleteCategoryByNameResponse(BaseResponse):
    """Response after successful category deletion."""

    pass
