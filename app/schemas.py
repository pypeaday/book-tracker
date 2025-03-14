from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class BookStatus(str, Enum):
    TO_READ = "to_read"
    READING = "reading"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DNF = "dnf"

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Book schemas
class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    status: BookStatus
    notes: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
