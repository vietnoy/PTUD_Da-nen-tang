"""Food - related API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import Category, Food, Unit, User
from ..schemas.base import ResultMessage
from ..schemas.food import (
    CreateFoodRequest,
    CreateFoodResponse,
    DeleteFoodByNameRequest,
    DeleteFoodByNameResponse,
    EditFoodByNameRequest,
    EditFoodByNameResponse,
    FoodData,
    GetAllFoodsResponse,
    GetFoodsByNamesRequest,
    GetFoodsByNamesResponse,
)
from ..utils.resultCode import ResultCode

router = APIRouter(prefix="/food", tags=["Foods"])


@router.post(
    "/", response_model=CreateFoodResponse, status_code=status.HTTP_201_CREATED
)
def create_food(
    request: CreateFoodRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.name == request.category_name).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name does not exist",
        )
    unit = db.query(Unit).filter(Unit.name == request.unit_name).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit with this ID does not exist",
        )
    food = db.query(Food).filter(Food.name == request.name).first()
    if food:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food with this name already exists",
        )
    new_food = Food(
        name=request.name,
        category_id=category.id,
        category_name=category.name,
        unit_id=unit.id,
        unit_name=unit.name,
        group_id=request.group_id,
        created_by=user.id,
        description=request.description,
        image_url=request.image_url,
        brand=request.brand,
        default_shelf_life_days=request.default_shelf_life_days,
        storage_instructions=request.storage_instructions,
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return CreateFoodResponse(
        food=FoodData.model_validate(new_food),
        resultCode=ResultCode.SUCCESS_FOOD_CREATED.value[0],
        resultMessage=ResultMessage(
            en="Food created successfully",
            vn=ResultCode.SUCCESS_FOOD_CREATED.value[1],
        ),
    )


@router.get("/", response_model=GetAllFoodsResponse)
def get_all_foods(
    db: Session = Depends(get_db),
):
    foods = db.query(Food).all()
    return GetAllFoodsResponse(
        foods=[FoodData.model_validate(food) for food in foods],
        resultCode=ResultCode.SUCCESS_FOOD_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Foods fetched successfully",
            vn=ResultCode.SUCCESS_FOOD_LIST_FETCHED.value[1],
        ),
    )


@router.put("/", response_model=EditFoodByNameResponse)
def edit_food_by_name(
    request: EditFoodByNameRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    food = db.query(Food).filter(Food.name == request.food_name).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food with this name does not exist",
        )
    if request.name is not None:
        food.name = request.name
    if request.category_name is not None:
        category = (
            db.query(Category).filter(Category.name == request.category_name).first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name does not exist",
            )
        food.category_id = category.id
    if request.unit_name is not None:
        unit = db.query(Unit).filter(Unit.name == request.unit_name).first()
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit with this name does not exist",
            )
        food.unit_id = unit.id
    if request.group_id is not None:
        food.group_id = request.group_id
    if request.description is not None:
        food.description = request.description
    if request.image_url is not None:
        food.image_url = request.image_url
    if request.brand is not None:
        food.brand = request.brand
    if request.default_shelf_life_days is not None:
        food.default_shelf_life_days = request.default_shelf_life_days
    if request.storage_instructions is not None:
        food.storage_instructions = request.storage_instructions

    db.commit()
    db.refresh(food)
    return EditFoodByNameResponse(
        food=FoodData.model_validate(food),
        resultCode=ResultCode.SUCCESS_FOOD_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Food updated successfully",
            vn=ResultCode.SUCCESS_FOOD_UPDATED.value[1],
        ),
    )


@router.delete("/", response_model=DeleteFoodByNameResponse)
def delete_food_by_name(
    request: DeleteFoodByNameRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    food = db.query(Food).filter(Food.name == request.food_name).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food with this name does not exist",
        )
    db.delete(food)
    db.commit()
    return DeleteFoodByNameResponse(
        resultCode=ResultCode.SUCCESS_FOOD_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Food deleted successfully",
            vn=ResultCode.SUCCESS_FOOD_DELETED.value[1],
        ),
    )


@router.post("/names/", response_model=GetFoodsByNamesResponse)
def get_foods_by_names(
    request: GetFoodsByNamesRequest,
    db: Session = Depends(get_db),
):
    foods = db.query(Food).filter(Food.name.in_(request.food_names)).all()
    return GetFoodsByNamesResponse(
        foods=[FoodData.model_validate(food) for food in foods],
        resultCode=ResultCode.SUCCESS_FOOD_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Foods fetched successfully by names",
            vn=ResultCode.SUCCESS_FOOD_LIST_FETCHED.value[1],
        ),
    )


__all__ = ["router"]
