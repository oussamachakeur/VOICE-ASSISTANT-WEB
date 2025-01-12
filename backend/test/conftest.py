from fastapi.testclient import TestClient 
from backend.main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.database import get_db , Base
import pytest
from backend import schemas
from backend.ouath2 import create_access_token
from backend import mdls



database_url = "postgresql://postgres:kaddakadda@localhost:5432/SEproject_test"

engin = create_engine(database_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)



@pytest.fixture(scope="function")
def session():
    # Create the database tables
    Base.metadata.drop_all(bind=engin)
    Base.metadata.create_all(bind=engin)
    
    # Create a new session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    test_client = TestClient(app)
    yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
@pytest.fixture
def testUser(client):
    user_data = {
        "email": "test3@gmail.com",
        "password": "password123",  # Include the password here
        "first_name": "John",
        "last_name": "Doe"
    }
    res = client.post("/user", json=user_data)
    
    # Ensure the response has status code 201 (Created)
    assert res.status_code == 201, f"Failed to create test user: {res.json()}"
    
    # Return the user data along with the password for future use
    return res.json()  # Ensure the response contains the 'password' key