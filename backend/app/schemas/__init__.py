# Main schemas exports for easy importing

# Base response structures
# Admin schemas

# Authentication schemas
from .auth import (
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    RegisterResponse,
    SendVerificationCodeRequest,
    SendVerificationCodeResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
)

# Base schemas
from .base import BaseResponse, ResultMessage, UserData
from .unit import (
    CreateUnitRequest,
    CreateUnitResponse,
    DeleteUnitRequest,
    DeleteUnitResponse,
    EditUnitByNameRequest,
    EditUnitByNameResponse,
    GetAllUnitsRequest,
    GetAllUnitsResponse,
    UnitData,
)

# User schemas
from .user import (
    AddMemberRequest,
    AddMemberResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    CreateGroupRequest,
    CreateGroupResponse,
    DeleteMemberRequest,
    DeleteMemberResponse,
    DeleteUserRequest,
    DeleteUserResponse,
    EditUserRequest,
    EditUserResponse,
    GetGroupMembersRequest,
    GetGroupMembersResponse,
    GetUserRequest,
    GetUserResponse,
    GroupMemberData,
    SaveNotificationTokenRequest,
    SaveNotificationTokenResponse,
    UserResponse,
)

# Export all for * imports
__all__ = [
    # Base
    "ResultMessage",
    "BaseResponse",
    # User Auth
    "UserData",
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "LogoutRequest",
    "LogoutResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "SendVerificationCodeRequest",
    "SendVerificationCodeResponse",
    "VerifyEmailRequest",
    "VerifyEmailResponse",
    # User Edit
    "ChangePasswordRequest",
    "ChangePasswordResponse",
    "EditUserRequest",
    "EditUserResponse",
    "SaveNotificationTokenRequest",
    "SaveNotificationTokenResponse",
    # User Group
    "GroupMemberData",
    "CreateGroupRequest",
    "CreateGroupResponse",
    "AddMemberRequest",
    "AddMemberResponse",
    "DeleteMemberRequest",
    "DeleteMemberResponse",
    "GetGroupMembersRequest",
    "GetGroupMembersResponse",
    # User
    "GetUserRequest",
    "GetUserResponse",
    "DeleteUserRequest",
    "DeleteUserResponse",
    "UserResponse",
    # Unit
    "UnitData",
    "CreateUnitRequest",
    "CreateUnitResponse",
    "GetAllUnitsRequest",
    "GetAllUnitsResponse",
    "EditUnitByNameRequest",
    "EditUnitByNameResponse",
    "DeleteUnitRequest",
    "DeleteUnitResponse",
]
