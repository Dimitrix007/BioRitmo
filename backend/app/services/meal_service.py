"""Service layer for meal operations."""

from datetime import date, datetime

from sqlalchemy.orm import Session

from ..models.models import Meal
from ..schemas.schemas import MealCreate, MealUpdate


def get_meal(db: Session, meal_id: int) -> Meal | None:
    """Get a single meal by ID."""
    return db.query(Meal).filter(Meal.id == meal_id).first()


def get_meals(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    date_filter: date | None = None,
) -> list[Meal]:
    """Get all meals, optionally filtered by date."""
    query = db.query(Meal)
    if date_filter:
        start = datetime.combine(date_filter, datetime.min.time())
        end = datetime.combine(date_filter, datetime.max.time())
        query = query.filter(Meal.logged_at.between(start, end))
    return query.order_by(Meal.logged_at.desc()).offset(skip).limit(limit).all()


def create_meal(db: Session, meal: MealCreate) -> Meal:
    """Create a new meal record."""
    db_meal = Meal(
        name=meal.name,
        description=meal.description,
        calories=meal.calories,
        water_ml=meal.water_ml,
        logged_at=meal.logged_at,
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


def update_meal(db: Session, meal_id: int, meal_update: MealUpdate) -> Meal | None:
    """Update an existing meal record."""
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        return None
    update_data = meal_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meal, field, value)
    db_meal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_meal)
    return db_meal


def delete_meal(db: Session, meal_id: int) -> bool:
    """Delete a meal record."""
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        return False
    db.delete(db_meal)
    db.commit()
    return True


def get_daily_meal_summary(db: Session, target_date: date) -> dict:
    """Get aggregated meal data for a specific date."""
    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())
    meals = db.query(Meal).filter(Meal.logged_at.between(start, end)).all()
    return {
        "meal_count": len(meals),
        "total_calories": sum(m.calories for m in meals),
        "total_water_ml": sum(m.water_ml for m in meals),
    }
