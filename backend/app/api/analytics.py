from fastapi import APIRouter, Depends
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models import User, ShoppingList, ShoppingTask, Food, Category, FridgeItem
from ..schemas.analytics import (
    MonthlySpendingResponse,
    CategoryBreakdownResponse,
    CategoryData,
    AnalyticsSummaryResponse,
)
from ..schemas.base import ResultMessage

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/spending/monthly", response_model=MonthlySpendingResponse)
def get_monthly_spending(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns monthly spending aggregated by month for current group"""
    # Get user's current group
    group_id = current_user.belongs_to_group_admin_id

    if group_id is None:
        return MonthlySpendingResponse(
            months=[],
            amounts=[],
            budgets=[],
            resultCode="00201",
            resultMessage=ResultMessage(
                en="No group assigned",
                vn="Chưa có nhóm"
            ),
        )

    # Query last 12 months
    twelve_months_ago = datetime.now() - timedelta(days=365)

    results = (
        db.query(
            func.date_trunc("month", ShoppingList.created_at).label("month"),
            func.sum(ShoppingList.total_cost).label("amount"),
            func.sum(ShoppingList.budget).label("budget"),
        )
        .filter(
            ShoppingList.group_id == group_id,
            ShoppingList.status == "completed",
            ShoppingList.created_at >= twelve_months_ago,
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    months = [r.month.strftime("%Y-%m") for r in results]
    amounts = [float(r.amount) if r.amount else 0.0 for r in results]
    budgets = [float(r.budget) if r.budget else 0.0 for r in results]

    return MonthlySpendingResponse(
        months=months,
        amounts=amounts,
        budgets=budgets,
        resultCode="00201",
        resultMessage=ResultMessage(
            en="Monthly spending retrieved successfully",
            vn="Lấy chi tiêu hàng tháng thành công"
        ),
    )


@router.get("/categories/breakdown", response_model=CategoryBreakdownResponse)
def get_category_breakdown(
    month: str | None = None,  # Format: "2025-01"
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns spending breakdown by food category"""
    group_id = current_user.belongs_to_group_admin_id

    if group_id is None:
        return CategoryBreakdownResponse(
            categories=[],
            total=0.0,
            resultCode="00202",
            resultMessage=ResultMessage(
                en="No group assigned",
                vn="Chưa có nhóm"
            ),
        )

    query = (
        db.query(
            Category.name,
            func.sum(ShoppingTask.actual_cost).label("amount"),
            func.count(ShoppingTask.id).label("count"),
        )
        .join(Food, ShoppingTask.food_id == Food.id)
        .join(Category, Food.category_id == Category.id)
        .join(ShoppingList, ShoppingTask.list_id == ShoppingList.id)
        .filter(ShoppingList.group_id == group_id)
    )

    if month:
        # Filter by month
        try:
            start_date = datetime.strptime(month, "%Y-%m")
            # Get last day of month
            if start_date.month == 12:
                end_date = start_date.replace(year=start_date.year + 1, month=1, day=1)
            else:
                end_date = start_date.replace(month=start_date.month + 1, day=1)

            query = query.filter(
                ShoppingList.created_at >= start_date,
                ShoppingList.created_at < end_date,
            )
        except ValueError:
            pass  # Invalid date format, ignore filter

    results = query.group_by(Category.name).all()
    total = sum(float(r.amount) if r.amount else 0.0 for r in results)

    categories = [
        CategoryData(
            name=r.name,
            amount=float(r.amount) if r.amount else 0.0,
            percentage=(float(r.amount) if r.amount else 0.0) / total * 100
            if total > 0
            else 0.0,
            itemCount=r.count,
        )
        for r in results
    ]

    return CategoryBreakdownResponse(
        categories=categories,
        total=total,
        resultCode="00202",
        resultMessage=ResultMessage(
            en="Category breakdown retrieved successfully",
            vn="Lấy phân tích danh mục thành công"
        ),
    )


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns overall analytics summary"""
    group_id = current_user.belongs_to_group_admin_id

    if group_id is None:
        return AnalyticsSummaryResponse(
            totalSpent=0.0,
            totalBudget=0.0,
            averageShoppingTrip=0.0,
            fridgeValue=0.0,
            expiringSoonCount=0,
            resultCode="00203",
            resultMessage=ResultMessage(
                en="No group assigned",
                vn="Chưa có nhóm"
            ),
        )

    # Total spent (completed lists)
    total_spent = (
        db.query(func.sum(ShoppingList.total_cost))
        .filter(
            ShoppingList.group_id == group_id,
            ShoppingList.status == "completed",
        )
        .scalar()
        or 0
    )

    # Total budget
    total_budget = (
        db.query(func.sum(ShoppingList.budget))
        .filter(ShoppingList.group_id == group_id)
        .scalar()
        or 0
    )

    # Average shopping trip
    avg_trip = (
        db.query(func.avg(ShoppingList.total_cost))
        .filter(
            ShoppingList.group_id == group_id,
            ShoppingList.status == "completed",
        )
        .scalar()
        or 0
    )

    # Fridge value (sum of costs)
    fridge_value = (
        db.query(func.sum(FridgeItem.cost))
        .filter(FridgeItem.group_id == group_id)
        .scalar()
        or 0
    )

    # Expiring soon count (within 3 days)
    three_days_later = date.today() + timedelta(days=3)
    expiring_soon = (
        db.query(func.count(FridgeItem.id))
        .filter(
            FridgeItem.group_id == group_id,
            FridgeItem.use_within_date <= three_days_later,
            FridgeItem.use_within_date >= date.today(),
        )
        .scalar()
        or 0
    )

    return AnalyticsSummaryResponse(
        totalSpent=float(total_spent),
        totalBudget=float(total_budget),
        averageShoppingTrip=float(avg_trip),
        fridgeValue=float(fridge_value),
        expiringSoonCount=expiring_soon,
        resultCode="00203",
        resultMessage=ResultMessage(
            en="Analytics summary retrieved successfully",
            vn="Lấy tổng quan phân tích thành công"
        ),
    )


__all__ = ["router"]
