from sqlmodel import Session, select
from app.core.security import verify_password, get_password_hash
from app.models.user import User, UserIn


def register_user(session: Session, user: UserIn) -> User:
    db_user = session.exec(select(User).where(User.username == user.username)).one_or_none()
    if db_user:
        return None
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def authenticate_user(session: Session, user_name: str, password: str) -> User:
    user = session.exec(select(User).where(User.username == user_name)).one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user