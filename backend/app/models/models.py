"""SQLAlchemy ORM models."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from ..database.database import Base


class Meal(Base):
    """Model for meal records."""

    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    calories = Column(Float, nullable=False)
    water_ml = Column(Float, nullable=False, default=0.0)
    logged_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Exercise(Base):
    """Model for exercise records."""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    calories_burned = Column(Float, nullable=False)
    duration_minutes = Column(Float, nullable=False)
    logged_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WeightLog(Base):
    """Model for weight log records."""

    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True, index=True)
    weight_kg = Column(Float, nullable=False)
    logged_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
