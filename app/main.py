from fastapi import FastAPI
from app.api import book_routes, user_routes, category_routes  # <-- add this

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(category_routes.router)  # <-- add this
