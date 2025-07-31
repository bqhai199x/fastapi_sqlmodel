from fastapi import APIRouter, HTTPException, status
from app.models.user import AdminUserOut, AdminUpdateUser
from app.api.deps import SessionDep, require_admin
from app.api.services import user as user_service


router = APIRouter()


@router.get("/", response_model=list[AdminUserOut], dependencies=[require_admin()])
def get_users(session: SessionDep):
    return user_service.get_users(session)


@router.patch("/{id}", response_model=AdminUserOut, dependencies=[require_admin()])
def update_user(id: int, user_update: AdminUpdateUser, session: SessionDep):
    db_user = user_service.update_user(session, id, user_update)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
