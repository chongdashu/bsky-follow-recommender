from fastapi import HTTPException, status


class BlueskyAuthError(HTTPException):
    """Exception raised for Bluesky authentication errors."""

    def __init__(self, detail: str = "Authentication with Bluesky failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class BlueskyAPIError(HTTPException):
    """Exception raised for Bluesky API errors."""

    def __init__(self, detail: str = "Error communicating with Bluesky API"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class RecommendationError(HTTPException):
    """Exception raised for recommendation generation errors."""

    def __init__(self, detail: str = "Error generating recommendations"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
