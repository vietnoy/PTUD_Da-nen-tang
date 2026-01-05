from ..models import User, Group, GroupMember
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..schemas.group import CreateGroupRequest, CreateGroupResponse
from ..schemas.base import ResultMessage
from fastapi import HTTPException, status
import secrets

class GroupService:
    @staticmethod
    def register(user: User, db: Session, request: CreateGroupRequest):
        
        # check if whether user has group with a same name
        result = db.query(Group).filter(Group.owner_id == user.id, Group.name == request.name).first()
        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name of the group have existed!"
            )
        
        group = Group(
            name=request.name,
            description=request.description,
            owner_id=user.id,
            invite_code=secrets.token_urlsafe(4)[:6].upper()
        )
        

        db.add(group)
        db.commit()

        # we should add the current user to the group with the role "owner"
        group_member = GroupMember(
            user_id=user.id,
            group_id=group.id,
            role="owner"
        )
        db.add(group_member)
        db.commit()

        return CreateGroupResponse(
            resultMessage=ResultMessage(
                en="Create group succesfully",
                vn="Tạo nhóm thành công"
            ),
            resultCode="00101",
            invite_code=group.invite_code,
            groupName=group.name,
            ownerID=user.id
        )
    
    @staticmethod
    def get_user_role(user_id: str, group_id: str, db: Session):
        response = db.query(GroupMember).filter(GroupMember.user_id == user_id, GroupMember.group_id == group_id).first()
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not a member of this group"
            )
        return response.role
    
    @staticmethod
    def add_group_member(user_id: str, db: Session, group_id: str):

        # Check if user already has an ACTIVE membership
        existing_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()

        if existing_membership and existing_membership.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user has already been a member of the group!"
            )

        # Deactivate all previous group memberships for this user (except where they're owner)
        db.query(GroupMember).filter(
            GroupMember.user_id == user_id,
            GroupMember.is_active == True,
            GroupMember.role != "owner"  # Don't deactivate owner memberships
        ).update({"is_active": False, "left_at": func.now()})

        # If user previously left this group, reactivate their membership
        if existing_membership and not existing_membership.is_active:
            existing_membership.is_active = True
            existing_membership.left_at = None
            existing_membership.joined_at = func.now()
        else:
            # Create new membership
            group_member = GroupMember(
                user_id=user_id,
                group_id=group_id,
                role="member",
                is_active=True
            )
            db.add(group_member)

        # Switch user's active group to the one they're joining
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.belongs_to_group_admin_id = group_id

        db.commit()

    @staticmethod
    def remove_group_member(user_id: str, db: Session, group_id: str):
        """Handle user leaving/being removed from group."""
        user = db.query(User).filter(User.id == user_id).first()

        if user and user.belongs_to_group_admin_id == group_id:
            # User is leaving their active group, switch back to their own group
            # Find the group where they are owner
            own_group = db.query(Group).filter(Group.owner_id == user_id).first()
            if own_group:
                user.belongs_to_group_admin_id = own_group.id
            else:
                # Fallback: set to NULL if no owned group found
                user.belongs_to_group_admin_id = None

        db.commit()