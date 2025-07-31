from sqlmodel import create_engine, Session, text, select
from app.core.config import settings
from sqlmodel import SQLModel, func
from app.models import User, UserRole
from app.helpers.constant import ROLE_ID
from app.core.security import get_password_hash


engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
    with next(get_session()) as session:
        if not session.exec(select(func.count(User.id))).one():
            print("Initializing database...")
            session.add_all([
                UserRole(id=ROLE_ID.ADMIN, permissions=[], is_superuser=True),
                UserRole(id=ROLE_ID.NORMAL_USER, permissions=[], is_superuser=False)
            ])
            session.add(User(id=1, username='admin', hashed_password=get_password_hash('admin123'), role_id=ROLE_ID.ADMIN))
            session.exec(text("SELECT setval('user_id_seq', (SELECT MAX(id) FROM \"user\"))"))
            session.exec(text("SELECT setval('user_role_id_seq', (SELECT MAX(id) FROM \"user_role\"))"))
            session.commit()
