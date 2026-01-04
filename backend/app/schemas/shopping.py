from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from .base import BaseResponse


class ShoppingListData(BaseModel):
    id: int
    name: str
    description: str | None = None
    group_id: int = Field(..., alias="groupId")
    assign_to_user_id: int | None = Field(None, alias="assignToUserId")
    assign_to_username: str | None = Field(None, alias="assignToUsername")
    due_date: date | None = Field(None, alias="dueDate")
    priority: str
    status: str
    budget: Decimal | None = None
    total_cost: Decimal = Field(..., alias="totalCost")
    is_archived: bool = Field(..., alias="isArchived")
    created_by: int = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class ShoppingTaskData(BaseModel):
    id: int
    list_id: int = Field(..., alias="listId")
    food_id: int = Field(..., alias="foodId")
    food_name: str = Field(..., alias="foodName")
    quantity: Decimal
    unit_id: int | None = Field(None, alias="unitId")
    unit_name: str | None = Field(None, alias="unitName")
    note: str | None = None
    estimated_cost: Decimal | None = Field(None, alias="estimatedCost")
    actual_cost: Decimal | None = Field(None, alias="actualCost")
    priority: str
    is_done: bool = Field(..., alias="isDone")
    done_at: datetime | None = Field(None, alias="doneAt")
    done_by: int | None = Field(None, alias="doneBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CreateShoppingListRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    assign_to_username: str | None = Field(None, max_length=50, alias="assignToUsername")
    due_date: date | None = Field(None, alias="dueDate")
    priority: str = Field(default="medium")
    budget: Decimal | None = Field(None, ge=0)


class CreateShoppingListResponse(BaseResponse):
    shopping_list: ShoppingListData = Field(..., alias="shoppingList")

    model_config = {"by_alias": True, "populate_by_name": True}


class GetShoppingListsRequest(BaseModel):
    pass


class GetShoppingListsResponse(BaseResponse):
    shopping_lists: list[ShoppingListData] = Field(..., alias="shoppingLists")

    model_config = {"by_alias": True, "populate_by_name": True}


class GetShoppingListByIdRequest(BaseModel):
    id: int = Field(..., gt=0)


class GetShoppingListByIdResponse(BaseResponse):
    shopping_list: ShoppingListData = Field(..., alias="shoppingList")
    tasks: list[ShoppingTaskData]

    model_config = {"by_alias": True, "populate_by_name": True}


class UpdateShoppingListRequest(BaseModel):
    id: int = Field(..., gt=0)
    new_name: str | None = Field(None, min_length=1, max_length=100, alias="newName")
    new_assign_to_username: str | None = Field(None, max_length=50, alias="newAssignToUsername")
    new_due_date: date | None = Field(None, alias="newDueDate")
    new_status: str | None = Field(None, alias="newStatus")
    new_priority: str | None = Field(None, alias="newPriority")
    new_budget: Decimal | None = Field(None, ge=0, alias="newBudget")


class UpdateShoppingListResponse(BaseResponse):
    shopping_list: ShoppingListData = Field(..., alias="shoppingList")

    model_config = {"by_alias": True, "populate_by_name": True}


class DeleteShoppingListRequest(BaseModel):
    id: int = Field(..., gt=0)


class DeleteShoppingListResponse(BaseResponse):
    pass


class TaskInput(BaseModel):
    food_id: int = Field(..., alias="foodId", gt=0)
    quantity: Decimal = Field(..., gt=0)
    unit_id: int | None = Field(None, alias="unitId", gt=0)
    note: str | None = Field(None, max_length=500)
    estimated_cost: Decimal | None = Field(None, ge=0, alias="estimatedCost")
    priority: str = Field(default="medium")

    model_config = {"populate_by_name": True}


class CreateShoppingTasksRequest(BaseModel):
    list_id: int = Field(..., gt=0, alias="listId")
    tasks: list[TaskInput]


class CreateShoppingTasksResponse(BaseResponse):
    tasks: list[ShoppingTaskData]


class UpdateShoppingTaskRequest(BaseModel):
    task_id: int = Field(..., gt=0, alias="taskId")
    new_quantity: Decimal | None = Field(None, gt=0, alias="newQuantity")
    new_note: str | None = Field(None, max_length=500, alias="newNote")
    new_estimated_cost: Decimal | None = Field(None, ge=0, alias="newEstimatedCost")
    actual_cost: Decimal | None = Field(None, ge=0, alias="actualCost")
    is_done: bool | None = Field(None, alias="isDone")


class UpdateShoppingTaskResponse(BaseResponse):
    task: ShoppingTaskData


class DeleteShoppingTaskRequest(BaseModel):
    task_id: int = Field(..., gt=0, alias="taskId")


class DeleteShoppingTaskResponse(BaseResponse):
    pass
