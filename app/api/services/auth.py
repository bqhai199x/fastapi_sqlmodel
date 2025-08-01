from sqlmodel import Session, select
from app.core.security import verify_password, get_password_hash, create_token, decode_token
from app.models.user import User, UserIn, UserChangePassword
from fastapi import HTTPException, status
from app.models.shared import Token, TokenPayload


def register_user(session: Session, user: UserIn) -> User:
    db_user = session.exec(select(User).where(User.username == user.username)).one_or_none()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def authenticate_user(session: Session, user_name: str, password: str) -> Token:
    user = session.exec(select(User).where(User.username == user_name)).one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token_payload = TokenPayload(sub=user.username, permissions=user.permissions, is_superuser=user.is_superuser)
    access_token = create_token(token_payload)
    refresh_token = create_token(token_payload, refresh=True)
    return Token(access_token=access_token, refresh_token=refresh_token)


def change_password(session: Session, user_update: UserChangePassword, current_user: User) -> User:
    if not verify_password(user_update.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )
    current_user.hashed_password = get_password_hash(user_update.new_password)
    session.commit()
    return current_user


def refresh_access_token(session: Session, token: str) -> Token:
    payload = decode_token(token, refresh=True)
    user = session.exec(select(User).where(User.username == payload.sub)).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    new_access_token = create_token(TokenPayload(sub=user.username, permissions=user.permissions, is_superuser=user.is_superuser))
    return Token(access_token=new_access_token, refresh_token=token)
