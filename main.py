from fastapi import FastAPI
from database import engine, Base
import models
from routers import users, books, orders  # single import line
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bookstore API",
    version="1.0.0",
    description="A simple Bookstore API using FastAPI with JWT Auth"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Allow Swagger UI or other frontends to work smoothly (optional but helpful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(users.router)
app.include_router(books.router)
app.include_router(orders.router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Bookstore API"}
