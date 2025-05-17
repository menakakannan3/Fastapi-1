from fastapi import FastAPI
from app.api import book_routes, user_routes
from app.database.session import Base, engine

app = FastAPI(title="Books & Users API")

Base.metadata.create_all(bind=engine)

app.include_router(book_routes.router)
app.include_router(user_routes.router)
