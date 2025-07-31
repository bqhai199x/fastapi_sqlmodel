from fastapi import APIRouter
from app.api.routes import auth
from app.api.routes import user


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
