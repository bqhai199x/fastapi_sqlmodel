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
