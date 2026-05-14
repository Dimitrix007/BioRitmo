"""Routes for dashboard summary data."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas import DailySummary
from ..services import exercise_service, meal_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

WATER_GOAL_ML = 2000.0


@router.get("/summary", response_model=DailySummary)
def get_daily_summary(
    target_date: date = None,
    db: Session = Depends(get_db),
):
    """Get the daily health summary for the dashboard."""
    if target_date is None:
        target_date = date.today()

    meal_summary = meal_service.get_daily_meal_summary(db, target_date)
    exercise_summary = exercise_service.get_daily_exercise_summary(db, target_date)

    total_consumed = meal_summary["total_calories"]
    total_burned = exercise_summary["total_calories_burned"]
    total_water = meal_summary["total_water_ml"]
    water_pct = min((total_water / WATER_GOAL_ML) * 100, 100)

    return DailySummary(
        date=target_date.isoformat(),
        total_calories_consumed=total_consumed,
        total_calories_burned=total_burned,
        caloric_balance=total_consumed - total_burned,
        total_water_ml=total_water,
        water_goal_ml=WATER_GOAL_ML,
        water_progress_pct=round(water_pct, 1),
        meal_count=meal_summary["meal_count"],
        exercise_count=exercise_summary["exercise_count"],
    )
