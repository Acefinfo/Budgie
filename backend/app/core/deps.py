from app.core.database import SessionLocal
from typing import Generator

def get_db() -> Generator:
    """
    Dependency function to obtain a database session for FastAPI request handlers.

    This function is designed to be used with FastAPI's dependency injection system.
    It will provide a new database session on each request and ensures that the 
    session is properly closed after the request is processed.

    Yields:
        db (Session): A SQLAlchemy database session that can be used for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

