from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.crud import user as crud_user
from app.database.session import SessionLocal
from app.auth import create_access_token, verify_password

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new user
@router.post("/", response_model=UserRead)
def create(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)

# Get all users
@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

# Login and return JWT token
@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = "admin" if user.name.lower() == "admin" else "user"
    token_data = {
        "sub": user.email,
        "name": user.name,
        "role": role
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
