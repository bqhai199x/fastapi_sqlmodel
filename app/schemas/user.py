from pydantic import BaseModel
from datetime import datetime


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    role: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
