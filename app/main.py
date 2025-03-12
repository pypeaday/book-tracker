from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from . import models, database

app = FastAPI(title="Book Tracking API")
templates = Jinja2Templates(directory="app/templates")

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def home(request: Request, db: Session = Depends(database.get_db)):
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.get("/add-book")
def add_book_form(request: Request):
    return templates.TemplateResponse("book_form.html", {"request": request, "book": None})

@app.get("/edit-book/{book_id}")
def edit_book_form(request: Request, book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_form.html", {"request": request, "book": book})

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
    db: Session = Depends(database.get_db)
):
    book_data = {
        "title": title,
        "author": author,
        "status": status,
        "notes": notes
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
    db: Session = Depends(database.get_db)
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data = {
        "title": title,
        "author": author,
        "status": status,
        "notes": notes
    }
    
    for key, value in book_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    
    # Get all books for the full page refresh
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.delete("/books/{book_id}")
def delete_book(request: Request, book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    
    # Get all books for the full page refresh
    books = db.query(models.Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})
