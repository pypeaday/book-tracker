from pydantic import BaseModel
from typing import Optional
from enum import Enum

class BookStatus(str, Enum):
    TO_READ = "to_read"
    READING = "reading"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DNF = "dnf"

class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    status: BookStatus
    notes: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
