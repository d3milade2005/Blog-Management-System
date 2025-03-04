from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./sql.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Creating a sessionmaker object to interact with the database
Base = declarative_base()

#function to manage database session and we use get_db whenever we need to interact with the database in our API endpoints
def get_db():
    db = SessionLocal() #creates a new session for interacting with the database
    try:
        yield db #we use yield instead of return, so the session will automatically close after the request is finished
    finally:
        db.close()

#yield db returns the session to the route handler that depends on get_db