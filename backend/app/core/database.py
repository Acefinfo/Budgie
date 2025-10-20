from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# Create the SQLAlchemy engine for database connection using the provided DATABASE_URL
# The 'pool_pre_ping' option ensures that the connection is checked before each use.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a session factory that will allow interaction with the database.
# autocommit=False: Disables automatic commits; transactions must be explicitly committed.
# autoflush=False: Disables automatic flushing, meaning changes aren't written to the DB until commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency function for getting a new database session.

    This function is used with FastAPI's dependency injection system. It creates
    a new database session that can be used in request handlers and automatically
    closes the session when the request is finished.

    Yields:
        db (Session): A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()