from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    refresh_token: str


class TokenPayload(SQLModel):
    sub: str
    permissions: set[int]
    is_superuser: bool
