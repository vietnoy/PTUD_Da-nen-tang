"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import verify_token
from ..models import User
from ..schemas import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    RegisterResponse,
    ResultMessage,
)
from ..services.auth import AuthService
from ..utils.responseCodeEnums import ResponseCode

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    user = AuthService.register_user(db, user_data)
    tokens = AuthService.create_tokens(user)

    return RegisterResponse(
        user=user,
        confirmToken=tokens["access_token"],  # Using access_token as confirm_token
        resultMessage=ResultMessage(
            en="User registered successfully",
            vn=ResponseCode.REGISTRATION_SUCCESS.value[1],
        ),
        resultCode=ResponseCode.REGISTRATION_SUCCESS.value[0],
    )


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return tokens."""
    user = AuthService.authenticate_user(db, login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    tokens = AuthService.create_tokens(user)

    return LoginResponse(
        user=user,
        accessToken=tokens["access_token"],
        refreshToken=tokens["refresh_token"],
        resultMessage=ResultMessage(
            en="Login successful", vn=ResponseCode.LOGIN_SUCCESS.value[1]
        ),
        resultCode=ResponseCode.LOGIN_SUCCESS.value[0],
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    payload = verify_token(token_data.refresh_token, "refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    # Verify user still exists and is active

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    tokens = AuthService.create_tokens(user)

    return RefreshTokenResponse(
        accessToken=tokens["access_token"],
        refreshToken=tokens["refresh_token"],
        resultMessage=ResultMessage(
            en="Token refreshed successfully",
            vn=ResponseCode.TOKEN_REFRESH_SUCCESS.value[1],
        ),
        resultCode=ResponseCode.TOKEN_REFRESH_SUCCESS.value[0],
    )


@router.post("/logout", response_model=LogoutResponse)
def logout():
    """Logout user (client should discard tokens)."""
    return LogoutResponse(
        resultMessage=ResultMessage(
            en="Successfully logged out", vn=ResponseCode.LOGOUT_SUCCESS.value[1]
        ),
        resultCode=ResponseCode.LOGOUT_SUCCESS.value[0],
    )
