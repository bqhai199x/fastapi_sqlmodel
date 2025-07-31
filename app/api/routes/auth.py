from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from app.models.user import User, UserIn, UserOut, UserChangePassword
from app.models.shared import Token
from app.core.security import get_password_hash, create_access_token, verify_password
from app.api.deps import SessionDep, CurrentUserDep
from app.api.services import auth as auth_service


router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserIn, session: SessionDep):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/token", response_model=Token)
def login(session: SessionDep, login_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(session, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserOut)
def get_me(current_user: CurrentUserDep):
    return current_user


@router.patch("/change-password", response_model=UserOut)
def change_password(user_update: UserChangePassword, current_user: CurrentUserDep, session: SessionDep):
    if not verify_password(user_update.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )
    current_user.hashed_password = get_password_hash(user_update.new_password)
    session.commit()
    return current_user
