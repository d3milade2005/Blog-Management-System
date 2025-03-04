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
    response = client.post("/register", json={"username": "testuser", "email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

# Test User Login & Token Generation
def test_login():
    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test Creating a Blog
def test_create_blog():
    token_response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = token_response.json()["access_token"]

    response = client.post("/blogs/", json={"title": "Test Blog", "content": "This is a test blog."},
                           headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["title"] == "Test Blog"

# Test Getting All Blogs
def test_get_blogs():
    response = client.get("/blogs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test Getting a Single Blog
def test_get_blog_by_id():
    response = client.get("/blogs/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# Test Updating a Blog
def test_update_blog():
    token_response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = token_response.json()["access_token"]

    response = client.put("/blogs/1", json={"title": "Updated Title", "content": "Updated content."},
                          headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

# Test Deleting a Blog
def test_delete_blog():
    token_response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = token_response.json()["access_token"]

    response = client.delete("/blogs/1", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Blog deleted successfully"
