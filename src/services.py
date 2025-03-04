from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models, schemas


def create_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    db_blog = models.Blog(**blog.dict(), author_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blogs(db: Session):
    return db.query(models.Blog).all()

def get_blog_by_id(db: Session, blog_id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

def update_blog(db: Session, blog_id: int, blog_data: schemas.BlogCreate, user_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.author_id == user_id).first()
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found or unauthorized")
    db_blog.title = blog_data.title
    db_blog.content = blog_data.content
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int, user_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.author_id == user_id).first()
    if not db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found or unauthorized")
    db.delete(db_blog)
    db.commit()
    return db_blog