from fastapi import FastAPI, Depends, HTTPException, Request, Form, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import datetime

from . import models, database, themes

app = FastAPI(title="Book Tracking API")
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Default theme
DEFAULT_THEME = "gruvbox-dark"

def get_current_theme(theme_name: Optional[str] = Cookie(default=DEFAULT_THEME)) -> themes.ThemeColors:
    """Get the current theme colors based on cookie or default"""
    theme = themes.get_theme(theme_name)
    if not theme:
        theme = themes.get_theme(DEFAULT_THEME)
    return theme

# API Models
class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    status: str
    notes: Optional[str] = None
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    rating: Optional[int] = None

    @field_validator('rating')
    def validate_rating(cls, v):
        if v is not None and not (0 <= v <= 3):
            raise ValueError('Rating must be between 0 and 3')
        return v

class Book(BookCreate):
    id: int
    
    class Config:
        from_attributes = True

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def home(request: Request, db: Session = Depends(database.get_db), theme: themes.ThemeColors = Depends(get_current_theme)):
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books, "theme": theme})

@app.get("/settings")
def settings_page(request: Request, theme: themes.ThemeColors = Depends(get_current_theme)):
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "themes": themes.THEMES,
            "current_theme": next((name for name, t in themes.THEMES.items() if t == theme), None),
            "theme": theme
        }
    )

@app.post("/settings/theme")
def update_theme(request: Request, theme_name: str = Form(...)):
    if theme_name not in themes.THEMES:
        raise HTTPException(status_code=400, detail="Invalid theme")
    
    # Update the HTML data-theme attribute via HTMX response
    response = HTMLResponse("", status_code=200)
    response.set_cookie(key="theme", value=theme_name, max_age=31536000)  # 1 year
    response.headers["HX-Trigger"] = "themeChanged"
    return response

@app.get("/add-book")
def add_book_form(request: Request, theme: themes.ThemeColors = Depends(get_current_theme)):
    return templates.TemplateResponse("book_form.html", {"request": request, "book": None, "theme": theme})

@app.get("/edit-book/{book_id}")
def edit_book_form(request: Request, book_id: int, db: Session = Depends(database.get_db), theme: themes.ThemeColors = Depends(get_current_theme)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_form.html", {"request": request, "book": book, "theme": theme})

# JSON API endpoints
@app.get("/api/books/", response_model=List[Book])
def list_books(db: Session = Depends(database.get_db)):
    books = db.query(models.Book).all()
    return books

@app.post("/api/books/", response_model=Book)
def create_book_api(book: BookCreate, db: Session = Depends(database.get_db)):
    # Convert empty string rating to None
    data = book.model_dump()
    if data.get('rating') == "":
        data['rating'] = None
    db_book = models.Book(**data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/api/books/{book_id}")
def delete_book_api(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"ok": True}

# Template endpoints
@app.get("/books/{book_id}")
def get_book(request: Request, book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_form.html", {"request": request, "book": book})

@app.post("/books/")
def create_book(
    request: Request,
    title: str = Form(...),
    author: Optional[str] = Form(None),
    status: str = Form(...),
    notes: Optional[str] = Form(None),
    rating: Optional[int] = Form(None),
    db: Session = Depends(database.get_db),
    theme: themes.ThemeColors = Depends(get_current_theme)
):
    book_data = {
        "title": title,
        "author": author,
        "status": status,
        "notes": notes,
        "rating": rating if rating != "" else None
    }
    
    db_book = models.Book(**book_data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.put("/books/{book_id}")
def update_book(
    request: Request,
    book_id: int,
    title: str = Form(...),
    author: Optional[str] = Form(None),
    status: str = Form(...),
    notes: Optional[str] = Form(None),
    rating: Optional[int] = Form(None),
    db: Session = Depends(database.get_db),
    theme: themes.ThemeColors = Depends(get_current_theme)
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data = {
        "title": title,
        "author": author,
        "status": status,
        "notes": notes,
        "rating": rating if rating != "" else None
    }
    
    for key, value in book_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    
    # Get all books for the full page refresh
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.delete("/books/{book_id}")
def delete_book(request: Request, book_id: int, db: Session = Depends(database.get_db), theme: themes.ThemeColors = Depends(get_current_theme)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    
    # Get all books for the full page refresh
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})
