"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import verify_token, create_access_token
from ..core.config import settings
from ..schemas.auth import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
    RefreshToken, TokenResponse,
    VerifyEmailRequest, VerifyEmailResponse,
    SendVerificationCodeRequest, SendVerificationCodeResponse,
    LogoutResponse
)
from ..schemas.base import UserData, ResultMessage
from ..services.auth import AuthService
from ..models import User

import redis

router = APIRouter(prefix="/auth", tags=["Authentication"])

# get the redis client
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


@router.post("/register", response_model=RegisterResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    user = AuthService.register_user(db, user_data)

    confirm_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "type": "confirm"
    })

    # send code to verify email
    AuthService.send_verification_code(user)

    return RegisterResponse(
        resultMessage=ResultMessage(en="Registration successful", vn="Đăng ký thành công"),
        resultCode="00035",
        user=UserData.model_validate(user),
        confirmToken=confirm_token
    )


@router.post("/verify-email", response_model=VerifyEmailResponse)
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    """Verify a new user email"""

    confirm_token = request.confirm_token

    payload = verify_token(confirm_token, "confirm")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    stored_code = redis_client.get(f"otp:{user.id}")

    if not stored_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP code expired or not found"
        )

    if stored_code == request.code:
        user.is_verified = True
        db.commit()
        db.refresh(user)

        tokens = AuthService.create_tokens(user)

        redis_client.delete(f"otp:{user.id}")

        return VerifyEmailResponse(
            resultMessage=ResultMessage(
                en="Your email has been verified successfully",
                vn="Địa chỉ email của bạn đã được xác minh thành công"
            ),
            resultCode="00058",
            accessToken=tokens["access_token"],
            refreshToken=tokens["refresh_token"],
            groupId=user.belongs_to_group_admin_id
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect OTP code"
        )


@router.post("/send-verification-code", response_model=SendVerificationCodeResponse)
def send_verification_code(request: SendVerificationCodeRequest, db: Session = Depends(get_db)):
    """Send or resend verification code"""

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    AuthService.send_verification_code(user)

    confirm_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "type": "confirm"
    })

    return SendVerificationCodeResponse(
        resultMessage=ResultMessage(
            en="Code has been sent to your email successfully",
            vn="Mã đã được gửi đến email của bạn thành công"
        ),
        resultCode="00048",
        confirmToken=confirm_token
    )


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return tokens."""
    user = AuthService.authenticate_user(db, login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    tokens = AuthService.create_tokens(user)

    return LoginResponse(
        resultMessage=ResultMessage(
            en="You have successfully logged in",
            vn="Bạn đã đăng nhập thành công"
        ),
        resultCode="00047",
        user=UserData.model_validate(user),
        accessToken=tokens["access_token"],
        refreshToken=tokens["refresh_token"],
        groupId=user.belongs_to_group_admin_id
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token_data: RefreshToken, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    payload = verify_token(token_data.refresh_token, "refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Verify user still exists and is active
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    tokens = AuthService.create_tokens(user)

    return TokenResponse(
        resultMessage=ResultMessage(
            en="Token has been refreshed successfully",
            vn="Token đã được làm mới thành công"
        ),
        resultCode="00065",
        accessToken=tokens["access_token"],
        refreshToken=tokens["refresh_token"]
    )


@router.post("/logout", response_model=LogoutResponse)
def logout():
    """Logout user (client should discard tokens)."""
    return LogoutResponse(
        resultMessage=ResultMessage(
            en="Logout successful",
            vn="Đăng xuất thành công"
        ),
        resultCode="00050"
    )
