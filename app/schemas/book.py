from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    category_id: int  # 🆕 added

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True
