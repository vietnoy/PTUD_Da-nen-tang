from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import Food, GroupMember, MealPlan, Unit, User
from ..schemas.base import ResultMessage
from ..schemas.meal_plan import (
    CreateMealPlanRequest,
    CreateMealPlanResponse,
    DeleteMealPlanRequest,
    DeleteMealPlanResponse,
    GetMealPlanByIdRequest,
    GetMealPlanByIdResponse,
    GetMealPlansRequest,
    GetMealPlansResponse,
    MealPlanData,
    UpdateMealPlanRequest,
    UpdateMealPlanResponse,
)
from ..utils.resultCode import ResultCode

router = APIRouter(prefix="/meal-plans", tags=["Meal Plans"])


@router.post(
    "/", response_model=CreateMealPlanResponse, status_code=status.HTTP_201_CREATED
)
def create_meal_plan(
    request: CreateMealPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.user_id == current_user.id, GroupMember.is_active == True
        )
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    meal_type_lower = request.meal_type.lower()
    if meal_type_lower not in ["breakfast", "lunch", "dinner"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Meal type must be breakfast, lunch, or dinner",
        )

    # Verify the food exists and belongs to the user's group
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

    # Verify unit exists if provided
    if request.unit_id:
        unit = db.query(Unit).filter(Unit.id == request.unit_id).first()
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit not found",
            )

    # Convert serving_size from string to Decimal if provided
    serving_size_decimal = None
    if request.serving_size:
        try:
            from decimal import Decimal
            serving_size_decimal = Decimal(request.serving_size)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid serving size format",
            )

    new_meal_plan = MealPlan(
        food_id=request.food_id,
        group_id=group_member.group_id,
        meal_type=meal_type_lower,
        meal_date=request.meal_date,
        serving_size=serving_size_decimal,
        unit_id=request.unit_id,
        note=request.note,
        is_prepared=request.is_prepared,
        created_by=current_user.id,
    )

    db.add(new_meal_plan)
    db.commit()
    db.refresh(new_meal_plan)

    meal_plan_data = _build_meal_plan_data(db, new_meal_plan)

    return CreateMealPlanResponse(
        meal_plan=meal_plan_data,
        resultCode=ResultCode.SUCCESS_MEAL_PLAN_ADDED.value[0],
        resultMessage=ResultMessage(
            en="Meal plan created successfully",
            vn=ResultCode.SUCCESS_MEAL_PLAN_ADDED.value[1],
        ),
    )


@router.get("/", response_model=GetMealPlansResponse)
def get_meal_plans(
    start_date: str | None = None,
    end_date: str | None = None,
    meal_type: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.user_id == current_user.id, GroupMember.is_active == True
        )
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    query = db.query(MealPlan).filter(MealPlan.group_id == group_member.group_id)

    if start_date:
        from datetime import date as date_type
        start = date_type.fromisoformat(start_date)
        query = query.filter(MealPlan.meal_date >= start)

    if end_date:
        from datetime import date as date_type
        end = date_type.fromisoformat(end_date)
        query = query.filter(MealPlan.meal_date <= end)

    if meal_type:
        meal_type_lower = meal_type.lower()
        if meal_type_lower in ["breakfast", "lunch", "dinner"]:
            query = query.filter(MealPlan.meal_type == meal_type_lower)

    meal_plans = query.all()

    meal_plans_data = [_build_meal_plan_data(db, mp) for mp in meal_plans]

    return GetMealPlansResponse(
        meal_plans=meal_plans_data,
        resultCode=ResultCode.SUCCESS_MEAL_PLAN_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Meal plans fetched successfully",
            vn=ResultCode.SUCCESS_MEAL_PLAN_LIST_FETCHED.value[1],
        ),
    )


@router.post("/id/", response_model=GetMealPlanByIdResponse)
def get_meal_plan_by_id(
    request: GetMealPlanByIdRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.user_id == current_user.id, GroupMember.is_active == True
        )
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    meal_plan = db.query(MealPlan).filter(MealPlan.id == request.meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found",
        )

    if meal_plan.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this meal plan",
        )

    meal_plan_data = _build_meal_plan_data(db, meal_plan)

    return GetMealPlanByIdResponse(
        meal_plan=meal_plan_data,
        resultCode=ResultCode.SUCCESS_MEAL_PLAN_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Meal plan fetched successfully",
            vn=ResultCode.SUCCESS_MEAL_PLAN_LIST_FETCHED.value[1],
        ),
    )


@router.put("/", response_model=UpdateMealPlanResponse)
def update_meal_plan(
    request: UpdateMealPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.user_id == current_user.id, GroupMember.is_active == True
        )
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    meal_plan = db.query(MealPlan).filter(MealPlan.id == request.meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found",
        )

    if meal_plan.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this meal plan",
        )

    if request.food_id is not None:
        # Verify the food exists and belongs to the user's group
        food = (
            db.query(Food)
            .filter(
                Food.id == request.food_id,
                Food.group_id == group_member.group_id
            )
            .first()
        )
        if not food:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Food not found in group",
            )
        meal_plan.food_id = request.food_id

    if request.meal_type is not None:
        meal_type_lower = request.meal_type.lower()
        if meal_type_lower not in ["breakfast", "lunch", "dinner"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Meal type must be breakfast, lunch, or dinner",
            )
        meal_plan.meal_type = meal_type_lower

    if request.meal_date is not None:
        meal_plan.meal_date = request.meal_date

    if request.serving_size is not None:
        try:
            from decimal import Decimal
            meal_plan.serving_size = Decimal(request.serving_size)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid serving size format",
            )

    if request.unit_id is not None:
        # Verify unit exists
        unit = db.query(Unit).filter(Unit.id == request.unit_id).first()
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit not found",
            )
        meal_plan.unit_id = request.unit_id

    if request.note is not None:
        meal_plan.note = request.note

    if request.is_prepared is not None:
        meal_plan.is_prepared = request.is_prepared
        if request.is_prepared:
            meal_plan.prepared_at = datetime.now()
        else:
            meal_plan.prepared_at = None

    db.commit()
    db.refresh(meal_plan)

    meal_plan_data = _build_meal_plan_data(db, meal_plan)

    return UpdateMealPlanResponse(
        meal_plan=meal_plan_data,
        resultCode=ResultCode.SUCCESS_MEAL_PLAN_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Meal plan updated successfully",
            vn=ResultCode.SUCCESS_MEAL_PLAN_UPDATED.value[1],
        ),
    )


@router.delete("/", response_model=DeleteMealPlanResponse)
def delete_meal_plan(
    request: DeleteMealPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.user_id == current_user.id, GroupMember.is_active == True
        )
        .first()
    )
    if not group_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in any group",
        )

    meal_plan = db.query(MealPlan).filter(MealPlan.id == request.meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found",
        )

    if meal_plan.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this meal plan",
        )

    db.delete(meal_plan)
    db.commit()

    return DeleteMealPlanResponse(
        resultCode=ResultCode.SUCCESS_MEAL_PLAN_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Meal plan deleted successfully",
            vn=ResultCode.SUCCESS_MEAL_PLAN_DELETED.value[1],
        ),
    )


def _build_meal_plan_data(db: Session, meal_plan: MealPlan) -> MealPlanData:
    food = db.query(Food).filter(Food.id == meal_plan.food_id).first()
    food_name = food.name if food else "Unknown"

    unit_name = None
    if meal_plan.unit_id:
        unit = db.query(Unit).filter(Unit.id == meal_plan.unit_id).first()
        unit_name = unit.name if unit else None

    # Resolve creator username
    created_by_username = None
    if meal_plan.created_by:
        creator = db.query(User).filter(User.id == meal_plan.created_by).first()
        if creator:
            created_by_username = creator.username

    return MealPlanData(
        id=meal_plan.id,
        food_id=meal_plan.food_id,
        food_name=food_name,
        group_id=meal_plan.group_id,
        meal_type=meal_plan.meal_type,
        meal_date=meal_plan.meal_date,
        serving_size=meal_plan.serving_size,
        unit_id=meal_plan.unit_id,
        unit_name=unit_name,
        note=meal_plan.note,
        is_prepared=meal_plan.is_prepared,
        prepared_at=meal_plan.prepared_at,
        created_by=meal_plan.created_by,
        created_by_username=created_by_username,
        created_at=meal_plan.created_at,
        updated_at=meal_plan.updated_at,
    )


__all__ = ["router"]
