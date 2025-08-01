from sqlmodel import create_engine, Session, text, select
from app.core.config import settings
from sqlmodel import SQLModel, func
from app.models import User
from app.core.security import get_password_hash


engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    try:
        SQLModel.metadata.create_all(engine)
        with next(get_session()) as session:
            if not session.exec(select(func.count(User.id))).one():
                print("Initializing database...")
                session.add(User(id=1, username='admin', hashed_password=get_password_hash('admin123'), is_superuser=True))
                session.exec(text("SELECT setval('user_id_seq', 2)"))
                session.commit()
    except Exception as e:
        print("Database initialization failed", f"Error: {e}", sep="\n")
