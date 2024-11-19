from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.

    Args:
        app: FastAPI application instance
    """
    # Startup: Add any async startup code here (DB connections, etc.)
    print("Starting up FastAPI application...")
    yield
    # Shutdown: Add any async cleanup code here
    print("Shutting down FastAPI application...")


# Create FastAPI app instance
app = FastAPI(
    title="Bluesky Recommendations API",
    description="API for providing Bluesky user recommendations",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint to verify API is running.

    Returns:
        dict: Basic API information
    """
    return {
        "status": "online",
        "service": "Bluesky Recommendations API",
        "version": "1.0.0",
    }


# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global HTTP exception handler.

    Args:
        request: The incoming request
        exc: The exception that was raised

    Returns:
        dict: Error details
    """
    return {"status": "error", "code": exc.status_code, "message": exc.detail}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
