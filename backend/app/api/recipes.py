from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ..core import storage
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import Food, GroupMember, Recipe, User
from ..schemas.base import ResultMessage
from ..schemas.recipe import (
    CreateRecipeResponse,
    DeleteRecipeRequest,
    DeleteRecipeResponse,
    GetRecipeByIdRequest,
    GetRecipeByIdResponse,
    GetRecipesResponse,
    RecipeData,
    UpdateRecipeResponse,
)
from ..utils.resultCode import ResultCode

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post(
    "/", response_model=CreateRecipeResponse, status_code=status.HTTP_201_CREATED
)
def create_recipe(
    name: str = Form(...),
    description: str = Form(...),
    html_content: str = Form(..., alias="htmlContent"),
    food_name: str | None = Form(None, alias="foodName"),
    prep_time_minutes: int | None = Form(None, alias="prepTimeMinutes"),
    cook_time_minutes: int | None = Form(None, alias="cookTimeMinutes"),
    servings: int | None = Form(None),
    difficulty: str | None = Form(None),
    is_public: bool = Form(False, alias="isPublic"),
    file: UploadFile = File(None),
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

    if difficulty and difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Difficulty must be easy, medium, or hard",
        )

    food_id = None
    if food_name:
        food = (
            db.query(Food)
            .filter(
                Food.name == food_name,
                Food.group_id == group_member.group_id,
                Food.is_active == True,
            )
            .first()
        )
        if food:
            food_id = food.id

    new_recipe = Recipe(
        name=name,
        description=description,
        html_content=html_content,
        food_id=food_id,
        group_id=group_member.group_id,
        prep_time_minutes=prep_time_minutes,
        cook_time_minutes=cook_time_minutes,
        servings=servings,
        difficulty=difficulty,
        is_public=is_public,
        created_by=current_user.id,
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    if file:
        client = storage.get_minio_client()
        upload_response = storage.upload_file(
            client, file, f"recipes/{new_recipe.id}", None
        )
        if upload_response:
            new_recipe.image_url = upload_response["public_url"]
            db.commit()
            db.refresh(new_recipe)

    recipe_data = _build_recipe_data(db, new_recipe)

    return CreateRecipeResponse(
        recipe=recipe_data,
        resultCode=ResultCode.SUCCESS_RECIPE_ADDED.value[0],
        resultMessage=ResultMessage(
            en="Recipe created successfully",
            vn=ResultCode.SUCCESS_RECIPE_ADDED.value[1],
        ),
    )


@router.get("/", response_model=GetRecipesResponse)
def get_recipes(
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

    recipes = db.query(Recipe).filter(Recipe.group_id == group_member.group_id).all()

    recipes_data = [_build_recipe_data(db, recipe) for recipe in recipes]

    return GetRecipesResponse(
        recipes=recipes_data,
        resultCode=ResultCode.SUCCESS_RECIPE_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Recipes fetched successfully",
            vn=ResultCode.SUCCESS_RECIPE_LIST_FETCHED.value[1],
        ),
    )


@router.post("/id/", response_model=GetRecipeByIdResponse)
def get_recipe_by_id(
    request: GetRecipeByIdRequest,
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

    recipe = db.query(Recipe).filter(Recipe.id == request.id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    if recipe.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this recipe",
        )

    recipe_data = _build_recipe_data(db, recipe)

    return GetRecipeByIdResponse(
        recipe=recipe_data,
        resultCode=ResultCode.SUCCESS_RECIPE_LIST_FETCHED.value[0],
        resultMessage=ResultMessage(
            en="Recipe fetched successfully",
            vn=ResultCode.SUCCESS_RECIPE_LIST_FETCHED.value[1],
        ),
    )


@router.put("/", response_model=UpdateRecipeResponse)
def update_recipe(
    id: int = Form(...),
    new_name: str | None = Form(None, alias="newName"),
    new_description: str | None = Form(None, alias="newDescription"),
    new_html_content: str | None = Form(None, alias="newHtmlContent"),
    new_food_name: str | None = Form(None, alias="newFoodName"),
    new_prep_time_minutes: int | None = Form(None, alias="newPrepTimeMinutes"),
    new_cook_time_minutes: int | None = Form(None, alias="newCookTimeMinutes"),
    new_servings: int | None = Form(None, alias="newServings"),
    new_difficulty: str | None = Form(None, alias="newDifficulty"),
    file: UploadFile = File(None),
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

    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    if recipe.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this recipe",
        )

    if new_name is not None:
        recipe.name = new_name

    if new_description is not None:
        recipe.description = new_description

    if new_html_content is not None:
        recipe.html_content = new_html_content

    if new_food_name is not None:
        food = (
            db.query(Food)
            .filter(
                Food.name == new_food_name,
                Food.group_id == group_member.group_id,
                Food.is_active == True,
            )
            .first()
        )
        if food:
            recipe.food_id = food.id

    if new_prep_time_minutes is not None:
        recipe.prep_time_minutes = new_prep_time_minutes

    if new_cook_time_minutes is not None:
        recipe.cook_time_minutes = new_cook_time_minutes

    if new_servings is not None:
        recipe.servings = new_servings

    if new_difficulty is not None:
        if new_difficulty not in ["easy", "medium", "hard"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Difficulty must be easy, medium, or hard",
            )
        recipe.difficulty = new_difficulty

    if file:
        client = storage.get_minio_client()
        upload_response = storage.upload_file(
            client, file, f"recipes/{recipe.id}", recipe.image_url
        )
        if upload_response:
            recipe.image_url = upload_response["public_url"]

    db.commit()
    db.refresh(recipe)

    recipe_data = _build_recipe_data(db, recipe)

    return UpdateRecipeResponse(
        recipe=recipe_data,
        resultCode=ResultCode.SUCCESS_RECIPE_UPDATED.value[0],
        resultMessage=ResultMessage(
            en="Recipe updated successfully",
            vn=ResultCode.SUCCESS_RECIPE_UPDATED.value[1],
        ),
    )


@router.delete("/", response_model=DeleteRecipeResponse)
def delete_recipe(
    request: DeleteRecipeRequest,
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

    recipe = db.query(Recipe).filter(Recipe.id == request.id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    if recipe.group_id != group_member.group_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this recipe",
        )

    db.delete(recipe)
    db.commit()

    return DeleteRecipeResponse(
        resultCode=ResultCode.SUCCESS_RECIPE_DELETED.value[0],
        resultMessage=ResultMessage(
            en="Recipe deleted successfully",
            vn=ResultCode.SUCCESS_RECIPE_DELETED.value[1],
        ),
    )


def _build_recipe_data(db: Session, recipe: Recipe) -> RecipeData:
    food_name = None
    if recipe.food_id:
        food = db.query(Food).filter(Food.id == recipe.food_id).first()
        food_name = food.name if food else None

    return RecipeData(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        html_content=recipe.html_content,
        food_id=recipe.food_id,
        food_name=food_name,
        group_id=recipe.group_id,
        prep_time_minutes=recipe.prep_time_minutes,
        cook_time_minutes=recipe.cook_time_minutes,
        servings=recipe.servings,
        difficulty=recipe.difficulty,
        image_url=recipe.image_url,
        is_public=recipe.is_public,
        created_by=recipe.created_by,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at,
    )


__all__ = ["router"]
