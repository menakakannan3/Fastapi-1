# app/api/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.crud import user as crud_user
from app.database.session import SessionLocal

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead)
def create(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)

@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": "admin" if user.name.lower() == "admin" else "user"}
