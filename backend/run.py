"""Script to run the FastAPI application using uvicorn."""

import uvicorn


def main() -> None:
    """
    Run the FastAPI application using uvicorn.

    This ensures we're using the correct uvicorn from our virtual environment.
    """
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
    )


if __name__ == "__main__":
    main()
