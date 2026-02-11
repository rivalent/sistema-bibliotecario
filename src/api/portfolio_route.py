import logging
import traceback
from fastapi import APIRouter, HTTPException, status
from src.service.portfolio_service import PortfolioService
from src.service.book_service import BookService
from src.schemas.portfolio_schema import PortfolioCreate, PortfolioUpdate

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
portfolio_service = PortfolioService()
book_service = BookService()

@router.post('/portfolio', status_code=status.HTTP_201_CREATED)
def register_new_copy(portfolio_data: PortfolioCreate):
    try:
        isbn_clean = portfolio_data.book_isbn
        existing_book = book_service.find_by_isbn(isbn_clean)
        
        if not existing_book:
            raise HTTPException(status_code=404, detail=f"Book with ISBN {isbn_clean} not found. Register the book first.")

        new_copy = portfolio_service.register_new_copy(
            book_isbn = portfolio_data.book_isbn,
            condition_str = portfolio_data.condition_enum, 
            cover_str = portfolio_data.cover_enum
        )

        if not new_copy:
            raise HTTPException(
                status_code=400, 
                detail="Failed to register. Check if: 1) ISBN is valid (13 digits), 2) Book exists, 3) Enums are correct."
            )
        
        logging.debug(f"[PORTFOLIO-API] Created successfully: {new_copy.id}")
        return new_copy.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[PORTFOLIO-API] Fail to create: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/portfolio/book/{book_isbn}', status_code=status.HTTP_200_OK)
def list_copies_by_book(book_isbn: str):
    try:

        copies = portfolio_service.list_copies_by_book(book_isbn)

        logging.debug(f"[PORTFOLIO-API] Found {len(copies)} copies for book {book_isbn}")
        return [copy.to_dict() for copy in copies]

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[PORTFOLIO-API] Fail to get: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.put('/portfolio/{portfolio_id}', status_code=status.HTTP_200_OK)
def update_condition(portfolio_id: str, update_data: PortfolioUpdate):
    try:
        success = portfolio_service.update_state(
            portfolio_id=portfolio_id,
            new_condition_str=update_data.condition_enum 
        )

        if not success:
            raise HTTPException(status_code=404, detail="Portfolio item not found or Enum invalid")
        
        return {"message": "Condition updated successfully"}

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[PORTFOLIO-API] Fail to update: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))
