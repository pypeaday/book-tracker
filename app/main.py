from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
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

def get_current_theme(request: Request) -> tuple[themes.ThemeColors, str]:
    """Get the current theme colors based on cookie or default"""
    theme_name = request.cookies.get("theme", DEFAULT_THEME)
    theme = themes.get_theme(theme_name)
    if not theme:
        theme = themes.get_theme(DEFAULT_THEME)
        theme_name = DEFAULT_THEME
    return theme, theme_name

def set_theme_cookie(response: HTMLResponse, theme_name: str) -> None:
    """Set theme cookie with standard parameters"""
    response.set_cookie(
        key="theme",
        value=theme_name,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )

# API Models
class ThemeColors(BaseModel):
    bg: str
    bg1: str
    bg2: str
    fg: str
    fg1: str
    accent: str
    accent_hover: str
    success: str
    error: str

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
def home(request: Request, db: Session = Depends(database.get_db)):
    books = db.query(models.Book).all()
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "index.html",
        {"request": request, "books": books, "theme": theme, "current_theme": current_theme}
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )
    return response

@app.get("/settings")
def settings_page(request: Request):
    theme, current_theme = get_current_theme(request)
    # Create a dict of theme names and their colors
    theme_previews = {name: colors for name, colors in themes.THEMES.items()}
    # Sort themes alphabetically for consistent display
    theme_previews = dict(sorted(theme_previews.items()))
    
    response = templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "theme_previews": theme_previews,
            "current_theme": current_theme,
            "theme": theme
        }
    )
    set_theme_cookie(response, current_theme)
    return response

@app.post("/settings/theme")
def update_theme(request: Request, theme_name: str = Form(...)):
    if theme_name not in themes.THEMES:
        raise HTTPException(status_code=400, detail="Invalid theme")
    
    # Update the HTML data-theme attribute via HTMX response
    response = HTMLResponse("", status_code=200)
    set_theme_cookie(response, theme_name)
    response.headers["HX-Trigger"] = "themeChanged"
    return response

@app.get("/add-book")
def add_book_form(request: Request):
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "book_form.html",
        {"request": request, "book": None, "theme": theme, "current_theme": current_theme}
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )
    return response

@app.get("/edit-book/{book_id}")
def edit_book_form(request: Request, book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "book_form.html",
        {"request": request, "book": book, "theme": theme, "current_theme": current_theme}
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )
    return response

# JSON API endpoints
@app.get("/api/theme/{theme_name}", response_model=ThemeColors)
def get_theme_colors(theme_name: str):
    theme = themes.get_theme(theme_name)
    if not theme:
        raise HTTPException(status_code=404, detail=f"Theme '{theme_name}' not found")
    return theme

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
    
    # Get theme information
    theme, current_theme = get_current_theme(request)
    
    # Check if we should return the card or the form
    format_param = request.query_params.get('format', 'form')
    
    if format_param == 'card':
        # Return just the book card
        context = {
            "request": request, 
            "book": book, 
            "theme": theme, 
            "current_theme": current_theme
        }
        return templates.TemplateResponse("partials/book_card.html", context)
    else:
        # Return the edit form
        return templates.TemplateResponse("book_form.html", {"request": request, "book": book, "theme": theme, "current_theme": current_theme})

@app.post("/books/")
def create_book(
    request: Request,
    title: str = Form(...),
    author: Optional[str] = Form(None),
    status: str = Form(...),
    notes: Optional[str] = Form(None),
    rating: Optional[int] = Form(None),
    db: Session = Depends(database.get_db)
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
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "index.html",
        {"request": request, "books": books, "theme": theme, "current_theme": current_theme}
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )
    return response

@app.put("/books/{book_id}")
def update_book(
    request: Request,
    book_id: int,
    title: str = Form(...),
    author: Optional[str] = Form(None),
    status: str = Form(...),
    notes: Optional[str] = Form(None),
    rating: Optional[int] = Form(None),
    db: Session = Depends(database.get_db)
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
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "index.html",
        {"request": request, "books": books, "theme": theme, "current_theme": current_theme}
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )
    return response

@app.patch("/books/{book_id}/status")
async def update_book_status(request: Request, book_id: int, status: str = Form(...), db: Session = Depends(database.get_db)):
    print(f"Updating book {book_id} status to {status}")
    
    # Find the book
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        print(f"Book {book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update the status
    old_status = db_book.status
    db_book.status = status
    db.commit()
    db.refresh(db_book)
    print(f"Book {book_id} status updated from {old_status} to {status}")
    
    # Return the updated book card
    theme, current_theme = get_current_theme(request)
    
    # Create context for template rendering
    context = {
        "request": request, 
        "book": db_book, 
        "theme": theme, 
        "current_theme": current_theme
    }
    
    # Render the template directly
    html_content = templates.get_template("partials/book_card.html").render(context)
    print(f"Returning JSON response for book {book_id}")
    
    # Return JSON with both HTML content and book data
    return JSONResponse(content={
        "html": html_content,
        "book": {
            "id": db_book.id,
            "title": db_book.title,
            "author": db_book.author,
            "status": db_book.status,
            "rating": db_book.rating
        }
    }, status_code=200)

@app.delete("/books/{book_id}")
def delete_book(request: Request, book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    
    # Get all books for the full page refresh
    books = db.query(models.Book).all()
    theme, current_theme = get_current_theme(request)
    response = templates.TemplateResponse(
        "index.html",
        {"request": request, "books": books, "theme": theme, "current_theme": current_theme}
    )
    response.set_cookie(
        key="theme",
        value=current_theme,
        max_age=31536000,  # 1 year
        httponly=False,  # Allow JavaScript to read the cookie
        samesite="lax",
        secure=False  # Allow non-HTTPS for local development
    )
    return response
