"""Admin API routes for managing users, units, and categories."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.config import settings
from ..core.security import create_access_token
from ..models import User, Unit, Category
from ..schemas.base import ResultMessage
from ..schemas.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminUserData,
    AdminUserListResponse,
    AdminUserCreateRequest,
    AdminUserCreateResponse,
    AdminUserUpdateRequest,
    AdminUserUpdateResponse,
    AdminUserDeleteResponse,
    AdminUnitData,
    AdminUnitListResponse,
    AdminUnitCreateRequest,
    AdminUnitCreateResponse,
    AdminUnitUpdateRequest,
    AdminUnitUpdateResponse,
    AdminUnitDeleteResponse,
    AdminCategoryData,
    AdminCategoryListResponse,
    AdminCategoryCreateRequest,
    AdminCategoryCreateResponse,
    AdminCategoryUpdateRequest,
    AdminCategoryUpdateResponse,
    AdminCategoryDeleteResponse,
)
from ..core import security

router = APIRouter(prefix="/admin", tags=["Admin"])


def verify_admin(username: str, password: str) -> bool:
    """Verify admin credentials from settings."""
    return (
        username == settings.admin_username
        and password == settings.admin_password
    )


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(request: AdminLoginRequest):
    """Admin login endpoint."""
    if not verify_admin(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )
    
    access_token = create_access_token({
        "sub": "admin",
        "type": "admin"
    })
    
    return AdminLoginResponse(
        resultMessage=ResultMessage(
            en="Admin login successful",
            vn="Đăng nhập admin thành công"
        ),
        resultCode="00100",
        accessToken=access_token,
        username=request.username
    )


# ==================== USER MANAGEMENT ====================

@router.get("/users", response_model=AdminUserListResponse)
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users (Admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    total = db.query(User).count()
    
    return AdminUserListResponse(
        resultMessage=ResultMessage(
            en="Users retrieved successfully",
            vn="Lấy danh sách người dùng thành công"
        ),
        resultCode="00101",
        users=[AdminUserData.model_validate(user) for user in users],
        total=total
    )


@router.get("/users/{user_id}", response_model=AdminUserData)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user by ID (Admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return AdminUserData.model_validate(user)


@router.post("/users", response_model=AdminUserCreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: AdminUserCreateRequest,
    db: Session = Depends(get_db)
):
    """Create new user (Admin only)."""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if request.username:
        existing_username = db.query(User).filter(User.username == request.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Hash password
    password_hash = security.hash_password(request.password)
    
    new_user = User(
        email=request.email,
        password_hash=password_hash,
        name=request.name,
        username=request.username,
        language=request.language or "en",
        timezone=request.timezone or 0,
        is_activated=request.is_activated if request.is_activated is not None else True,
        is_verified=request.is_verified if request.is_verified is not None else False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return AdminUserCreateResponse(
        resultMessage=ResultMessage(
            en="User created successfully",
            vn="Tạo người dùng thành công"
        ),
        resultCode="00102",
        user=AdminUserData.model_validate(new_user)
    )


@router.put("/users/{user_id}", response_model=AdminUserUpdateResponse)
def update_user(
    user_id: int,
    request: AdminUserUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update user (Admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields if provided
    if request.email is not None:
        # Check if new email already exists
        existing_user = db.query(User).filter(User.email == request.email, User.id != user_id).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user.email = request.email
    
    if request.name is not None:
        user.name = request.name
    
    if request.username is not None:
        # Check if new username already exists
        existing_username = db.query(User).filter(User.username == request.username, User.id != user_id).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        user.username = request.username
    
    if request.password is not None:
        user.password_hash = security.hash_password(request.password)
    
    if request.language is not None:
        user.language = request.language
    
    if request.timezone is not None:
        user.timezone = request.timezone
    
    if request.is_activated is not None:
        user.is_activated = request.is_activated
    
    if request.is_verified is not None:
        user.is_verified = request.is_verified
    
    db.commit()
    db.refresh(user)
    
    return AdminUserUpdateResponse(
        resultMessage=ResultMessage(
            en="User updated successfully",
            vn="Cập nhật người dùng thành công"
        ),
        resultCode="00103",
        user=AdminUserData.model_validate(user)
    )


@router.delete("/users/{user_id}", response_model=AdminUserDeleteResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete user (Admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return AdminUserDeleteResponse(
        resultMessage=ResultMessage(
            en="User deleted successfully",
            vn="Xóa người dùng thành công"
        ),
        resultCode="00104"
    )


# ==================== UNIT MANAGEMENT ====================

@router.get("/units", response_model=AdminUnitListResponse)
def get_all_units(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all units (Admin only)."""
    units = db.query(Unit).offset(skip).limit(limit).all()
    total = db.query(Unit).count()
    
    return AdminUnitListResponse(
        resultMessage=ResultMessage(
            en="Units retrieved successfully",
            vn="Lấy danh sách đơn vị thành công"
        ),
        resultCode="00105",
        units=[AdminUnitData.model_validate(unit) for unit in units],
        total=total
    )


@router.get("/units/{unit_id}", response_model=AdminUnitData)
def get_unit_by_id(
    unit_id: int,
    db: Session = Depends(get_db)
):
    """Get unit by ID (Admin only)."""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    return AdminUnitData.model_validate(unit)


@router.post("/units", response_model=AdminUnitCreateResponse, status_code=status.HTTP_201_CREATED)
def create_unit(
    request: AdminUnitCreateRequest,
    db: Session = Depends(get_db)
):
    """Create new unit (Admin only)."""
    # Check if unit name already exists
    existing_unit = db.query(Unit).filter(Unit.name == request.name).first()
    if existing_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit with this name already exists"
        )
    
    if request.type not in ["weight", "volume", "count", "length"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid unit type. Must be one of: weight, volume, count, length"
        )
    
    new_unit = Unit(
        name=request.name,
        type=request.type,
        conversion_factor=request.conversion_factor,
        base_unit_id=request.base_unit_id
    )
    
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    
    return AdminUnitCreateResponse(
        resultMessage=ResultMessage(
            en="Unit created successfully",
            vn="Tạo đơn vị thành công"
        ),
        resultCode="00106",
        unit=AdminUnitData.model_validate(new_unit)
    )


@router.put("/units/{unit_id}", response_model=AdminUnitUpdateResponse)
def update_unit(
    unit_id: int,
    request: AdminUnitUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update unit (Admin only)."""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    
    if request.name is not None:
        # Check if new name already exists
        existing_unit = db.query(Unit).filter(Unit.name == request.name, Unit.id != unit_id).first()
        if existing_unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit with this name already exists"
            )
        unit.name = request.name
    
    if request.type is not None:
        if request.type not in ["weight", "volume", "count", "length"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid unit type. Must be one of: weight, volume, count, length"
            )
        unit.type = request.type
    
    if request.conversion_factor is not None:
        unit.conversion_factor = request.conversion_factor
    
    if request.base_unit_id is not None:
        unit.base_unit_id = request.base_unit_id
    
    db.commit()
    db.refresh(unit)
    
    return AdminUnitUpdateResponse(
        resultMessage=ResultMessage(
            en="Unit updated successfully",
            vn="Cập nhật đơn vị thành công"
        ),
        resultCode="00107",
        unit=AdminUnitData.model_validate(unit)
    )


@router.delete("/units/{unit_id}", response_model=AdminUnitDeleteResponse)
def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db)
):
    """Delete unit (Admin only)."""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    
    db.delete(unit)
    db.commit()
    
    return AdminUnitDeleteResponse(
        resultMessage=ResultMessage(
            en="Unit deleted successfully",
            vn="Xóa đơn vị thành công"
        ),
        resultCode="00108"
    )


# ==================== CATEGORY MANAGEMENT ====================

@router.get("/categories", response_model=AdminCategoryListResponse)
def get_all_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all categories (Admin only)."""
    categories = db.query(Category).offset(skip).limit(limit).all()
    total = db.query(Category).count()
    
    return AdminCategoryListResponse(
        resultMessage=ResultMessage(
            en="Categories retrieved successfully",
            vn="Lấy danh sách danh mục thành công"
        ),
        resultCode="00109",
        categories=[AdminCategoryData.model_validate(category) for category in categories],
        total=total
    )


@router.get("/categories/{category_id}", response_model=AdminCategoryData)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Get category by ID (Admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return AdminCategoryData.model_validate(category)


@router.post("/categories", response_model=AdminCategoryCreateResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    request: AdminCategoryCreateRequest,
    db: Session = Depends(get_db)
):
    """Create new category (Admin only)."""
    # Check if category name already exists
    existing_category = db.query(Category).filter(Category.name == request.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    new_category = Category(
        name=request.name,
        description=request.description
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return AdminCategoryCreateResponse(
        resultMessage=ResultMessage(
            en="Category created successfully",
            vn="Tạo danh mục thành công"
        ),
        resultCode="00110",
        category=AdminCategoryData.model_validate(new_category)
    )


@router.put("/categories/{category_id}", response_model=AdminCategoryUpdateResponse)
def update_category(
    category_id: int,
    request: AdminCategoryUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update category (Admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    if request.name is not None:
        # Check if new name already exists
        existing_category = db.query(Category).filter(Category.name == request.name, Category.id != category_id).first()
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        category.name = request.name
    
    if request.description is not None:
        category.description = request.description
    
    db.commit()
    db.refresh(category)
    
    return AdminCategoryUpdateResponse(
        resultMessage=ResultMessage(
            en="Category updated successfully",
            vn="Cập nhật danh mục thành công"
        ),
        resultCode="00111",
        category=AdminCategoryData.model_validate(category)
    )


@router.delete("/categories/{category_id}", response_model=AdminCategoryDeleteResponse)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete category (Admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return AdminCategoryDeleteResponse(
        resultMessage=ResultMessage(
            en="Category deleted successfully",
            vn="Xóa danh mục thành công"
        ),
        resultCode="00112"
    )
