from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    status = Column(Enum('to_read', 'reading', 'completed', 'on_hold', 'dnf', name='book_status'), nullable=False)
    notes = Column(Text)
