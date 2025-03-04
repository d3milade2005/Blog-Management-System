from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext #Importing the CryptContext class from the passlib library to hash our password
from sqlalchemy.orm import Session
import models
from database import get_db
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key") #The secret key used for our JWT token
ALGORITHM = os.getenv("ALGORITHM", "HS256") #The alorithm used for our encryption for the JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) #The time in minutes that the token will expire


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #Creating a CryptContext object to hash our password
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token") #Creating an OAuth2PasswordBearer object to authenticate our user

def verify_password(plain_password, hashed_password): #Function to verify the password
    return pwd_context.verify(plain_password, hashed_password) #verify if the plain password matches the hashed password

def get_password_hash(password): #Function to hash the password
    return pwd_context.hash(password) #hash the password

# Fetch user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# Fetch user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db, username: str, password: str): #Function to authenticate the user
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None): #Function to create the access token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user.id  # Return user ID for authorization checks
