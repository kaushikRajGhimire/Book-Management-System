from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, books

app = FastAPI(
    title="Book Management System API",
    description="API for managing books with JWT authentication",
    version="1.0.0"
)

# CORS middleware    PADHNA HAI AUR
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with tags for organizing in Swagger UI OF THE AUTH API AND BOOKS CRUD API
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(books.router, prefix="/api", tags=["Books"])

@app.get("/")
async def root():
    return {"message": "Welcome to Book Management System API"}