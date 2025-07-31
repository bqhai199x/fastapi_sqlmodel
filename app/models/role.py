from sqlmodel import SQLModel, Field, ARRAY, Integer


class UserRoleBase(SQLModel):
    permissions: set[int] = Field(default_factory=list, sa_type=ARRAY(Integer))
    is_superuser: bool = False


class UserRole(UserRoleBase, table=True):
    __tablename__ = 'user_role'

    id: int | None = Field(primary_key=True)


class UserRoleIn(UserRoleBase):
    pass


class UserRoleOut(UserRoleBase):
    pass
