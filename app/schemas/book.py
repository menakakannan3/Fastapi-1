from pydantic import BaseModel
from typing import Optional
class BookBase(BaseModel):
    title: str
    author: str
    description: str
    category_id: Optional[int]  # ✅ allow nulls in DB

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True
