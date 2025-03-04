from sqlalchemy.orm import Session
import src.models as models, src.schemas as schemas


def create_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    db_blog = models.Blog(**blog.dict(), author_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blogs(db: Session):
    return db.query(models.Blog).all()

def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def update_blog(db: Session, blog_id: int, blog_data: schemas.BlogCreate, user_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.author_id == user_id).first()
    if not db_blog:
        return None
    db_blog.title = blog_data.title
    db_blog.content = blog_data.content
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int, user_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.author_id == user_id).first()
    if not db_blog:
        return None
    db.delete(db_blog)
    db.commit()
    return db_blog