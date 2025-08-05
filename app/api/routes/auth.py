from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserIn, UserOut, UserChangePassword
from app.models.shared import Token
from app.api.deps import SessionDep, CurrentUserDep, TokenDep
from app.api.services import auth as auth_service


router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserIn, session: SessionDep):
    return auth_service.register_user(session, user)


@router.post("/token", response_model=Token)
def login(session: SessionDep, login_data: OAuth2PasswordRequestForm = Depends()):
    return auth_service.authenticate_user(session, login_data.username, login_data.password)


@router.get("/me", response_model=UserOut)
def get_me(current_user: CurrentUserDep):
    return current_user


@router.put("/change-password", response_model=UserOut)
def change_password(user_update: UserChangePassword, current_user: CurrentUserDep, session: SessionDep):
    return auth_service.change_password(session, user_update, current_user)


@router.get("/refresh", response_model=Token)
def refresh_access_token(token: str, session: SessionDep):
    return auth_service.refresh_access_token(session, token)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: TokenDep):
    auth_service.logout_user(token)