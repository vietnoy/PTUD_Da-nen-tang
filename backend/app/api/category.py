from app.core.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas import (
    AddCategoryRequest,
    AddCategoryResponse,
    DeleteCategoryRequest,
    DeleteCategoryResponse,
    EditCategoryRequest,
    EditCategoryResponse,
    GetAllCategoriesResponse,
)
from ..services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Food Category"])


@router.post("/", response_model=AddCategoryResponse)
def add_category(
    category_data: AddCategoryRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a new food category."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to add categories.",
        )
    return CategoryService.add_category(db, category_data)


@router.get("/", response_model=GetAllCategoriesResponse)
def get_all_categories(
    db: Session = Depends(get_db),
):
    """Get all food categories."""
    return CategoryService.get_all_categories(db)


@router.put("/", response_model=EditCategoryResponse)
def edit_category(
    category_data: EditCategoryRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Edit an existing food category."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to edit categories.",
        )
    return CategoryService.edit_category(db, category_data)


@router.delete("/", response_model=DeleteCategoryResponse)
def delete_category(
    category_data: DeleteCategoryRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a food category."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to delete categories.",
        )
    return CategoryService.delete_category(db, category_data)
