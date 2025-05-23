from fastapi import HTTPException, status

class ValidationError(HTTPException):
    """Raised when request validation fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class GenerationError(HTTPException):
    """Raised when content generation fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class SearchError(HTTPException):
    """Raised when search operation fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        ) 