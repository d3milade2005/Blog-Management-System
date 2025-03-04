from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import src.schemas as schemas, src.services as services, src.auth as auth
from src.database import get_db

blog_router = APIRouter()

@blog_router.post("/", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user)):
    return services.create_blog(db, blog, user_id)

@blog_router.get("/", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    return services.get_blogs(db)

@blog_router.get("/{id}", response_model=schemas.BlogResponse)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = services.get_blog_by_id(db, id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@blog_router.put("/{id}", response_model=schemas.BlogResponse)
def update_blog(id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user)):
    updated_blog = services.update_blog(db, id, blog, user_id)
    if not updated_blog:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return updated_blog

@blog_router.delete("/{id}", response_model=schemas.BlogResponse)
def delete_blog(id: int, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user)):
    deleted_blog = services.delete_blog(db, id, user_id)
    if not deleted_blog:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return deleted_blog