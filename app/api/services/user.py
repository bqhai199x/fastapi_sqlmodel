from sqlmodel import Session, select
from app.models.user import User, AdminUpdateUser
from fastapi import HTTPException, status


def get_users(session: Session) -> list[User]:
    users = session.exec(select(User)).all()
    return users


def update_user(session: Session, user_id: int, user_update: AdminUpdateUser) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user
