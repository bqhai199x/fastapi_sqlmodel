from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def validation_exception_handler(_, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        print(f"Validation error: {error}")
        errors.append({
            "source": error["loc"][0],
            "field": ".".join(error["loc"][1:]),
            "message": error["msg"],
        })

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )
