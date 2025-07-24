from fastapi import FastAPI
from app.middlewares.exception import ExceptionMiddleware
from app.api.main import api_router


app = FastAPI(title="FastAPI Project")


# Add middleware
app.add_middleware(ExceptionMiddleware)


# Include routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"}
