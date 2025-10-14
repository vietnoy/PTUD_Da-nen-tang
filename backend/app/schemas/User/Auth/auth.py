from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# User data structure for responses
class UserData(BaseModel):
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


# Login endpoint schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseResponse):
    user: UserData
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")


# Register endpoint schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1)
    language: str = Field(..., min_length=2, max_length=5)
    timezone: int = Field(..., ge=-12, le=14)
    device_id: str = Field(..., alias="deviceId")


class RegisterResponse(BaseResponse):
    user: UserData
    confirm_token: str = Field(..., alias="confirmToken")


# Logout endpoint schemas
class LogoutRequest(BaseModel):
    pass  # No body parameters needed, uses Authorization header


class LogoutResponse(BaseResponse):
    pass  # Only base response structure needed


# Refresh token endpoint schemas
class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., alias="refreshToken")


class RefreshTokenResponse(BaseResponse):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")


# Send verification code endpoint schemas
class SendVerificationCodeRequest(BaseModel):
    email: EmailStr


class SendVerificationCodeResponse(BaseResponse):
    confirm_token: str = Field(..., alias="confirmToken")


# Verify email endpoint schemas
class VerifyEmailRequest(BaseModel):
    code: str = Field(..., min_length=1)
    token: str = Field(..., min_length=1)


class VerifyEmailResponse(BaseResponse):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")
