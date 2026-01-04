from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse, UserData


class CreateGroupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class CreateGroupResponse(BaseResponse):
    invite_code: str = Field(..., min_length=6, max_length=6)
    name: str = Field(..., alias="groupName")
    owner_id: int = Field(..., alias="ownerID")


class AddMemberRequest(BaseModel):
    invite_code: str = Field(..., min_length=6, max_length=6, alias="inviteCode")


class AddMemberResponse(BaseResponse):
    group_id: int = Field(..., alias="groupId")


class RemoveMemberRequest(BaseModel):
    user_name: str = Field(...)
    group_id: int = Field(...)


class RemoveMemberResponse(BaseResponse):
    pass


class MemberInfo(BaseModel):
    id: int
    name: str
    username: str | None
    avatar_url: str | None = Field(None, alias="avatarUrl")
    role: str
    joined_at: str = Field(..., alias="joinedAt")

    class Config:
        from_attributes = True
        populate_by_name = True


class GetGroupMembersResponse(BaseResponse):
    group_id: int = Field(..., alias="groupId")
    group_name: str = Field(..., alias="groupName")
    invite_code: str | None = Field(None, alias="inviteCode")
    members: List[MemberInfo]
