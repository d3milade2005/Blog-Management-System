from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from smol_blogwriter import write_blog_post
from fastapi import BackgroundTasks
from src.schemas import BlogCreate, BlogResponse, UserResponse
from src.auth import get_current_user
from src.models import Blog
from src.database import get_db
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

load_dotenv()

ai_router = APIRouter()

# Set up OpenAI key
openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_blog_post_async(title: str) -> str:
    response = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Write a detailed blog post about {title}"}],
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Create a new blog post using AI agent
@ai_router.post("/", response_model=BlogResponse)
async def create_blog_post_with_ai(blog_post: BlogCreate, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    content = await generate_blog_post_async(blog_post.title)
    new_blog_post = Blog(title=blog_post.title, content=content, author_id=current_user)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post