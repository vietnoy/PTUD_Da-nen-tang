from pydantic import BaseModel, Field
from decimal import Decimal

from .base import BaseResponse


class MonthlySpendingResponse(BaseResponse):
    months: list[str]
    amounts: list[float]
    budgets: list[float]


class CategoryData(BaseModel):
    name: str
    amount: float
    percentage: float
    item_count: int = Field(..., alias="itemCount")

    model_config = {"populate_by_name": True}


class CategoryBreakdownResponse(BaseResponse):
    categories: list[CategoryData]
    total: float


class AnalyticsSummaryResponse(BaseResponse):
    total_spent: float = Field(..., alias="totalSpent")
    total_budget: float = Field(..., alias="totalBudget")
    average_shopping_trip: float = Field(..., alias="averageShoppingTrip")
    fridge_value: float = Field(..., alias="fridgeValue")
    expiring_soon_count: int = Field(..., alias="expiringSoonCount")

    model_config = {"populate_by_name": True, "by_alias": True}
