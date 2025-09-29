"""Authentication schemas for request/response validation."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    username: str | None
    avatar_url: str | None
    language: str
    timezone: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"