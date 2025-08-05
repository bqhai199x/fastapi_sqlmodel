from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.user import User
from typing import Annotated
from app.core.security import decode_token
from app.helpers.custom_exception import credentials_exception, permissions_exception


TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/token"))]


SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    payload = decode_token(token)
    if not payload.sub:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == payload.sub, User.is_active)).one_or_none()
    if not user:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


class RequirePermissions:
    def __init__(self, permissions: set[int]):
        self.permissions = permissions

    def __call__(self, token: TokenDep):
        payload = decode_token(token)
        if not payload.is_superuser and not self.permissions.issubset(payload.permissions):
            raise permissions_exception


def require_permissions(permissions: set[int]):
    return Depends(RequirePermissions(permissions))


class RequireAdmin:
    def __call__(self, token: TokenDep):
        payload = decode_token(token)
        if not payload.is_superuser:
            raise permissions_exception


def require_admin():
    return Depends(RequireAdmin())


class RequireAuthenticated:
    def __call__(self, token: TokenDep):
        payload = decode_token(token)
        if not payload.sub:
            raise credentials_exception


def require_authenticated():
    return Depends(RequireAuthenticated())
