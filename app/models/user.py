from sqlalchemy import Integer
from sqlmodel import ARRAY, SQLModel, Field, text
from datetime import datetime


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=50, min_length=3)


class User(UserBase, table=True):
    __tablename__ = 'user'

    id: int | None = Field(primary_key=True)
    hashed_password: str = Field(max_length=255)
    permissions: set[int] = Field(default_factory=list, sa_type=ARRAY(Integer))
    is_superuser: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})
    is_active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")})


class UserIn(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserOut(UserBase):
    id: int
    permissions: set[int] = Field(default_factory=list, sa_type=ARRAY(Integer))
    is_superuser: bool = False


class UserChangePassword(SQLModel):
    old_password: str
    new_password: str = Field(min_length=6, max_length=128)


class AdminUpdateUser(SQLModel):
    is_superuser: bool | None = None
    permissions: set[int] | None = None
    is_active: bool | None = None


class AdminUserOut(UserOut):
    is_superuser: bool | None = None
    permissions: set[int] | None = None
    is_active: bool
