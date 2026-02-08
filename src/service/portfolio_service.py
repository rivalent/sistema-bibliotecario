import logging
from ulid import ULID
from src.repositories.portfolio_repository import PortfolioRepository
from src.models.portfolio import Portfolio

class PortfolioService:
    def __init__(self):
        self.repo = PortfolioRepository()

    def register_new_copy(self, book_isbn, condition_enum, cover_enum):
        try:
            item_id = str(ULID())
            
            new_item = Portfolio(
                id=item_id,
                book_id=book_isbn,
                condition=condition_enum,
                cover=cover_enum
            )
            self.repo.create_portfolio(new_item)

            logging.debug(f"[PORTFOLIO-SERVICE] Added copy ID {item_id} for Book {book_isbn}")
            return new_item
            
        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to add copy: {error}")
            return None

    def list_copies_by_book(self, book_isbn):
        try:
            items = self.repo.get_portfolio_by_book_id(book_isbn)
            return items

        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to list copies: {error}")
            return []

    def update_state(self, portfolio_id, new_condition_enum):
        try:
            self.repo.update_condition(portfolio_id, new_condition_enum)

            logging.debug(f"[PORTFOLIO-SERVICE] Updated condition for {portfolio_id}")
            return True

        except Exception as error:
            logging.error(f"[PORTFOLIO-SERVICE] Fail to update condition: {error}")
            return False
