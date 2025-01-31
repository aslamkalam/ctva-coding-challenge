import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Rest_API.app.main import app
from Rest_API.app.database import Base, get_db  # Absolute import for database module
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the test database URL from environment variable
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable not set")

# Create SQLAlchemy engine for the test database
engine = create_engine(TEST_DATABASE_URL)

# Create a sessionmaker for test database sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")  # Database fixture (function scope)
def test_db():
    """
    Sets up and tears down the test database for each test function.

    Yields:
        A database session for the test.
    """
    Base.metadata.create_all(bind=engine)  # Create all tables in the test database
    db = TestingSessionLocal()  # Create a new session for the test
    try:
        yield db  # Provide the session to the test function
    finally:
        db.close()  # Close the session
        Base.metadata.drop_all(bind=engine)  # Drop all tables after the test

@pytest.fixture  # Test client fixture
def client(test_db):  # Inject the test_db fixture
    """
    Creates a test client with dependency override for the database.

    Args:
        test_db: The test database session fixture.

    Yields:
        A TestClient instance for making requests to the FastAPI application.
    """

    def override_get_db():  # Override the get_db dependency for testing
        """Provides the test database session to the application."""
        try:
            yield test_db  # Use the test database session in the application
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db  # Override the get_db dependency
    with TestClient(app) as c:  # Create a test client
        yield c  # Provide the test client to the test functions