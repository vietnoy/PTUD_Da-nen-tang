from typing import Optional

from pydantic import BaseModel, Field

from .Auth.auth import UserData


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# Get user endpoint schemas
class GetUserRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request with Authorization header


class GetUserResponse(BaseResponse):
    user: UserData


# Delete user endpoint schemas
class DeleteUserRequest(BaseModel):
    pass  # No body parameters needed based on the documentation


class DeleteUserResponse(BaseResponse):
    pass  # Only base response structure needed
