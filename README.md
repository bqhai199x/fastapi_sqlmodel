## Setup

1. Install Python 3.9+
2. Install PostgreSQL and Redis
3. Create virtual environment: `python -m venv .venv`
4. Activate: `source venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Configure `.env` with your DATABASE_URL and SECRET_KEY
7. Run migrations: 
   ```bash
   alembic revision --autogenerate -m "int"
   alembic upgrade head
   ```
8. Run `python -m app.core.db`
9. Run: `uvicorn app.main:app --reload` or `fastapi dev app/main.py`
