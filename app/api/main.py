from fastapi import APIRouter
from app.api.routes import auth


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
