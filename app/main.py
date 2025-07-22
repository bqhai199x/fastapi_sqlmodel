from fastapi import FastAPI
from app.middlewares.exception import ExceptionMiddleware
from app.core.logging import setup_logging
from app.api.main import api_router
from alembic.config import Config
from alembic import command
from contextlib import asynccontextmanager
import asyncio

# Setup logging
log = setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await asyncio.to_thread(command.upgrade, Config("alembic.ini"), "head")
    yield


app = FastAPI(title="FastAPI Project", lifespan=lifespan)


# Add middleware
app.add_middleware(ExceptionMiddleware)


# Include routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"}
