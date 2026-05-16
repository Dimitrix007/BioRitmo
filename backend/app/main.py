"""BioRitmo FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.database import init_db
from .routes import meals, exercises, weight, dashboard, foods

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    init_db()
    yield


app = FastAPI(
    title="BioRitmo API",
    description="Plataforma pessoal de gestão de saúde",
    version="1.1.0",
    contact={
        "name": "Dimitri Rafael Gomes Batista",          # ✅ troque para seu nome
        "url": "https://github.com/Dimitrix007",
    },
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
app.include_router(foods.router)


@app.get("/", tags=["root"])
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "BioRitmo API está rodando 🚀", "version": "1.0.0"}


@app.get("/health", tags=["root"])
def health_check():
    """Detailed health check."""
    return {"status": "healthy", "api": "BioRitmo", "version": "1.0.0"}
