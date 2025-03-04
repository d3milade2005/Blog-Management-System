# Blog-Management-System
# AI-Powered Blog Post Generator

An API-driven blog post management system built with **FastAPI**. This system supports **user authentication, blog CRUD operations**, and is designed for seamless AI integration in the future.

## Features
✅ Secure user authentication with JWT  
✅ CRUD operations for managing blog posts  
✅ SQLite database with SQLAlchemy & Alembic  
✅ Well-structured FastAPI endpoints  
✅ Fully tested with `pytest`


## Setup Instructions

### Clone the Repository
```sh
git clone https://github.com/your-username/Blog-Management-System.git
cd Blog-Management System
```

### Create a Virtual Environment
```sh
python -m venv env
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file:
```sh
# OPENAI_API_KEY=your-openai-api-key  # (Commented out until AI is implemented)
# LITELLM_API_KEY=your-litellm-key    # (Commented out until AI is implemented)
SECRET_KEY = "generate a secret key"
ALGORITHM = ""
ACCESS_TOKEN_EXPIRE_MINUTES = 
```

### **5️⃣ Apply Database Migrations**
```sh
alembic revision --autogenerate -m "migration"
alembic upgrade head
```

### Run the FastAPI Server
```sh
uvicorn app.main:app --reload
```

### Test the API
Check the **Swagger UI**:
```
http://127.0.0.1:8000/docs
```
Or use **Postman/cURL**:
```sh
curl -X GET "http://127.0.0.1:8000/api/v1/blogs/"
```

## Endpoints

| Method | Endpoint                         | Description                  |
|--------|----------------------------------|------------------------------|
| POST   | `/api/v1/users/register`        | Register a new user          |
| POST   | `/api/v1/users/login`           | User authentication (JWT)    |
| POST   | `/api/v1/blogs/`                | Create a new blog post       |
| GET    | `/api/v1/blogs/{id}`            | Get a single blog post       |


## Design Decisions & Rationale
- **FastAPI** was chosen for its async capabilities and automatic API documentation.
- **SQLite + SQLAlchemy** for an easy-to-setup database.
- **Alembic** for managing database migrations.
- **JWT authentication** for secure user access.
- **`pytest`** for automated testing.

## Assumptions Made
- Users must authenticate before creating blogs.

##  Future Improvements
🔹 Add **AI integration for automatic blog generation**.  
