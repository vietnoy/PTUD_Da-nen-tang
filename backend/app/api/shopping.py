from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import Food, GroupMember, ShoppingList, ShoppingTask, Unit, User
from ..schemas.base import ResultMessage
from ..schemas.shopping import (
    CreateShoppingListRequest,
    CreateShoppingListResponse,
    CreateShoppingTasksRequest,
    CreateShoppingTasksResponse,
    DeleteShoppingListRequest,
    DeleteShoppingListResponse,
    DeleteShoppingTaskRequest,
    DeleteShoppingTaskResponse,
    GetShoppingListByIdRequest,
    GetShoppingListByIdResponse,
    GetShoppingListsResponse,
    ShoppingListData,
    ShoppingTaskData,
    UpdateShoppingListRequest,
    UpdateShoppingListResponse,
    UpdateShoppingTaskRequest,
    UpdateShoppingTaskResponse,
)
from ..utils.resultCode import ResultCode

router = APIRouter(prefix="/shopping", tags=["Shopping"])


@router.post(
    "/list/",
    response_model=CreateShoppingListResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shopping_list(
    request: CreateShoppingListRequest,
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

    if request.priority not in ["low", "medium", "high"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Priority must be low, medium, or high",
        )

    assign_to_user_id = None
    if request.assign_to_username:
        assign_to_user = (
            db.query(User).filter(User.username == request.assign_to_username).first()
        )
        if not assign_to_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user not found",
            )
        assign_to_member = (
            db.query(GroupMember)
            .filter(
                GroupMember.user_id == assign_to_user.id,
                GroupMember.group_id == group_member.group_id,
                GroupMember.is_active == True,
            )
            .first()
        )
        if not assign_to_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user is not in the same group",
            )
        assign_to_user_id = assign_to_user.id

    new_list = ShoppingList(
        name=request.name,
        description=request.description,
        group_id=group_member.group_id,
        assign_to_user_id=assign_to_user_id,
        due_date=request.due_date,
        priority=request.priority,
        status="active",
        budget=request.budget,
        total_cost=Decimal("0"),
        is_archived=False,
        created_by=current_user.id,
    )

    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    list_data = _build_shopping_list_data(db, new_list)

    return CreateShoppingListResponse(
        shopping_list=list_data,
        resultCode=ResultCode.SUCCESS_SHOPPING_LIST_CREATED.value[0],
        resultMessage=ResultMessage(
            en="Shopping list created successfully",
            vn=ResultCode.SUCCESS_SHOPPING_LIST_CREATED.value[1],
        ),
    )


@router.get("/list/", response_model=GetShoppingListsResponse)
def get_shopping_lists(
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

    shopping_lists = (
        db.query(ShoppingList)
        .filter(ShoppingList.group_id == group_member.group_id)
        .all()
    )

    lists_data = [_build_shopping_list_data(db, lst) for lst in shopping_lists]

    return GetShoppingListsResponse(
        shopping_lists=lists_data,
        resultCode=ResultCode.SUCCESS_TASK_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Shopping lists fetched successfully",
            vn=ResultCode.SUCCESS_TASK_LIST_FETCHED.value[1],
        ),
    )


@router.post("/list/id/", response_model=GetShoppingListByIdResponse)
def get_shopping_list_by_id(
    request: GetShoppingListByIdRequest,
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

    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == request.id).first()
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list not found",
        )

    if shopping_list.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this shopping list",
        )

    list_data = _build_shopping_list_data(db, shopping_list)

    tasks = (
        db.query(ShoppingTask).filter(ShoppingTask.list_id == shopping_list.id).all()
    )
    tasks_data = [_build_shopping_task_data(db, task) for task in tasks]

    return GetShoppingListByIdResponse(
        shopping_list=list_data,
        tasks=tasks_data,
        resultCode=ResultCode.SUCCESS_TASK_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Shopping list fetched successfully",
            vn=ResultCode.SUCCESS_TASK_LIST_FETCHED.value[1],
        ),
    )


@router.put("/list/", response_model=UpdateShoppingListResponse)
def update_shopping_list(
    request: UpdateShoppingListRequest,
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

    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == request.id).first()
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list not found",
        )

    if shopping_list.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this shopping list",
        )

    if request.new_name is not None:
        shopping_list.name = request.new_name

    if request.new_assign_to_username is not None:
        assign_to_user = (
            db.query(User)
            .filter(User.username == request.new_assign_to_username)
            .first()
        )
        if not assign_to_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user not found",
            )
        shopping_list.assign_to_user_id = assign_to_user.id

    if request.new_due_date is not None:
        shopping_list.due_date = request.new_due_date

    if request.new_status is not None:
        if request.new_status not in ["draft", "active", "completed", "cancelled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be draft, active, completed, or cancelled",
            )
        shopping_list.status = request.new_status

    if request.new_priority is not None:
        if request.new_priority not in ["low", "medium", "high"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Priority must be low, medium, or high",
            )
        shopping_list.priority = request.new_priority

    if request.new_budget is not None:
        shopping_list.budget = request.new_budget

    db.commit()
    db.refresh(shopping_list)

    list_data = _build_shopping_list_data(db, shopping_list)

    return UpdateShoppingListResponse(
        shopping_list=list_data,
        resultCode=ResultCode.SUCCESS_SHOPPING_LIST_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Shopping list updated successfully",
            vn=ResultCode.SUCCESS_SHOPPING_LIST_UPDATED.value[1],
        ),
    )


@router.delete("/list/", response_model=DeleteShoppingListResponse)
def delete_shopping_list(
    request: DeleteShoppingListRequest,
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

    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == request.id).first()
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list not found",
        )

    if shopping_list.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this shopping list",
        )

    db.delete(shopping_list)
    db.commit()

    return DeleteShoppingListResponse(
        resultCode=ResultCode.SUCCESS_SHOPPING_LIST_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Shopping list deleted successfully",
            vn=ResultCode.SUCCESS_SHOPPING_LIST_DELETED.value[1],
        ),
    )


@router.post(
    "/task/",
    response_model=CreateShoppingTasksResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_tasks_to_list(
    request: CreateShoppingTasksRequest,
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

    shopping_list = (
        db.query(ShoppingList).filter(ShoppingList.id == request.list_id).first()
    )
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list not found",
        )

    if shopping_list.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this shopping list",
        )

    created_tasks = []
    for task_input in request.tasks:
        if task_input.priority not in ["low", "medium", "high"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Priority must be low, medium, or high",
            )

        food = (
            db.query(Food)
            .filter(
                Food.id == task_input.food_id,
                Food.group_id == group_member.group_id,
            )
            .first()
        )
        if not food:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Food not found in group",
            )

        new_task = ShoppingTask(
            list_id=shopping_list.id,
            food_id=task_input.food_id,
            quantity=task_input.quantity,
            unit_id=task_input.unit_id,
            note=task_input.note,
            estimated_cost=task_input.estimated_cost,
            priority=task_input.priority,
            is_done=False,
        )

        db.add(new_task)
        created_tasks.append(new_task)

    db.commit()
    for task in created_tasks:
        db.refresh(task)

    tasks_data = [_build_shopping_task_data(db, task) for task in created_tasks]

    return CreateShoppingTasksResponse(
        tasks=tasks_data,
        resultCode=ResultCode.SUCCESS_TASK_ADDED.value[0],
        resultMessage=ResultMessage(
            en="Tasks added successfully",
            vn=ResultCode.SUCCESS_TASK_ADDED.value[1],
        ),
    )


@router.put("/task/", response_model=UpdateShoppingTaskResponse)
def update_shopping_task(
    request: UpdateShoppingTaskRequest,
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

    task = db.query(ShoppingTask).filter(ShoppingTask.id == request.task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping task not found",
        )

    shopping_list = (
        db.query(ShoppingList).filter(ShoppingList.id == task.list_id).first()
    )
    if shopping_list.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this shopping task",
        )

    if request.new_quantity is not None:
        task.quantity = request.new_quantity

    if request.new_note is not None:
        task.note = request.new_note

    if request.new_estimated_cost is not None:
        task.estimated_cost = request.new_estimated_cost

    if request.actual_cost is not None:
        task.actual_cost = request.actual_cost

    if request.is_done is not None:
        task.is_done = request.is_done
        if request.is_done:
            task.done_at = datetime.now()
            task.done_by = current_user.id
        else:
            task.done_at = None
            task.done_by = None

    db.commit()
    db.refresh(task)

    _recalculate_total_cost(db, shopping_list)

    task_data = _build_shopping_task_data(db, task)

    return UpdateShoppingTaskResponse(
        task=task_data,
        resultCode=ResultCode.SUCCESS_TASK_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Task updated successfully",
            vn=ResultCode.SUCCESS_TASK_UPDATED.value[1],
        ),
    )


@router.delete("/task/", response_model=DeleteShoppingTaskResponse)
def delete_shopping_task(
    request: DeleteShoppingTaskRequest,
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

    task = db.query(ShoppingTask).filter(ShoppingTask.id == request.task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping task not found",
        )

    shopping_list = (
        db.query(ShoppingList).filter(ShoppingList.id == task.list_id).first()
    )
    if shopping_list.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this shopping task",
        )

    db.delete(task)
    db.commit()

    _recalculate_total_cost(db, shopping_list)

    return DeleteShoppingTaskResponse(
        resultCode=ResultCode.SUCCESS_TASK_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Task deleted successfully",
            vn=ResultCode.SUCCESS_TASK_DELETED.value[1],
        ),
    )


def _build_shopping_list_data(
    db: Session, shopping_list: ShoppingList
) -> ShoppingListData:
    assign_to_username = None
    if shopping_list.assign_to_user_id:
        assign_to_user = (
            db.query(User).filter(User.id == shopping_list.assign_to_user_id).first()
        )
        if assign_to_user:
            assign_to_username = assign_to_user.username

    # Resolve creator username
    created_by_username = None
    if shopping_list.created_by:
        creator = db.query(User).filter(User.id == shopping_list.created_by).first()
        if creator:
            created_by_username = creator.username

    return ShoppingListData(
        id=shopping_list.id,
        name=shopping_list.name,
        description=shopping_list.description,
        group_id=shopping_list.group_id,
        assign_to_user_id=shopping_list.assign_to_user_id,
        assign_to_username=assign_to_username,
        due_date=shopping_list.due_date,
        priority=shopping_list.priority,
        status=shopping_list.status,
        budget=shopping_list.budget,
        total_cost=shopping_list.total_cost,
        is_archived=shopping_list.is_archived,
        created_by=shopping_list.created_by,
        created_by_username=created_by_username,
        created_at=shopping_list.created_at,
        updated_at=shopping_list.updated_at,
    )


def _build_shopping_task_data(db: Session, task: ShoppingTask) -> ShoppingTaskData:
    food = db.query(Food).filter(Food.id == task.food_id).first()
    food_name = food.name if food else "Unknown"

    unit_name = None
    if task.unit_id:
        unit = db.query(Unit).filter(Unit.id == task.unit_id).first()
        unit_name = unit.name if unit else None

    # Resolve done_by username
    done_by_username = None
    if task.done_by:
        done_by_user = db.query(User).filter(User.id == task.done_by).first()
        if done_by_user:
            done_by_username = done_by_user.username

    return ShoppingTaskData(
        id=task.id,
        list_id=task.list_id,
        food_id=task.food_id,
        food_name=food_name,
        quantity=task.quantity,
        unit_id=task.unit_id,
        unit_name=unit_name,
        note=task.note,
        estimated_cost=task.estimated_cost,
        actual_cost=task.actual_cost,
        priority=task.priority,
        is_done=task.is_done,
        done_at=task.done_at,
        done_by=task.done_by,
        done_by_username=done_by_username,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def _recalculate_total_cost(db: Session, shopping_list: ShoppingList):
    tasks = (
        db.query(ShoppingTask).filter(ShoppingTask.list_id == shopping_list.id).all()
    )

    total = Decimal("0")
    for task in tasks:
        if task.actual_cost is not None:
            total += task.actual_cost
        elif task.estimated_cost is not None:
            total += task.estimated_cost

    shopping_list.total_cost = total
    db.commit()


__all__ = ["router"]
