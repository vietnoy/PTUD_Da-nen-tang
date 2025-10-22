"""Authentication service layer."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from ..models import User
from ..schemas import LoginRequest, RegisterRequest


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: RegisterRequest) -> User:
        """Register a new user."""
        # Check if user already exists
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            name=user_data.name,
            language=user_data.language,
            timezone=user_data.timezone,
            device_id=user_data.device_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, login_data: LoginRequest) -> User | None:
        """Authenticate user with email and password."""
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not user.is_active:
            return None

        if not verify_password(login_data.password, user.password_hash):
            return None

        return user

    @staticmethod
    def create_tokens(user: User) -> dict[str, str]:
        """Create access and refresh tokens for user."""
        access_token = create_access_token({"sub": str(user.id), "email": user.email})
        refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
