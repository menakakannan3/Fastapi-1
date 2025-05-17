# app/api/book_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate, BookRead
from app.crud import book as crud
from app.database.session import SessionLocal
from app.dependencies import admin_required, get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Admin-only
@router.post("/", response_model=BookRead, dependencies=[Depends(admin_required)])
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

# ✅ Public
@router.get("/", response_model=list[BookRead])
def read_all(db: Session = Depends(get_db)):
    return crud.get_books(db)

@router.get("/{book_id}", response_model=BookRead)
def read_one(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ✅ Admin-only
@router.put("/{book_id}", response_model=BookRead, dependencies=[Depends(admin_required)])
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# ✅ Admin-only
@router.delete("/{book_id}", dependencies=[Depends(admin_required)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
