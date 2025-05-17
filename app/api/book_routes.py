from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate, BookRead
from app.crud import book as crud
from app.database.session import SessionLocal

router = APIRouter(prefix="/books", tags=["Books"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simulated "admin check" using token in header
def admin_required(x_token: str = Header(...)):
    if x_token != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

# ✅ Admin-only: Create a book
@router.post("/", response_model=BookRead, dependencies=[Depends(admin_required)])
def create(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

# ✅ Public: Get all books
@router.get("/", response_model=list[BookRead])
def read_all(db: Session = Depends(get_db)):
    return crud.get_books(db)

# ✅ Public: Get single book
@router.get("/{book_id}", response_model=BookRead)
def read_one(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ✅ Admin-only: Update book
@router.put("/{book_id}", response_model=BookRead, dependencies=[Depends(admin_required)])
def update(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# ✅ Admin-only: Delete book
@router.delete("/{book_id}", dependencies=[Depends(admin_required)])
def delete(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
