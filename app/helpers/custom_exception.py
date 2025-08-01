from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic_core import ErrorDetails


class RequestError(RequestValidationError):
    def __init__(self, field: str, message: str, source: str = "body"):
        error_details = [
            ErrorDetails(
                loc=(source, field),
                msg=message,
            )
        ]
        super().__init__(error_details)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated"
)


permissions_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied"
)
