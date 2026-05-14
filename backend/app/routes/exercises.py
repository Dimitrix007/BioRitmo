"""Routes for exercise CRUD operations."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from ..services import exercise_service

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExerciseResponse])
def list_exercises(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    date_filter: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    """List all exercises with optional date filter."""
    return exercise_service.get_exercises(db, skip=skip, limit=limit, date_filter=date_filter)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get a single exercise by ID."""
    exercise = exercise_service.get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")
    return exercise


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    """Create a new exercise record."""
    return exercise_service.create_exercise(db, exercise)


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(exercise_id: int, exercise_update: ExerciseUpdate, db: Session = Depends(get_db)):
    """Update an existing exercise record."""
    exercise = exercise_service.update_exercise(db, exercise_id, exercise_update)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Delete an exercise record."""
    deleted = exercise_service.delete_exercise(db, exercise_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")
