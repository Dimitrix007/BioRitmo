"""Routes for meal CRUD operations."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..schemas.schemas import MealCreate, MealResponse, MealUpdate
from ..services import meal_service

router = APIRouter(prefix="/meals", tags=["meals"])


@router.get("/", response_model=list[MealResponse])
def list_meals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    date_filter: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    """List all meals with optional date filter."""
    return meal_service.get_meals(db, skip=skip, limit=limit, date_filter=date_filter)


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    """Get a single meal by ID."""
    meal = meal_service.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refeição não encontrada")
    return meal


@router.post("/", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    """Create a new meal record."""
    return meal_service.create_meal(db, meal)


@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(meal_id: int, meal_update: MealUpdate, db: Session = Depends(get_db)):
    """Update an existing meal record."""
    meal = meal_service.update_meal(db, meal_id, meal_update)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refeição não encontrada")
    return meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    """Delete a meal record."""
    deleted = meal_service.delete_meal(db, meal_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refeição não encontrada")
