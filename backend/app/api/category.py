"""Category-related API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.deps import get_current_user
from ..models import Category, User
from ..schemas.base import ResultMessage
from ..schemas.category import (
    CategoryData,
    CreateCategoryRequest,
    CreateCategoryResponse,
    DeleteCategoryByNameRequest,
    DeleteCategoryByNameResponse,
    EditCategoryByNameRequest,
    EditCategoryByNameResponse,
    GetAllCategoriesResponse,
)
from ..utils.resultCode import ResultCode
from .core.database import get_db

router = APIRouter(prefix="/category", tags=["Categories"])


@router.post(
    "/", response_model=CreateCategoryResponse, status_code=status.HTTP_201_CREATED
)
def create_category(
    request: CreateCategoryRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.name == request.name).first()
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )
    new_category = Category(
        name=request.name,
        description=request.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return CreateCategoryResponse(
        category=CategoryData.model_validate(new_category),
        resultCode=ResultCode.SUCCESS_CATEGORY_CREATED.value[0],
        resultMessage=ResultMessage(
            en="Category created successfully",
            vn=ResultCode.SUCCESS_CATEGORY_CREATED.value[1],
        ),
    )


@router.get("/", response_model=GetAllCategoriesResponse)
def get_all_categories(
    db: Session = Depends(get_db),
):
    categories = db.query(Category).all()
    return GetAllCategoriesResponse(
        categories=[CategoryData.model_validate(cat) for cat in categories],
        resultCode=ResultCode.SUCCESS_CATEGORIES_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Categories fetched successfully",
            vn=ResultCode.SUCCESS_CATEGORIES_FETCHED.value[1],
        ),
    )


@router.put("/", response_model=EditCategoryByNameResponse)
def edit_category_by_name(
    request: EditCategoryByNameRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.name == request.old_name).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    category.name = request.new_name
    category.description = request.description
    db.commit()
    db.refresh(category)
    return EditCategoryByNameResponse(
        category=CategoryData.model_validate(category),
        resultCode=ResultCode.SUCCESS_CATEGORY_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Category edited successfully",
            vn=ResultCode.SUCCESS_CATEGORY_UPDATED.value[1],
        ),
    )


@router.delete("/", response_model=DeleteCategoryByNameResponse)
def delete_category_by_name(
    request: DeleteCategoryByNameRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.name == request.name).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    db.delete(category)
    db.commit()
    return DeleteCategoryByNameResponse(
        resultCode=ResultCode.SUCCESS_CATEGORY_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Category deleted successfully",
            vn=ResultCode.SUCCESS_CATEGORY_DELETED.value[1],
        ),
    )


__all__ = ["router"]
