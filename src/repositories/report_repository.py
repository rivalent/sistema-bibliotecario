from src.storage.db_manager import DBManager

class ReportRepository:
    def __init__(self):
        self.db = DBManager()

    def get_expired_loans(self, user_id=None):
        query = """
            SELECT l.id, u.name, b.title, l.start_at, l.period
            FROM loan l
            JOIN users u ON l.user_id = u.id
            JOIN portfolio p ON l.portfolio_id = p.id
            JOIN books b ON p.book_id = b.isbn
            WHERE l.return_at IS NULL
            AND date(l.start_at, '+' || l.period || ' days') < date('now')
        """
        
        params = []
        if user_id:
            query += " AND l.user_id = ?"
            params.append(user_id)
            
        results = self.db.execute_query(query, tuple(params))
        return results

    def get_taken_loans(self, book_id=None, user_id=None):
        query = """
            SELECT l.id, u.name, b.title, l.start_at
            FROM loan l
            JOIN users u ON l.user_id = u.id
            JOIN portfolio p ON l.portfolio_id = p.id
            JOIN books b ON p.book_id = b.isbn
            WHERE l.return_at IS NULL
        """
        
        params = []
        if book_id:
            query += " AND b.isbn = ?"
            params.append(book_id)
        if user_id:
            query += " AND l.user_id = ?"
            params.append(user_id)

        results = self.db.execute_query(query, tuple(params))
        return results

    def get_available_portfolio(self, book_id=None):
        query = """
            SELECT p.id, b.title, p.condition
            FROM portfolio p
            JOIN books b ON p.book_id = b.isbn
            WHERE p.id NOT IN (
                SELECT portfolio_id FROM loan WHERE return_at IS NULL
            )
        """
        
        params = []
        if book_id:
            query += " AND p.book_id = ?"
            params.append(book_id)
            
        results = self.db.execute_query(query, tuple(params))
        return results
