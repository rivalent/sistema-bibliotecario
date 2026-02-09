import logging
import traceback
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from src.service.book_service import BookService
from src.schemas.book_schema import BookRequest, BookUpdate

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
service = BookService()

@router.post('/books', status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookRequest):
    try:
        new_book = service.create(
            title=book_data.title,
            isbn=book_data.isbn,
            author=book_data.author,
            release_year=book_data.release_year,
            publisher=book_data.publisher,
            page_len=book_data.page_len,
            genre_enum=book_data.genre,
            summary=book_data.summary
        )

        if not new_book:
            logging.debug(f"[BOOK-API] fail to create")
            raise HTTPException(status_code=400, detail="Fail to create book. Verify the data")

        logging.debug(f"[BOOK-API] Created successfully: {new_book.title} - {new_book.isbn}")
        return new_book.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[BOOK-API] Fail to create: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/books', status_code=status.HTTP_200_OK)
def search_books(q: Optional[str] = None, search_type: Optional[str] = "title"):
    try:
        results = []
        if q:
            results = service.search(q, search_type)
        else:
            results = [] 
        
        return [book.to_dict() for book in results]

    except Exception as error:
        logging.error(f"[BOOK-API] Fail to search: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))


@router.get('/books/{isbn}', status_code=status.HTTP_200_OK)
def get_book_by_isbn(isbn: str):
    try:
        book = service.find_by_isbn(isbn)

        if not book:
            logging.debug(f"[BOOK-API] Book {isbn} not found (404)")
            raise HTTPException(status_code=404, detail="Book not found")
        
        logging.debug(f"[BOOK-API] Found book: {book.isbn}")
        return book.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[BOOK-API] Fail to find: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))


@router.put('/books/{isbn}', status_code=status.HTTP_200_OK)
def update_book(isbn: str, book_data: BookUpdate):
    try:
        updated_book = service.update(
            isbn,
            book_data
        )

        if not updated_book:
            logging.debug(f"[BOOK-API] Update failed: Book {isbn} not found")
            raise HTTPException(status_code=404, detail="Book not found")
        
        logging.debug(f"[BOOK-API] Updated successfully: {isbn}")
        return updated_book.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[BOOK-API] Fail to update: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))


@router.delete('/books/{isbn}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(isbn: str):
    try:
        success_delete = service.delete(isbn)

        if not success_delete:
            logging.debug(f"[BOOK-API] Delete failed: Book {isbn} not found")
            raise HTTPException(status_code=404, detail="Book not found") 
        
        return

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[BOOK-API] Fail to delete: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))
