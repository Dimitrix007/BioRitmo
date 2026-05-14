"""Routes for weight log CRUD operations."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas import WeightLogCreate, WeightLogResponse, WeightLogUpdate
from ..services import weight_service

router = APIRouter(prefix="/weight", tags=["weight"])


@router.get("/", response_model=list[WeightLogResponse])
def list_weight_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    date_filter: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    """List all weight logs with optional date filter."""
    return weight_service.get_weight_logs(db, skip=skip, limit=limit, date_filter=date_filter)


@router.get("/{log_id}", response_model=WeightLogResponse)
def get_weight_log(log_id: int, db: Session = Depends(get_db)):
    """Get a single weight log by ID."""
    log = weight_service.get_weight_log(db, log_id)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de peso não encontrado")
    return log


@router.post("/", response_model=WeightLogResponse, status_code=status.HTTP_201_CREATED)
def create_weight_log(log: WeightLogCreate, db: Session = Depends(get_db)):
    """Create a new weight log."""
    return weight_service.create_weight_log(db, log)


@router.put("/{log_id}", response_model=WeightLogResponse)
def update_weight_log(log_id: int, log_update: WeightLogUpdate, db: Session = Depends(get_db)):
    """Update an existing weight log."""
    log = weight_service.update_weight_log(db, log_id, log_update)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de peso não encontrado")
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weight_log(log_id: int, db: Session = Depends(get_db)):
    """Delete a weight log."""
    deleted = weight_service.delete_weight_log(db, log_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de peso não encontrado")
