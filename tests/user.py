import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db, SessionLocal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import src.models as models

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)  # Create tables for the test DB

# Override dependency to use test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    yield db
    db.close()

# Test User Registration
def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["username"] == "testuser"

# Test User Registration with Duplicate Email
def test_register_duplicate_user():
    response = client.post("/register", json={
        "username": "testuser2",
        "email": "test@example.com",  # Same email as previous test
        "password": "testpass"
    })
    assert response.status_code == 400  # Assuming your API returns 400 for duplicate emails

# Test User Login (Successful)
def test_login_success():
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test User Login (Incorrect Password)
def test_login_wrong_password():
    response = client.post("/token", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401  # Unauthorized

# Test Fetching Current User Details
def test_get_current_user():
    token_response = client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })


    token = token_response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

# Test Fetching User Without Token (Unauthorized)
def test_get_current_user_no_token():
    response = client.get("/users/me")
    assert response.status_code == 401