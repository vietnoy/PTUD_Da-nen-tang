"""Authentication-related schemas for login, register, token refresh, and email verification."""
from pydantic import BaseModel, EmailStr, Field

from .base import BaseResponse, UserData


# Login endpoint schemas
class LoginRequest(BaseModel):
    """Request body for user login."""
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseResponse):
    """Response after successful login."""
    user: UserData
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")


# Register endpoint schemas
class RegisterRequest(BaseModel):
    """Request body for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1)
    language: str = Field(..., min_length=2, max_length=5)
    timezone: int = Field(..., ge=-12, le=14)
    device_id: str = Field(..., alias="deviceId")
    user_name: str = Field(..., min_length=4)


class RegisterResponse(BaseResponse):
    """Response after successful registration."""
    user: UserData
    confirm_token: str = Field(..., alias="confirmToken")


# Verify email endpoint schemas
class VerifyEmailRequest(BaseModel):
    """Request body for email verification."""
    code: str = Field(..., min_length=6, max_length=6)
    confirm_token: str = Field(...)


class VerifyEmailResponse(BaseResponse):
    """Response after successful email verification."""
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")


# Send verification code endpoint schemas
class SendVerificationCodeRequest(BaseModel):
    """Request body for sending email verification code."""
    email: EmailStr


class SendVerificationCodeResponse(BaseResponse):
    """Response with confirmation token for verification."""
    confirm_token: str = Field(..., alias="confirmToken")


# Logout endpoint schemas
class LogoutRequest(BaseModel):
    """Request body for logout (empty, uses Authorization header)."""
    pass


class LogoutResponse(BaseResponse):
    """Response after successful logout."""
    pass


# Refresh token endpoint schemas
class RefreshTokenRequest(BaseModel):
    """Request body for refreshing access token."""
    refresh_token: str = Field(..., alias="refreshToken")


class RefreshTokenResponse(BaseResponse):
    """Response with new access and refresh tokens."""
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")


# Legacy aliases for backward compatibility (if needed)
RefreshToken = RefreshTokenRequest
TokenResponse = RefreshTokenResponse
