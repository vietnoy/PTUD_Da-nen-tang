from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# Change password endpoint schemas
class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", min_length=1)
    new_password: str = Field(..., alias="newPassword", min_length=6)


class ChangePasswordResponse(BaseResponse):
    pass  # Only base response structure needed


# Edit user endpoint schemas
# Note: For file uploads, FastAPI uses Form() and File() in the endpoint directly
# This is for the text fields in the form-data request
class EditUserRequest(BaseModel):
    username: Optional[str] = None
    # Note: image file is handled separately in FastAPI endpoint using File() parameter


class EditUserResponse(BaseResponse):
    photo_url: Optional[str] = Field(None, alias="photoUrl")


# Save notification token endpoint schemas
class SaveNotificationTokenRequest(BaseModel):
    token: str = Field(..., min_length=1)


class SaveNotificationTokenResponse(BaseResponse):
    pass  # Only base response structure needed
