"""Authentication service layer."""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import User
from ..models.group import Group, GroupMember
from ..schemas.auth import RegisterRequest, LoginRequest
from ..core.security import hash_password, verify_password, create_access_token, create_refresh_token, generate_otp_code
from ..core.config import settings
from ..workers.celery_app import celery_app

import redis
import secrets
from datetime import timedelta

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: RegisterRequest) -> User:
        """Register a new user."""
        # Check if user already exists
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        if user_data.user_name and db.query(User).filter(User.username == user_data.user_name).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create new user
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            name=user_data.name,
            username=user_data.user_name,
            is_verified=True  # Bỏ qua xác thực email, set True ngay khi đăng ký
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Create a group for the user
        group = Group(
            name=f"{user.name}'s Group",
            owner_id=user.id,
            is_active=True,
            invite_code=secrets.token_urlsafe(4)[:6].upper()
        )
        db.add(group)
        db.commit()
        db.refresh(group)

        # Add user as owner member of the group
        group_member = GroupMember(
            user_id=user.id,
            group_id=group.id,
            role="owner",
            is_active=True
        )
        db.add(group_member)

        # Set user's group
        user.belongs_to_group_admin_id = group.id
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
            "token_type": "bearer"
        }

    @staticmethod
    def send_verification_code(user: User):
        """Create the OTP code and then send to user's email"""
        otp_code = generate_otp_code()

        redis_client.setex(
            f"otp:{user.id}",
            timedelta(minutes=15),
            otp_code
        )

        # add a task to the celery redis queue
        celery_app.send_task(
                'tasks.send_verification_email',
                args=[user.email, otp_code]
        )

        return otp_code
