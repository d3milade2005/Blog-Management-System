from fastapi import APIRouter
from src.ai_agent import generate_and_save_blog

ai_router = APIRouter()

@ai_router.post("/generate-blog/")
def generate_blog(topic: str):
    """
    API endpoint to generate a blog post using AI.
    """
    content = generate_and_save_blog(topic)
    return {"topic": topic, "content": content}