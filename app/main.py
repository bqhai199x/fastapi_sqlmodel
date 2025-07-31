from fastapi import FastAPI
from app.middlewares.exception_handler import validation_exception_handler
from app.api.main import api_router
from app.core.db import init_db
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError


# Initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="FastAPI Project", lifespan=lifespan)


# Add custom exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Include routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"}
