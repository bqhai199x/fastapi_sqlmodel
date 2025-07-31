from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.user import User
from jwt.exceptions import InvalidTokenError
from app.core.config import settings
from typing import Annotated
import jwt


SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/token"))) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == username)).one()
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


class RequirePermissions:
    def __init__(self, permissions: set[str]):
        self.permissions = permissions

    def __call__(self, current_user: CurrentUserDep):
        if (not current_user.role.is_superuser and not set(self.permissions).issubset(set(current_user.role.permissions))):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to perform this action",
            )


def require_permissions(permissions: set[str]):
    return Depends(RequirePermissions(permissions))


class RequireAdmin:
    def __call__(self, current_user: CurrentUserDep):
        if not current_user.role.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have admin permissions to perform this action",
            )


def require_admin():
    return Depends(RequireAdmin())


class RequireAuthenticated:
    def __call__(self, current_user: CurrentUserDep):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )


def require_authenticated():
    return Depends(RequireAuthenticated())
