from src.storage.db_manager import DBManager
from src.models.portfolio import Portfolio
import logging

class PortfolioRepository:
    def __init__(self):
        self.db = DBManager()

    def map_row_to_portfolio(self, row) -> Portfolio:
        row_dict = dict(row)

        return Portfolio(
            id = row["id"],
            book_id = row["book_id"],
            condition = row["condition"],
            cover = row["cover"],
            title=row_dict.get("title")
        )

    def create_portfolio(self, portfolio: Portfolio):
        try:
            query = """
                INSERT INTO portfolio (id, book_id, condition, cover)
                VALUES (?, ?, ?, ?)
            """

            condition_val = getattr(portfolio.condition, 'value', portfolio.condition)
            cover_val = getattr(portfolio.cover, 'value', portfolio.cover)

            params = (
                portfolio.id,
                portfolio.book_id,
                condition_val,
                cover_val
            )

            self.db.execute_query(query, params)
            logging.debug(f"[PORTFOLIO-REPOSITORY] Created portfolio ID: {portfolio.id} for Book: {portfolio.book_id}")
            return portfolio

        except Exception as error:
            logging.error(f"[PORTFOLIO-REPOSITORY] Fail to create: {error}")
            raise error

    def get_portfolio_by_id(self, portfolio_id) -> Portfolio:
        try:
            query = """
                SELECT p.id, p.book_id, p.condition, p.cover, b.title
                FROM portfolio p
                JOIN books b ON p.book_id = b.isbn
                WHERE p.id = ?
            """
            params = (portfolio_id,)
            result = self.db.execute_query(query, params)

            if result:
                return self.map_row_to_portfolio(result[0])

            logging.debug(f"[PORTFOLIO-REPOSITORY] ID {portfolio_id} not found")
            return None

        except Exception as error:
            logging.error(f"[PORTFOLIO-REPOSITORY] Fail to get by ID: {error}")
            raise error

    def get_portfolio_by_book_id(self, book_isbn) -> list[Portfolio]:
        try:
            query = """
                SELECT p.id, p.book_id, p.condition, p.cover, b.title
                FROM portfolio p
                JOIN books b ON p.book_id = b.isbn
                WHERE p.book_id = ?
            """
            params = (book_isbn,)
            result = self.db.execute_query(query, params)

            items = []
            if result:
                for row in result:
                    items.append(self.map_row_to_portfolio(row))

            logging.debug(f"[PORTFOLIO-REPOSITORY] Found {len(items)} copies for Book ISBN: {book_isbn}")
            return items

        except Exception as error:
            logging.error(f"[PORTFOLIO-REPOSITORY] Fail to get by Book ISBN: {error}")
            raise error

    def update_condition(self, portfolio_id, new_condition):
        try:
            condition_val = getattr(new_condition, 'value', new_condition)
            
            query = "UPDATE portfolio SET condition = ? WHERE id = ?"
            params = (condition_val, portfolio_id)
            
            self.db.execute_query(query, params)
            logging.debug(f"[PORTFOLIO-REPOSITORY] Updated condition for ID: {portfolio_id} to {condition_val}")

        except Exception as error:
            logging.error(f"[PORTFOLIO-REPOSITORY] Fail to update condition: {error}")
            raise error

    def delete_portfolio(self, portfolio_id):
        try:
            query = "DELETE FROM portfolio WHERE id = ?"
            params = (portfolio_id,)
            self.db.execute_query(query, params)

            logging.debug(f"[PORTFOLIO-REPOSITORY] Deleted ID: {portfolio_id}")

        except Exception as error:
            logging.error(f"[PORTFOLIO-REPOSITORY] Fail to delete: {error}")
            raise error
