from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
from src.auth import authenticate_user, create_access_token
from src.database import get_db
from src import schemas
import src.models as models, src.database as database
from .auth import auth_router
from .routes.blogs import blog_router
from .ai_agent import ai_router

# Initialize database
models.Base.metadata.create_all(bind=database.engine)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

app.include_router(blog_router, prefix="/api/v1/blogs")
app.include_router(ai_router, prefix="/api/v1/blogs/ai_generator")
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
def welcome():
    return {"message": "Welcome to the AI-Powered Blog Post Creation API!"}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}