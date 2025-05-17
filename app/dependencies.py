# app/dependencies.py
from fastapi import Depends, HTTPException, Header
from jose import JWTError
from app.auth import decode_access_token

def get_current_user(x_token: str = Header(...)):
    payload = decode_access_token(x_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get("name").lower() != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
