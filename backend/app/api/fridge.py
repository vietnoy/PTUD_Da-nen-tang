from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import Food, FridgeItem, Group, GroupMember, Unit, User
from ..schemas.base import ResultMessage
from ..schemas.fridge import (
    CreateFridgeItemRequest,
    CreateFridgeItemResponse,
    DeleteFridgeItemRequest,
    DeleteFridgeItemResponse,
    FridgeItemData,
    GetFridgeItemByIdRequest,
    GetFridgeItemByIdResponse,
    GetFridgeItemsResponse,
    UpdateFridgeItemRequest,
    UpdateFridgeItemResponse,
)
from ..utils.resultCode import ResultCode

router = APIRouter(prefix="/fridge", tags=["Fridge"])


@router.post(
    "/", response_model=CreateFridgeItemResponse, status_code=status.HTTP_201_CREATED
)
def create_fridge_item(
    request: CreateFridgeItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id, GroupMember.is_active == True)
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    food = (
        db.query(Food)
        .filter(
            Food.id == request.food_id,
            Food.group_id == group_member.group_id,
        )
        .first()
    )
    if not food:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food not found in group",
        )

    new_fridge_item = FridgeItem(
        food_id=request.food_id,
        group_id=group_member.group_id,
        quantity=request.quantity,
        unit_id=request.unit_id,
        note=request.note,
        purchase_date=request.purchase_date,
        use_within_date=request.use_within_date,
        location=request.location,
        is_opened=request.is_opened,
        opened_at=request.opened_at,
        cost=request.cost,
        created_by=current_user.id,
    )

    db.add(new_fridge_item)
    db.commit()
    db.refresh(new_fridge_item)

    fridge_item_data = _build_fridge_item_data(db, new_fridge_item)

    return CreateFridgeItemResponse(
        fridge_item=fridge_item_data,
        resultCode=ResultCode.SUCCESS_FRIDGE_ITEM_CREATED.value[0],
        resultMessage=ResultMessage(
            en="Fridge item created successfully",
            vn=ResultCode.SUCCESS_FRIDGE_ITEM_CREATED.value[1],
        ),
    )


@router.get("/", response_model=GetFridgeItemsResponse)
def get_fridge_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id, GroupMember.is_active == True)
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    fridge_items = (
        db.query(FridgeItem).filter(FridgeItem.group_id == group_member.group_id).all()
    )

    fridge_items_data = [_build_fridge_item_data(db, item) for item in fridge_items]

    return GetFridgeItemsResponse(
        fridge_items=fridge_items_data,
        resultCode=ResultCode.SUCCESS_FRIDGE_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Fridge items fetched successfully",
            vn=ResultCode.SUCCESS_FRIDGE_LIST_FETCHED.value[1],
        ),
    )


@router.post("/id/", response_model=GetFridgeItemByIdResponse)
def get_fridge_item_by_id(
    request: GetFridgeItemByIdRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id, GroupMember.is_active == True)
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    fridge_item = db.query(FridgeItem).filter(FridgeItem.id == request.id).first()
    if not fridge_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fridge item not found",
        )

    if fridge_item.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this fridge item",
        )

    fridge_item_data = _build_fridge_item_data(db, fridge_item)

    return GetFridgeItemByIdResponse(
        fridge_item=fridge_item_data,
        resultCode=ResultCode.SUCCESS_FRIDGE_ITEM_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Fridge item fetched successfully",
            vn=ResultCode.SUCCESS_FRIDGE_ITEM_FETCHED.value[1],
        ),
    )


@router.put("/", response_model=UpdateFridgeItemResponse)
def update_fridge_item(
    request: UpdateFridgeItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id, GroupMember.is_active == True)
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    fridge_item = db.query(FridgeItem).filter(FridgeItem.id == request.id).first()
    if not fridge_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fridge item not found",
        )

    if fridge_item.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this fridge item",
        )

    if request.quantity is not None:
        fridge_item.quantity = request.quantity

    if request.unit_id is not None:
        fridge_item.unit_id = request.unit_id

    if request.note is not None:
        fridge_item.note = request.note

    if request.purchase_date is not None:
        fridge_item.purchase_date = request.purchase_date

    if request.use_within_date is not None:
        fridge_item.use_within_date = request.use_within_date

    if request.location is not None:
        fridge_item.location = request.location

    if request.is_opened is not None:
        fridge_item.is_opened = request.is_opened

    if request.opened_at is not None:
        fridge_item.opened_at = request.opened_at

    if request.cost is not None:
        fridge_item.cost = request.cost

    db.commit()
    db.refresh(fridge_item)

    fridge_item_data = _build_fridge_item_data(db, fridge_item)

    return UpdateFridgeItemResponse(
        fridge_item=fridge_item_data,
        resultCode=ResultCode.SUCCESS_FRIDGE_ITEM_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Fridge item updated successfully",
            vn=ResultCode.SUCCESS_FRIDGE_ITEM_UPDATED.value[1],
        ),
    )


@router.delete("/", response_model=DeleteFridgeItemResponse)
def delete_fridge_item(
    request: DeleteFridgeItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id, GroupMember.is_active == True)
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    fridge_item = db.query(FridgeItem).filter(FridgeItem.id == request.id).first()
    if not fridge_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fridge item not found",
        )

    if fridge_item.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this fridge item",
        )

    db.delete(fridge_item)
    db.commit()

    return DeleteFridgeItemResponse(
        resultCode=ResultCode.SUCCESS_FRIDGE_ITEM_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Fridge item deleted successfully",
            vn=ResultCode.SUCCESS_FRIDGE_ITEM_DELETED.value[1],
        ),
    )


def _build_fridge_item_data(db: Session, fridge_item: FridgeItem) -> FridgeItemData:
    food = db.query(Food).filter(Food.id == fridge_item.food_id).first()
    food_name = food.name if food else "Unknown"

    unit_name = None
    if fridge_item.unit_id:
        unit = db.query(Unit).filter(Unit.id == fridge_item.unit_id).first()
        unit_name = unit.name if unit else None

    return FridgeItemData(
        id=fridge_item.id,
        food_id=fridge_item.food_id,
        food_name=food_name,
        group_id=fridge_item.group_id,
        quantity=fridge_item.quantity,
        unit_id=fridge_item.unit_id,
        unit_name=unit_name,
        note=fridge_item.note,
        purchase_date=fridge_item.purchase_date,
        use_within_date=fridge_item.use_within_date,
        location=fridge_item.location,
        is_opened=fridge_item.is_opened,
        opened_at=fridge_item.opened_at,
        cost=fridge_item.cost,
        created_by=fridge_item.created_by,
        created_at=fridge_item.created_at,
        updated_at=fridge_item.updated_at,
    )


__all__ = ["router"]
