"""BioRitmo FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.database import init_db
from .routes import dashboard, exercises, meals, weight


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    init_db()
    yield


app = FastAPI(
    title="BioRitmo API",
    description="API para gestão de saúde: balanço calórico, hidratação e peso corporal.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meals.router, prefix="/api/v1")
app.include_router(exercises.router, prefix="/api/v1")
app.include_router(weight.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")


@app.get("/", tags=["root"])
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "BioRitmo API está rodando 🚀", "version": "1.0.0"}


@app.get("/health", tags=["root"])
def health_check():
    """Detailed health check."""
    return {"status": "healthy", "api": "BioRitmo", "version": "1.0.0"}
