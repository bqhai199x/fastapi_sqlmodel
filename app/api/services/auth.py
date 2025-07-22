from sqlmodel import Session, select
from app.core.security import verify_password
from app.models.user import User


def authenticate_user(session: Session, user_name: str, password: str) -> User:
    user = session.exec(select(User).where(User.username == user_name)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user