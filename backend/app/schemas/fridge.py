from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from .base import BaseResponse


class FridgeItemData(BaseModel):
    id: int
    food_id: int = Field(..., alias="foodId")
    food_name: str = Field(..., alias="foodName")
    group_id: int = Field(..., alias="groupId")
    quantity: Decimal
    unit_id: int | None = Field(None, alias="unitId")
    unit_name: str | None = Field(None, alias="unitName")
    note: str | None = None
    purchase_date: date | None = Field(None, alias="purchaseDate")
    use_within_date: date = Field(..., alias="useWithinDate")
    location: str | None = None
    is_opened: bool = Field(..., alias="isOpened")
    opened_at: datetime | None = Field(None, alias="openedAt")
    cost: Decimal | None = None
    created_by: int = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CreateFridgeItemRequest(BaseModel):
    food_name: str = Field(..., min_length=1, max_length=100, alias="foodName")
    quantity: Decimal = Field(..., gt=0)
    unit_name: str | None = Field(None, max_length=20, alias="unitName")
    note: str | None = Field(None, max_length=500)
    purchase_date: date | None = Field(None, alias="purchaseDate")
    use_within_date: date = Field(..., alias="useWithinDate")
    location: str | None = Field(None, max_length=50)
    cost: Decimal | None = Field(None, ge=0)


class CreateFridgeItemResponse(BaseResponse):
    fridge_item: FridgeItemData = Field(..., alias="fridgeItem")

    model_config = {"by_alias": True, "populate_by_name": True}


class GetFridgeItemsRequest(BaseModel):
    pass


class GetFridgeItemsResponse(BaseResponse):
    fridge_items: list[FridgeItemData] = Field(..., alias="fridgeItems")

    model_config = {"by_alias": True, "populate_by_name": True}


class GetFridgeItemByIdRequest(BaseModel):
    id: int = Field(..., gt=0)


class GetFridgeItemByIdResponse(BaseResponse):
    fridge_item: FridgeItemData = Field(..., alias="fridgeItem")

    model_config = {"by_alias": True, "populate_by_name": True}


class UpdateFridgeItemRequest(BaseModel):
    id: int = Field(..., gt=0)
    new_quantity: Decimal | None = Field(None, gt=0, alias="newQuantity")
    new_note: str | None = Field(None, max_length=500, alias="newNote")
    new_use_within_date: date | None = Field(None, alias="newUseWithinDate")
    new_location: str | None = Field(None, max_length=50, alias="newLocation")
    is_opened: bool | None = Field(None, alias="isOpened")


class UpdateFridgeItemResponse(BaseResponse):
    fridge_item: FridgeItemData = Field(..., alias="fridgeItem")

    model_config = {"by_alias": True, "populate_by_name": True}


class DeleteFridgeItemRequest(BaseModel):
    id: int = Field(..., gt=0)


class DeleteFridgeItemResponse(BaseResponse):
    pass
