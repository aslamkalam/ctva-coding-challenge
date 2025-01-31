from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from .config import DATABASE_URL  # Import from the local config module

# Create the SQLAlchemy engine using the provided database URL
engine = create_engine(DATABASE_URL)

# Create a sessionmaker for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Creates a database session and yields it to the caller.

    This function provides a context manager-like behavior for managing database
    sessions. The session is automatically closed within the `finally` block
    regardless of whether exceptions occur during its use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()