"""Food - related API routes."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..core import storage
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
    name: str = Form(...),
    category_name: str = Form(...),
    unit_name: str = Form(...),
    group_id: int = Form(...),
    description: str = Form(None),
    brand: str = Form(None),
    default_shelf_life_days: int = Form(None),
    storage_instructions: str = Form(None),
    image: UploadFile = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name does not exist",
        )
    unit = db.query(Unit).filter(Unit.name == unit_name).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit with this ID does not exist",
        )
    food = db.query(Food).filter(Food.name == name).first()
    if food:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food with this name already exists",
        )

    # Handle image upload
    image_url = None
    if image:
        try:
            client = storage.get_minio_client()
            response = storage.upload_file(client, image, "food", None)
            if response:
                image_url = response["public_url"]
        except Exception as e:
            print(f"Error uploading image: {e}")

    new_food = Food(
        name=name,
        category_id=category.id,
        category_name=category.name,
        unit_id=unit.id,
        unit_name=unit.name,
        group_id=group_id,
        created_by=user.id,
        description=description,
        image_url=image_url,
        brand=brand,
        default_shelf_life_days=default_shelf_life_days,
        storage_instructions=storage_instructions,
        is_active=True,
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
    user: User = Depends(get_current_user),
):
    foods = db.query(Food).filter(
        Food.group_id == user.belongs_to_group_admin_id,
        Food.is_active == True
    ).all()
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
    foodId: int = Form(...),
    name: str = Form(None),
    description: str = Form(None),
    categoryId: int = Form(None),
    defaultUnitId: int = Form(None),
    brand: str = Form(None),
    default_shelf_life_days: int = Form(None),
    storage_instructions: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    food = db.query(Food).filter(Food.id == foodId).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )

    if name is not None:
        food.name = name

    if categoryId is not None:
        category = db.query(Category).filter(Category.id == categoryId).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )
        food.category_id = category.id
        food.category_name = category.name

    if defaultUnitId is not None:
        unit = db.query(Unit).filter(Unit.id == defaultUnitId).first()
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit not found",
            )
        food.unit_id = unit.id
        food.unit_name = unit.name

    if description is not None:
        food.description = description

    if brand is not None:
        food.brand = brand

    if default_shelf_life_days is not None:
        food.default_shelf_life_days = default_shelf_life_days

    if storage_instructions is not None:
        food.storage_instructions = storage_instructions

    # Handle image upload
    if image:
        try:
            client = storage.get_minio_client()
            response = storage.upload_file(client, image, "food", food.image_url)
            if response:
                food.image_url = response["public_url"]
        except Exception as e:
            print(f"Error uploading image: {e}")

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
    food = db.query(Food).filter(Food.id == request.food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )
    # Soft delete by setting is_active to False
    food.is_active = False
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
