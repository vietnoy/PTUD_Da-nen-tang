"""Common base schemas shared across the application."""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ResultMessage(BaseModel):
    """Result message structure in multiple languages."""
    en: str
    vn: str


class BaseResponse(BaseModel):
    """Base response structure for all API responses."""
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


class UserData(BaseModel):
    """User data structure for responses."""
    id: int
    email: str
    password: str = ""  # Usually empty string in responses for security
    username: Optional[str] = None
    name: str
    type: Optional[str] = None
    language: str
    gender: Optional[str] = None
    country_code: Optional[str] = Field(None, alias="countryCode")
    timezone: int
    birth_date: Optional[date] = Field(None, alias="birthDate")
    photo_url: Optional[str] = Field(None, alias="photoUrl")
    is_activated: bool = Field(..., alias="isActivated")
    is_verified: bool = Field(..., alias="isVerified")
    device_id: Optional[str] = Field(None, alias="deviceId")
    belongs_to_group_admin_id: int = Field(0, alias="belongsToGroupAdminId")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
