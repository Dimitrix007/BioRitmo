"""Service layer for exercise operations."""

from datetime import date, datetime

from sqlalchemy.orm import Session

from ..models.models import Exercise
from ..schemas.schemas import ExerciseCreate, ExerciseUpdate


def get_exercise(db: Session, exercise_id: int) -> Exercise | None:
    """Get a single exercise by ID."""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_exercises(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    date_filter: date | None = None,
) -> list[Exercise]:
    """Get all exercises, optionally filtered by date."""
    query = db.query(Exercise)
    if date_filter:
        start = datetime.combine(date_filter, datetime.min.time())
        end = datetime.combine(date_filter, datetime.max.time())
        query = query.filter(Exercise.logged_at.between(start, end))
    return query.order_by(Exercise.logged_at.desc()).offset(skip).limit(limit).all()


def create_exercise(db: Session, exercise: ExerciseCreate) -> Exercise:
    """Create a new exercise record."""
    db_exercise = Exercise(
        name=exercise.name,
        description=exercise.description,
        calories_burned=exercise.calories_burned,
        duration_minutes=exercise.duration_minutes,
        logged_at=exercise.logged_at,
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def update_exercise(db: Session, exercise_id: int, exercise_update: ExerciseUpdate) -> Exercise | None:
    """Update an existing exercise record."""
    db_exercise = get_exercise(db, exercise_id)
    if not db_exercise:
        return None
    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exercise, field, value)
    db_exercise.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exercise_id: int) -> bool:
    """Delete an exercise record."""
    db_exercise = get_exercise(db, exercise_id)
    if not db_exercise:
        return False
    db.delete(db_exercise)
    db.commit()
    return True


def get_daily_exercise_summary(db: Session, target_date: date) -> dict:
    """Get aggregated exercise data for a specific date."""
    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())
    exercises = db.query(Exercise).filter(Exercise.logged_at.between(start, end)).all()
    return {
        "exercise_count": len(exercises),
        "total_calories_burned": sum(e.calories_burned for e in exercises),
        "total_duration_minutes": sum(e.duration_minutes for e in exercises),
    }
