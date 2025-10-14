from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# User data structure for group member responses
class GroupMemberData(BaseModel):
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


# Create group endpoint schemas
class CreateGroupRequest(BaseModel):
    pass  # No body parameters needed based on the documentation


class CreateGroupResponse(BaseResponse):
    admin_id: int = Field(..., alias="adminId")


# Add member endpoint schemas
class AddMemberRequest(BaseModel):
    username: str = Field(..., min_length=1)


class AddMemberResponse(BaseResponse):
    pass  # Only base response structure needed


# Delete member endpoint schemas
class DeleteMemberRequest(BaseModel):
    username: str = Field(..., min_length=1)


class DeleteMemberResponse(BaseResponse):
    pass  # Only base response structure needed


# Get group members endpoint schemas
class GetGroupMembersRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetGroupMembersResponse(BaseResponse):
    group_admin: GroupMemberData = Field(..., alias="groupAdmin")
    members: List[GroupMemberData] = []
