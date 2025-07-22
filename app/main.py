from fastapi import FastAPI
from app.middlewares.exception import ExceptionMiddleware
from app.core.logging import setup_logging
from app.api.auth import router as auth_router

app = FastAPI(title="FastAPI Project")

# Setup logging
setup_logging()


# Add middleware
app.add_middleware(ExceptionMiddleware)


# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"}
