from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.models.role import UserRole, UserRoleOut
from app.helpers.constant import ROLE_ID
from app.helpers.custom_exception import RequestError


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=50, min_length=3)


class User(UserBase, table=True):
    __tablename__ = 'user'

    id: int | None = Field(primary_key=True)
    hashed_password: str = Field(max_length=255)
    is_active: bool = True
    role_id: int = Field(default=ROLE_ID.NORMAL_USER, foreign_key="user_role.id")
    role: UserRole = Relationship()
    created_at: datetime = Field(default_factory=datetime.now)


class UserIn(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserOut(UserBase):
    id: int
    role: UserRoleOut


class UserChangePassword(SQLModel):
    old_password: str
    new_password: str = Field(min_length=6, max_length=128)


class AdminUpdateUser(SQLModel):
    role_id: int | None = None
    is_active: bool | None = None

    def __init__(self, **data):
        super().__init__(**data)
        if "role_id" in data and self.role_id not in ROLE_ID.values():
            raise RequestError(field="role_id", message="Invalid role_id")


class AdminUserOut(UserOut):
    role_id: int
    is_active: bool
