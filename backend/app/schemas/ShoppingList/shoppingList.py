from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# Shopping list data structure
class ShoppingListData(BaseModel):
    id: int
    name: str
    note: str
    belongs_to_group_admin_id: int = Field(..., alias="belongsToGroupAdminId")
    assigned_to_user_id: int = Field(..., alias="assignedToUserId")
    date: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")
    user_id: int = Field(..., alias="UserId")
    username: Optional[str] = None
    details: Optional[List[Any]] = []


# Task data structure for shopping lists
class TaskData(BaseModel):
    food_name: str = Field(..., alias="foodName")
    quantity: str


# Shopping list with tasks (for GET endpoint response)
class ShoppingListWithTasks(ShoppingListData):
    details: Optional[List[Any]] = []  # Can contain task details


# Create shopping list endpoint schemas
class CreateShoppingListRequest(BaseModel):
    name: str = Field(..., min_length=1)
    assign_to_username: str = Field(..., alias="assignToUsername", min_length=1)
    note: str
    date: str  # Format: mm/dd/yyyy


class CreateShoppingListResponse(BaseResponse):
    created_shopping_list: ShoppingListData = Field(..., alias="createdShoppingList")


# Update shopping list endpoint schemas
class UpdateShoppingListRequest(BaseModel):
    list_id: str = Field(..., alias="listId")
    new_name: str = Field(..., alias="newName", min_length=1)
    new_assign_to_username: str = Field(..., alias="newAssignToUsername", min_length=1)
    new_date: str = Field(..., alias="newDate")
    new_note: str = Field(..., alias="newNote")


class UpdateShoppingListResponse(BaseResponse):
    new_shopping_list: ShoppingListData = Field(..., alias="newShoppingList")


# Delete shopping list endpoint schemas
class DeleteShoppingListRequest(BaseModel):
    list_id: str = Field(..., alias="listId")


class DeleteShoppingListResponse(BaseResponse):
    pass  # Only base response structure needed


# Create tasks endpoint schemas
class CreateTasksRequest(BaseModel):
    list_id: int = Field(..., alias="listId")
    tasks: List[TaskData]


class CreateTasksResponse(BaseResponse):
    pass  # Only base response structure needed


# Get shopping tasks endpoint schemas
class GetShoppingTasksRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetShoppingTasksResponse(BaseResponse):
    role: str
    list: List[ShoppingListWithTasks] = []


# Delete task endpoint schemas
class DeleteTaskRequest(BaseModel):
    task_id: str = Field(..., alias="taskId")


class DeleteTaskResponse(BaseResponse):
    pass  # Only base response structure needed


# Update task endpoint schemas
class UpdateTaskRequest(BaseModel):
    task_id: str = Field(..., alias="taskId")
    new_food_name: str = Field(..., alias="newFoodName", min_length=1)


class UpdateTaskResponse(BaseResponse):
    pass  # Only base response structure needed


# Mark task as done/not done endpoint schemas
class MarkTaskRequest(BaseModel):
    task_id: str = Field(..., alias="taskId")


class MarkTaskResponse(BaseResponse):
    pass  # Only base response structure needed
