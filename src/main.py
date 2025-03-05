from fastapi import FastAPI
import models, database
from .auth import auth_router
from .routes.blogs import blog_router
from .ai_agent import ai_router

# Initialize database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Blog Post Creation API")

app.include_router(blog_router, prefix="/api/v1/blogs")
app.include_router(ai_router, prefix="/api/v1/blogs/ai_generator")
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
def welcome():
    return {"message": "Welcome to the AI-Powered Blog Post Creation API!"}