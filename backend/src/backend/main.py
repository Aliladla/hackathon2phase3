"""Main FastAPI application."""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from backend.config import settings
from backend.database import create_db_and_tables
from backend.api import auth_router, tasks_router

# Validate configuration on startup
settings.validate()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Todo Full-Stack Web Application - Backend API",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check response model
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and deployment.

    Returns application status and version.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.APP_VERSION
    )


# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
