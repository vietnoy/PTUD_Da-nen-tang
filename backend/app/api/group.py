from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import User, GroupMember, Group
from ..services.group import GroupService

from ..schemas.group import (CreateGroupRequest, CreateGroupResponse, AddMemberRequest, AddMemberResponse,
                             RemoveMemberRequest, RemoveMemberResponse, GetGroupMembersResponse, MemberInfo)

router = APIRouter(prefix="/user", tags=["Groups"])


@router.post("/group", response_model=CreateGroupResponse)
def create_group(request: CreateGroupRequest,
                 current_user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):

    # verify the group first
    response = GroupService.register(current_user, db, request)

    return response

@router.post("/group/add", response_model=AddMemberResponse)
def add_member(request: AddMemberRequest,
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):

    group  = db.query(Group).filter(Group.invite_code == request.invite_code).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    GroupService.add_group_member(user_id=current_user.id, db=db, group_id=group.id)

    return AddMemberResponse()

@router.delete("/group", response_model=RemoveMemberResponse)
def remove_member(request: RemoveMemberRequest,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    # Check if group exists
    group = db.query(Group).filter(Group.id == request.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Get current user's role
    user_role = GroupService.get_user_role(current_user.id, group.id, db)

    # Get target member to remove
    target_member = db.query(GroupMember).filter(
        GroupMember.group_id == request.group_id,
        GroupMember.user_id == request.user_id
    ).first()

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in group"
        )

    # Get target user's role
    target_role = target_member.role

    # Permission logic
    if request.user_id == current_user.id:
        # User wants to leave the group
        if target_role == "owner":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner cannot leave group. Transfer ownership first."
            )
    else:
        # Removing someone else - check permissions
        if user_role == "owner":
            # Owner can remove anyone except themselves
            pass
        elif user_role == "admin":
            # Admin can only remove regular members
            if target_role != "member":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admins can only remove regular members"
                )
        else:
            # Regular members can only remove themselves
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to remove this member"
            )

    db.delete(target_member)
    db.commit()

    return RemoveMemberResponse()


@router.get("/group", response_model=GetGroupMembersResponse)
def get_group_members(group_id: int,
                      current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):

    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Verify current user is a member of this group
    user_membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id,
        GroupMember.is_active == True
    ).first()

    if not user_membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )

    # Get all active members with their user details
    members = db.query(GroupMember, User).join(
        User, GroupMember.user_id == User.id
    ).filter(
        GroupMember.group_id == group_id,
        GroupMember.is_active == True
    ).all()

    # Build member info list
    member_list = []
    for member, user in members:
        member_list.append(MemberInfo(
            id=user.id,
            name=user.name,
            username=user.username,
            avatarUrl=user.avatar_url,
            role=member.role,
            joinedAt=member.joined_at.isoformat()
        ))

    return GetGroupMembersResponse(
        groupId=group.id,
        groupName=group.name,
        members=member_list
    )