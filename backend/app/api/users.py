"""User management API routes."""
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..schemas.user import UserResponse, EditUserResponse, ChangePasswordRequest, ChangePasswordResponse
from ..models import User
from ..core import storage
from ..services import user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user

@router.put("/me", response_model=EditUserResponse)
def edit_current_user_profile(
    file: UploadFile = File(None), 
    username: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    """Edit current user profile."""

    # User can edit many fields such as: username or language or anything 
    # (except for password cause it has its own api for password changing)
    if username:
        current_user.username = username
    
    photo_url = None
    if file:
        try:
            client = storage.get_minio_client()
        except Exception as e:
            print(f"Error while creating minio client: {e}")

        response = storage.upload_file(client, file, f"avatar/{current_user.id}", current_user.avatar_url)
        current_user.avatar_url = response["public_url"]
        photo_url = response["public_url"]
    
    db.commit()

    return EditUserResponse(
        photoUrl=photo_url
    )

@router.post("/change-password", response_model=ChangePasswordResponse)
def change_password(request: ChangePasswordRequest,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    

    hashed_password = user.validate_password(request.old_password, request.new_password, current_user)

    current_user.password_hash = hashed_password

    db.commit()

    return ChangePasswordResponse()

@router.delete("/me")
def remove_current_user_profile(current_user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):

    db.delete(current_user)

    db.commit()

    return {"message": "User deleted successfully"}