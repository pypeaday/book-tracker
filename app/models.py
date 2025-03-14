from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, SmallInteger, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    role = Column(String(20), default="user", nullable=False)  # Options: 'user', 'admin'
    
    # Relationship with books
    books = relationship("Book", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    status = Column(Enum('to_read', 'reading', 'completed', 'on_hold', 'dnf', name='book_status'), nullable=False)
    notes = Column(Text)
    start_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    rating = Column(SmallInteger, nullable=True, comment='0: DNF, 1: Wouldn\'t read again, 2: Good but not recommendable, 3: Would recommend')
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationship with user
    user = relationship("User", back_populates="books")
