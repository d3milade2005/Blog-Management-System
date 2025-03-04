from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogResponse(BlogCreate):
    id: int
    author_id: int

    class Config:
        orm_mode = True