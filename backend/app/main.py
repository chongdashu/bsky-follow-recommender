"""Main FastAPI application initialization."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title="Blue Sky Follow Recommender",
    description="API for recommending Blue Sky users to follow",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify API is running.

    Returns:
        dict: Status message indicating the API is running
    """
    return {"status": "healthy"}
