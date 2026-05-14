"""Pydantic schemas for data validation and serialization."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# ─── Meal Schemas ────────────────────────────────────────────────────────────


class MealBase(BaseModel):
    """Base schema for meals."""

    name: str = Field(..., min_length=1, max_length=100, description="Name of the meal")
    description: str | None = Field(None, description="Optional description")
    calories: float = Field(..., gt=0, description="Calories consumed")
    water_ml: float = Field(0.0, ge=0, description="Water intake in milliliters")
    logged_at: datetime = Field(default_factory=datetime.utcnow, description="When the meal was consumed")

    @field_validator("calories")
    @classmethod
    def calories_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Calories must be greater than 0")
        return v


class MealCreate(MealBase):
    """Schema for creating a meal."""

    pass


class MealUpdate(BaseModel):
    """Schema for updating a meal (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    calories: float | None = Field(None, gt=0)
    water_ml: float | None = Field(None, ge=0)
    logged_at: datetime | None = None


class MealResponse(MealBase):
    """Schema for meal responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Exercise Schemas ─────────────────────────────────────────────────────────


class ExerciseBase(BaseModel):
    """Base schema for exercises."""

    name: str = Field(..., min_length=1, max_length=100, description="Name of the exercise")
    description: str | None = Field(None, description="Optional description")
    calories_burned: float = Field(..., gt=0, description="Calories burned")
    duration_minutes: float = Field(..., gt=0, description="Duration in minutes")
    logged_at: datetime = Field(default_factory=datetime.utcnow, description="When the exercise was performed")

    @field_validator("calories_burned", "duration_minutes")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be greater than 0")
        return v


class ExerciseCreate(ExerciseBase):
    """Schema for creating an exercise."""

    pass


class ExerciseUpdate(BaseModel):
    """Schema for updating an exercise (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    calories_burned: float | None = Field(None, gt=0)
    duration_minutes: float | None = Field(None, gt=0)
    logged_at: datetime | None = None


class ExerciseResponse(ExerciseBase):
    """Schema for exercise responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Weight Schemas ───────────────────────────────────────────────────────────


class WeightLogBase(BaseModel):
    """Base schema for weight logs."""

    weight_kg: float = Field(..., gt=0, lt=500, description="Weight in kilograms")
    logged_at: datetime = Field(default_factory=datetime.utcnow, description="When the weight was logged")

    @field_validator("weight_kg")
    @classmethod
    def weight_must_be_realistic(cls, v: float) -> float:
        if v <= 0 or v >= 500:
            raise ValueError("Weight must be between 0 and 500 kg")
        return v


class WeightLogCreate(WeightLogBase):
    """Schema for creating a weight log."""

    pass


class WeightLogUpdate(BaseModel):
    """Schema for updating a weight log (all fields optional)."""

    weight_kg: float | None = Field(None, gt=0, lt=500)
    logged_at: datetime | None = None


class WeightLogResponse(WeightLogBase):
    """Schema for weight log responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Dashboard Schema ─────────────────────────────────────────────────────────


class DailySummary(BaseModel):
    """Schema for dashboard daily summary."""

    date: str
    total_calories_consumed: float
    total_calories_burned: float
    caloric_balance: float
    total_water_ml: float
    water_goal_ml: float
    water_progress_pct: float
    meal_count: int
    exercise_count: int
