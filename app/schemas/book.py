# app/schemas/book.py
from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    genre: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=2025)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    genre: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=2025)

class BookResponse(BookBase):
    id: str
    owner: str

    class Config:
        schema_extra = {
            "example": {
                "id": "5f8a4d33e8b2c8f0b0f8d4c0",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A novel about the American Dream",
                "genre": "Classic",
                "published_year": 1925,
                "owner": "johndoe"
            }
        }