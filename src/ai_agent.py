from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# from smol_blogwriter import write_blog_post
from fastapi import BackgroundTasks
from schemas import BlogCreate, BlogResponse, UserResponse
from auth import get_current_user
from models import Blog
from database import get_db
from dotenv import load_dotenv
import os
import asyncio
import openai

load_dotenv()

ai_router = APIRouter()

# Set up OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

import openai

async def generate_blog_post_async(title: str) -> str:
    response = await openai.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Write a detailed blog post about {title}"}],
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()



# Create a new blog post using AI agent
@ai_router.post("/", response_model=BlogResponse)
async def create_blog_post_with_ai(blog_post: BlogCreate, background_tasks: BackgroundTasks, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    db_blog_post = Blog(title=blog_post.title, content="", author_id=current_user)
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)

    async def generate_blog_content_and_update():
        # content = write_blog_post(blog_post.title)
        # db_blog_post.content = content
        content = await generate_blog_post_async(blog_post.title) 
        db_blog_post.content = content
        db.commit()
        db.refresh(db_blog_post)

    background_tasks.add_task(generate_blog_content_and_update)
    return db_blog_post