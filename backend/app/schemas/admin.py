"""Admin-related Pydantic schemas."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from .base import ResultMessage


# ==================== ADMIN LOGIN ====================

class AdminLoginRequest(BaseModel):
    """Admin login request."""
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    """Admin login response."""
    resultMessage: ResultMessage
    resultCode: str
    accessToken: str
    username: str


# ==================== USER MANAGEMENT ====================

class AdminUserData(BaseModel):
    """Admin user data model."""
    id: int
    email: str
    name: str
    username: Optional[str] = None
    language: str = "en"
    timezone: int = 0
    is_activated: bool = True
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdminUserListResponse(BaseModel):
    """Admin user list response."""
    resultMessage: ResultMessage
    resultCode: str
    users: List[AdminUserData]
    total: int


class AdminUserCreateRequest(BaseModel):
    """Admin user create request."""
    email: EmailStr
    password: str
    name: str
    username: Optional[str] = None
    language: Optional[str] = "en"
    timezone: Optional[int] = 0
    is_activated: Optional[bool] = True
    is_verified: Optional[bool] = False


class AdminUserCreateResponse(BaseModel):
    """Admin user create response."""
    resultMessage: ResultMessage
    resultCode: str
    user: AdminUserData


class AdminUserUpdateRequest(BaseModel):
    """Admin user update request."""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[int] = None
    is_activated: Optional[bool] = None
    is_verified: Optional[bool] = None


class AdminUserUpdateResponse(BaseModel):
    """Admin user update response."""
    resultMessage: ResultMessage
    resultCode: str
    user: AdminUserData


class AdminUserDeleteResponse(BaseModel):
    """Admin user delete response."""
    resultMessage: ResultMessage
    resultCode: str


# ==================== UNIT MANAGEMENT ====================

class AdminUnitData(BaseModel):
    """Admin unit data model."""
    id: int
    name: str
    type: str
    conversion_factor: Optional[Decimal] = None
    base_unit_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUnitListResponse(BaseModel):
    """Admin unit list response."""
    resultMessage: ResultMessage
    resultCode: str
    units: List[AdminUnitData]
    total: int


class AdminUnitCreateRequest(BaseModel):
    """Admin unit create request."""
    name: str
    type: str
    conversion_factor: Optional[Decimal] = None
    base_unit_id: Optional[int] = None


class AdminUnitCreateResponse(BaseModel):
    """Admin unit create response."""
    resultMessage: ResultMessage
    resultCode: str
    unit: AdminUnitData


class AdminUnitUpdateRequest(BaseModel):
    """Admin unit update request."""
    name: Optional[str] = None
    type: Optional[str] = None
    conversion_factor: Optional[Decimal] = None
    base_unit_id: Optional[int] = None


class AdminUnitUpdateResponse(BaseModel):
    """Admin unit update response."""
    resultMessage: ResultMessage
    resultCode: str
    unit: AdminUnitData


class AdminUnitDeleteResponse(BaseModel):
    """Admin unit delete response."""
    resultMessage: ResultMessage
    resultCode: str


# ==================== CATEGORY MANAGEMENT ====================

class AdminCategoryData(BaseModel):
    """Admin category data model."""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AdminCategoryListResponse(BaseModel):
    """Admin category list response."""
    resultMessage: ResultMessage
    resultCode: str
    categories: List[AdminCategoryData]
    total: int


class AdminCategoryCreateRequest(BaseModel):
    """Admin category create request."""
    name: str
    description: Optional[str] = None


class AdminCategoryCreateResponse(BaseModel):
    """Admin category create response."""
    resultMessage: ResultMessage
    resultCode: str
    category: AdminCategoryData


class AdminCategoryUpdateRequest(BaseModel):
    """Admin category update request."""
    name: Optional[str] = None
    description: Optional[str] = None


class AdminCategoryUpdateResponse(BaseModel):
    """Admin category update response."""
    resultMessage: ResultMessage
    resultCode: str
    category: AdminCategoryData


class AdminCategoryDeleteResponse(BaseModel):
    """Admin category delete response."""
    resultMessage: ResultMessage
    resultCode: str
