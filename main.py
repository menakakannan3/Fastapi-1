from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import book_routes, user_routes, category_routes

app = FastAPI()

# CORS middleware to allow frontend (e.g., React on localhost:3000) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(category_routes.router)
