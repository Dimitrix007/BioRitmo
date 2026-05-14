"""Service layer for weight log operations."""

from datetime import date, datetime

from sqlalchemy.orm import Session

from ..models.models import WeightLog
from ..schemas.schemas import WeightLogCreate, WeightLogUpdate


def get_weight_log(db: Session, log_id: int) -> WeightLog | None:
    """Get a single weight log by ID."""
    return db.query(WeightLog).filter(WeightLog.id == log_id).first()


def get_weight_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    date_filter: date | None = None,
) -> list[WeightLog]:
    """Get all weight logs, optionally filtered by date."""
    query = db.query(WeightLog)
    if date_filter:
        start = datetime.combine(date_filter, datetime.min.time())
        end = datetime.combine(date_filter, datetime.max.time())
        query = query.filter(WeightLog.logged_at.between(start, end))
    return query.order_by(WeightLog.logged_at.asc()).offset(skip).limit(limit).all()


def create_weight_log(db: Session, log: WeightLogCreate) -> WeightLog:
    """Create a new weight log record."""
    db_log = WeightLog(
        weight_kg=log.weight_kg,
        logged_at=log.logged_at,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_weight_log(db: Session, log_id: int, log_update: WeightLogUpdate) -> WeightLog | None:
    """Update an existing weight log."""
    db_log = get_weight_log(db, log_id)
    if not db_log:
        return None
    update_data = log_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_log, field, value)
    db_log.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_weight_log(db: Session, log_id: int) -> bool:
    """Delete a weight log record."""
    db_log = get_weight_log(db, log_id)
    if not db_log:
        return False
    db.delete(db_log)
    db.commit()
    return True
