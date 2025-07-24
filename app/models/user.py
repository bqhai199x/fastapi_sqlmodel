from sqlmodel import SQLModel, Field
from datetime import datetime


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=50, min_length=3)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=255)
    is_active: bool = True
    role: int = 0
    created_at: datetime = Field(default_factory=datetime.now)


class UserIn(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserOut(UserBase):
    id: int
    role: int
