import logging
import traceback
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from src.service.book_service import BookService
from src.schemas.book_schema import BookRequest

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
service = BookService()

@router.post('/books', status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookRequest):
    try:
        summary_clean = book_data.summary.strip() if book_data.summary else None
        
        new_book = service.create(
            title=book_data.title.strip(),
            isbn=book_data.isbn.strip(),
            author=book_data.author.strip(),
            release_year=book_data.release_year,
            publisher=book_data.publisher.strip(),
            page_len=book_data.page_len,
            genre_enum=book_data.genre.strip().lower(),
            summary=summary_clean
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
            results = service.search(q.strip(), search_type.strip().lower())
        else:
            results = [] 
        
        return [book.to_dict() for book in results]

    except Exception as error:
        logging.error(f"[BOOK-API] Fail to search: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))


@router.get('/books/{isbn}', status_code=status.HTTP_200_OK)
def get_book_by_isbn(isbn: str):
    try:
        book = service.find_by_isbn(isbn.strip())

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
def update_book(isbn: str, book_data: BookRequest):
    try:
        updated_book = service.update(
            isbn.strip(),
            book_data.title.strip(),
            book_data.author.strip(),
            book_data.publisher.strip(),
            book_data.release_year,
            
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
        success_delete = service.delete(isbn.strip())

        if not success_delete:
            logging.debug(f"[BOOK-API] Delete failed: Book {isbn} not found")
            raise HTTPException(status_code=404, detail="Book not found") 
        
        return

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[BOOK-API] Fail to delete: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))
