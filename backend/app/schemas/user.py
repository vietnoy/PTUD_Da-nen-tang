"""User-related schemas for profile management, password changes, and group operations."""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse, UserData


# Get user endpoint schemas
class GetUserRequest(BaseModel):
    """Request for getting user (empty, uses Authorization header)."""
    pass


class GetUserResponse(BaseResponse):
    """Response with user data."""
    user: UserData


class UserResponse(UserData):
    """User response schema (alias for UserData for compatibility)."""
    pass


# Delete user endpoint schemas
class DeleteUserRequest(BaseModel):
    """Request for deleting user (empty, uses Authorization header)."""
    pass


class DeleteUserResponse(BaseResponse):
    """Response after successful user deletion."""
    pass


# Change password endpoint schemas
class ChangePasswordRequest(BaseModel):
    """Request body for changing password."""
    old_password: str = Field(..., alias="oldPassword", min_length=1)
    new_password: str = Field(..., alias="newPassword", min_length=6)


class ChangePasswordResponse(BaseResponse):
    """Response after successful password change."""
    pass


# Edit user endpoint schemas
class EditUserRequest(BaseModel):
    """Request body for editing user profile."""
    username: Optional[str] = None
    # Note: image file is handled separately in FastAPI endpoint using File() parameter


class EditUserResponse(BaseResponse):
    """Response after successful user profile edit."""
    user: "UserData" = Field(..., alias="user")
    photo_url: Optional[str] = Field(None, alias="photoUrl")


# Save notification token endpoint schemas
class SaveNotificationTokenRequest(BaseModel):
    """Request body for saving notification token."""
    token: str = Field(..., min_length=1)


class SaveNotificationTokenResponse(BaseResponse):
    """Response after saving notification token."""
    pass


# Group member data structure
class GroupMemberData(BaseModel):
    """User data structure for group member responses."""
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
    """Request for creating a group (empty body)."""
    pass


class CreateGroupResponse(BaseResponse):
    """Response after successful group creation."""
    admin_id: int = Field(..., alias="adminId")


# Add member endpoint schemas
class AddMemberRequest(BaseModel):
    """Request body for adding a member to group."""
    username: str = Field(..., min_length=1)


class AddMemberResponse(BaseResponse):
    """Response after successfully adding member."""
    pass


# Delete member endpoint schemas
class DeleteMemberRequest(BaseModel):
    """Request body for removing a member from group."""
    username: str = Field(..., min_length=1)


class DeleteMemberResponse(BaseResponse):
    """Response after successfully removing member."""
    pass


# Get group members endpoint schemas
class GetGroupMembersRequest(BaseModel):
    """Request for getting group members (empty, GET request)."""
    pass


class GetGroupMembersResponse(BaseResponse):
    """Response with group admin and members list."""
    group_admin: GroupMemberData = Field(..., alias="groupAdmin")
    members: List[GroupMemberData] = []
