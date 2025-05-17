from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    description: str | None = None

class BookRead(BookCreate):
    id: int

    class Config:
        orm_mode = True
