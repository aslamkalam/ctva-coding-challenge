
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL  # Import the database URL from the config module

# Create a SQLAlchemy engine using the database URL from the configuration
engine = create_engine(DATABASE_URL)

# Create a sessionmaker for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models
Base = declarative_base()