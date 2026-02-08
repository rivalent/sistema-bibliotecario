from src.storage.db_manager import DBManager
from src.models.portfolio import Portfolio

class PortfolioRepository:
    def __init__(self):
        self.db = DBManager()

    def create_portfolio(self, portfolio: Portfolio):
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
        return portfolio

    def get_portfolio_by_id(self, portfolio_id) -> Portfolio:
        query = "SELECT * FROM portfolio WHERE id = ?"
        params = (portfolio_id,)
        result = self.db.execute_query(query, params)

        if result:
            row = result[0]
            return Portfolio(*row)
        return None

    def get_portfolio_by_book_id(self, book_isbn) -> list[Portfolio]:
        query = "SELECT * FROM portfolio WHERE book_id = ?"
        params = (book_isbn,)
        result = self.db.execute_query(query, params)

        items = []
        if result:
            for row in result:
                items.append(Portfolio(*row))
        return items

    def update_condition(self, portfolio_id, new_condition):
        condition_val = getattr(new_condition, 'value', new_condition)
        
        query = "UPDATE portfolio SET condition = ? WHERE id = ?"
        params = (condition_val, portfolio_id)
        
        self.db.execute_query(query, params)

    def delete_portfolio(self, portfolio_id):
        query = "DELETE FROM portfolio WHERE id = ?"
        params = (portfolio_id,)
        self.db.execute_query(query, params)
