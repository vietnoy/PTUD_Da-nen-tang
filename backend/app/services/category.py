"""Service layer for managing categories."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import Category
from ..schemas.Admin.FoodCategory.foodCategory import (
    AddCategoryRequest,
    AddCategoryResponse,
    BaseResponse,
    CategoryData,
    DeleteCategoryRequest,
    DeleteCategoryResponse,
    EditCategoryRequest,
    EditCategoryResponse,
    GetAllCategoriesRequest,
    GetAllCategoriesResponse,
    ResultMessage,
)
from ..utils.responseCodeEnums import ResponseCode


class CategoryService:
    """Service class for managing food categories."""

    @staticmethod
    def add_category(
        db: Session, category_data: AddCategoryRequest
    ) -> AddCategoryResponse:
        """Add a new food category."""
        existing_category = (
            db.query(Category).filter(Category.name == category_data.name).first()
        )
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BaseResponse(
                    resultMessage=ResultMessage(
                        en="Category with this name already exists",
                        vn=ResponseCode.CATEGORY_NAME_EXISTS.value[1],
                    ),
                    resultCode=ResponseCode.CATEGORY_NAME_EXISTS.value[0],
                ),
            )

        new_category = Category(name=category_data.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return AddCategoryResponse(
            unit=CategoryData(
                id=new_category.id,
                name=new_category.name,
                createdAt=new_category.created_at,
                updatedAt=new_category.updated_at,
            ),
            resultMessage=ResultMessage(
                en="Category added successfully",
                vn=ResponseCode.CREATE_CATEGORY_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.CREATE_CATEGORY_SUCCESS.value[0],
        )

    @staticmethod
    def get_all_categories(db: Session) -> GetAllCategoriesResponse:
        """Retrieve all food categories."""
        categories = db.query(Category).all()
        category_list = [
            CategoryData(
                id=category.id,
                name=category.name,
                createdAt=category.created_at,
                updatedAt=category.updated_at,
            )
            for category in categories
        ]

        return GetAllCategoriesResponse(
            categories=category_list,
            resultMessage=ResultMessage(
                en="Categories retrieved successfully",
                vn=ResponseCode.GET_CATEGORIES_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.GET_CATEGORIES_SUCCESS.value[0],
        )

    @staticmethod
    def edit_category(
        db: Session, category_data: EditCategoryRequest
    ) -> EditCategoryResponse:
        """Edit an existing food category."""
        category = (
            db.query(Category).filter(Category.name == category_data.old_name).first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BaseResponse(
                    resultMessage=ResultMessage(
                        en="Category not found",
                        vn=ResponseCode.CATEGORY_NOT_FOUND_138.value[1],
                    ),
                    resultCode=ResponseCode.CATEGORY_NOT_FOUND_138.value[0],
                ),
            )

        category.name = category_data.new_name
        db.commit()
        db.refresh(category)

        return EditCategoryResponse(
            resultMessage=ResultMessage(
                en="Category updated successfully",
                vn=ResponseCode.UPDATE_CATEGORY_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.UPDATE_CATEGORY_SUCCESS.value[0],
        )

    @staticmethod
    def delete_category(
        db: Session, category_data: DeleteCategoryRequest
    ) -> DeleteCategoryResponse:
        """Delete a food category."""
        category = (
            db.query(Category).filter(Category.name == category_data.name).first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BaseResponse(
                    resultMessage=ResultMessage(
                        en="Category not found",
                        vn=ResponseCode.CATEGORY_NOT_FOUND_138.value[1],
                    ),
                    resultCode=ResponseCode.CATEGORY_NOT_FOUND_138.value[0],
                ),
            )

        db.delete(category)
        db.commit()

        return DeleteCategoryResponse(
            resultMessage=ResultMessage(
                en="Category deleted successfully",
                vn=ResponseCode.DELETE_CATEGORY_SUCCESS.value[1],
            ),
            resultCode=ResponseCode.DELETE_CATEGORY_SUCCESS.value[0],
        )
