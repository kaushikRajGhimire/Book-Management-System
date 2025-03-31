# app/api/books.py
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.core.security import get_current_user
from app.db.database import books_collection
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(
    book: BookCreate, 
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new book entry
    """
    book_data = book.dict()
    book_data["owner"] = current_user["username"]
    
    result = await books_collection.insert_one(book_data)
    
    created_book = await books_collection.find_one({"_id": result.inserted_id})
    created_book["id"] = str(created_book["_id"])
    del created_book["_id"]
    
    return created_book

@router.get("/books", response_model=List[BookResponse])
async def read_books(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve all books owned by the current user
    """
    books = await books_collection.find(
        {"owner": current_user["username"]}
    ).skip(skip).limit(limit).to_list(length=limit)
    
    for book in books:
        book["id"] = str(book["_id"])
        del book["_id"]
    
    return books

@router.get("/books/title/{title}", response_model=BookResponse)
async def read_book_by_title(
    title: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a specific book by title
    """
    book = await books_collection.find_one({
        "title": title,
        "owner": current_user["username"]
    })
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book["id"] = str(book["_id"])
    del book["_id"]
    
    return book

@router.get("/books/{book_id}", response_model=BookResponse)
async def read_book(
    book_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a specific book by ID
    """
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    book = await books_collection.find_one({
        "_id": obj_id,
        "owner": current_user["username"]
    })
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book["id"] = str(book["_id"])
    del book["_id"]
    
    return book

@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: str,
    book_update: BookUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing book
    """
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    # Filter out None values
    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    # Check if book exists and belongs to user
    book = await books_collection.find_one({
        "_id": obj_id,
        "owner": current_user["username"]
    })
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found or not authorized")
    
    # Update the book
    await books_collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    
    # Get updated book
    updated_book = await books_collection.find_one({"_id": obj_id})
    updated_book["id"] = str(updated_book["_id"])
    del updated_book["_id"]
    
    return updated_book

@router.delete("/books/{book_id}", response_model=dict)
async def delete_book(
    book_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a book
    """
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    # Check if book exists and belongs to user
    book = await books_collection.find_one({
        "_id": obj_id,
        "owner": current_user["username"]
    })
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found or not authorized")
    
    # Delete the book
    result = await books_collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete book")

@router.get("/books/search/", response_model=List[BookResponse])
async def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Search books by title, author, or genre
    """
    query = {"owner": current_user["username"]}
    
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    
    books = await books_collection.find(query).to_list(length=100)
    
    for book in books:
        book["id"] = str(book["_id"])
        del book["_id"]
    
    return books