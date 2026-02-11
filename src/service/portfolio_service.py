import logging
import traceback
from ulid import ULID
from src.repositories.portfolio_repository import PortfolioRepository
from src.repositories.book_repository import BookRepository 
from src.models.portfolio import Portfolio
from src.models.enums import BookConditionEnum, CoverEnum

class PortfolioService:
    def __init__(self):
        self.repo = PortfolioRepository()
        self.book_repo = BookRepository()

    def register_new_copy(self, book_isbn: str, condition_str: str, cover_str: str):
        try:
            book_isbn = book_isbn.replace(" ","").replace("-", "").strip()
            condition_str = condition_str.replace(" ", "").strip().lower()
            cover_str = cover_str.replace(" ", "").strip().lower()

            if len(book_isbn) != 13:
                logging.warning(f"[PORTFOLIO-SERVICE] Invalid ISBN length: {len(book_isbn)} chars. Expected 13.")
                return None

            book = self.book_repo.get_book_by_id(book_isbn)
            if not book:
                logging.warning(f"[PORTFOLIO-SERVICE] Attempt to add copy to non-existent book: {book_isbn}")
                return None

            condition_enum = BookConditionEnum(condition_str)
            cover_enum = CoverEnum(cover_str)
            item_id = str(ULID())

            new_item = Portfolio(
                id=item_id,
                book_id=book_isbn,
                condition=condition_enum,
                cover=cover_enum,
                title=book.title
            )
            self.repo.create_portfolio(new_item)

            logging.debug(f"[PORTFOLIO-SERVICE] Added copy ID {item_id} for Book {book_isbn}")
            return new_item

        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to add copy: {error} -> {traceback.format_exc()}")
            return None

    def list_copies_by_book(self, book_isbn: str):
        try:
            book_isbn = book_isbn.replace(" ","").replace("-", "").strip()
            if len(book_isbn) != 13:
                logging.warning(f"[PORTFOLIO-SERVICE] Invalid ISBN length: {len(book_isbn)} chars. Expected 13.")
                return None

            items = self.repo.get_portfolio_by_book_id(book_isbn)
            return items

        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to list copies: {error} -> {traceback.format_exc()}")
            return []
            
    def find_by_id(self, portfolio_id: str):
        try:
            portfolio_id = portfolio_id.replace(" ", "").strip()
            item = self.repo.get_portfolio_by_id(portfolio_id)
            return item
        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to find: {error} -> {traceback.format_exc()}")
            return None

    def update_state(self, portfolio_id: str, new_condition_str: str):
        try:
            portfolio_id = portfolio_id.replace(" ", "").strip()
            new_condition_str = new_condition_str.strip().lower()

            item = self.find_by_id(portfolio_id)
            if not item:
                logging.warning(f"[PORTFOLIO-SERVICE] Attempt to update non-existent item: {portfolio_id}")
                return False

            new_condition_enum = BookConditionEnum(new_condition_str)
            self.repo.update_condition(portfolio_id, new_condition_enum)

            logging.debug(f"[PORTFOLIO-SERVICE] Updated condition for {portfolio_id} to {new_condition_str}")
            return True

        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to update condition: {error} -> {traceback.format_exc()}")
            return False
