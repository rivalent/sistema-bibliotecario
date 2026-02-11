import logging
import traceback
from src.storage.db_manager import DBManager

class ReportRepository:
    def __init__(self):
        self.db = DBManager()

    def get_expired_loans(self, user_id=None):
        try:
            query = """
                SELECT 
                    l.id AS loan_id, 
                    u.name AS user_name, 
                    u.email AS user_email,
                    b.title AS book_title, 
                    l.start_at, 
                    l.period,
                    date(l.start_at, '+' || l.period || ' days') AS due_date
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
            
            logging.debug(f"[REPORT-REPO] Found {len(results)} expired loans")
            return results

        except Exception as error:
            logging.error(f"[REPORT-REPO] Fail to get expired loans: {error}")
            return []

    def get_taken_loans(self, book_isbn=None, user_id=None):
        try:
            query = """
                SELECT 
                    l.id AS loan_id, 
                    u.name AS user_name, 
                    b.title AS book_title, 
                    l.start_at,
                    date(l.start_at, '+' || l.period || ' days') AS due_date
                FROM loan l
                JOIN users u ON l.user_id = u.id
                JOIN portfolio p ON l.portfolio_id = p.id
                JOIN books b ON p.book_id = b.isbn
                WHERE l.return_at IS NULL
            """
            
            params = []
            if book_isbn:
                query += " AND b.isbn = ?"
                params.append(book_isbn)
            if user_id:
                query += " AND l.user_id = ?"
                params.append(user_id)

            results = self.db.execute_query(query, tuple(params))
            
            logging.debug(f"[REPORT-REPO] Found {len(results)} active loans")
            return results

        except Exception as error:
            logging.error(f"[REPORT-REPO] Fail to get taken loans: {error}")
            return []

    def get_available_portfolio(self, book_isbn=None):
        try:
            query = """
                SELECT 
                    p.id AS portfolio_id, 
                    b.title AS book_title, 
                    b.isbn,
                    p.condition
                FROM portfolio p
                JOIN books b ON p.book_id = b.isbn
                WHERE p.id NOT IN (
                    SELECT portfolio_id FROM loan WHERE return_at IS NULL
                )
            """
            
            params = []
            if book_isbn:
                query += " AND p.book_id = ?"
                params.append(book_isbn)
                
            results = self.db.execute_query(query, tuple(params))
            
            logging.debug(f"[REPORT-REPO] Found {len(results)} available items")
            return results

        except Exception as error:
            logging.error(f"[REPORT-REPO] Fail to get available portfolio: {error}")
            return []