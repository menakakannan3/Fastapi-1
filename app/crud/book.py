from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

def create_book(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        category_id=book.category_id  # ✅ store category ID
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(Book).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: BookCreate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    db_book.title = book.title
    db_book.author = book.author
    db_book.description = book.description
    db_book.category_id = book.category_id  # ✅ update category ID
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book
