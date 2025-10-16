from ..models import User, Group, GroupMember
from sqlalchemy.orm import Session
from ..schemas.group import CreateGroupRequest, CreateGroupResponse, AddMemberRequest
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

        if db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user has already been a member of the group!"
            )
        
        group_member = GroupMember(
            user_id=user_id,
            group_id=group_id,
            role="member"
        )

        db.add(group_member)
        db.commit()