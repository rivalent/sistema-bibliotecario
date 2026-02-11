import logging
import traceback
from src.repositories.report_repository import ReportRepository

class ReportService:
    def __init__(self):
        self.repo = ReportRepository()

    def get_expired_report(self, user_id: str = None):
        try:
            if user_id:
                user_id = user_id.strip()

            expired_list = self.repo.get_expired_loans(user_id=user_id)
            
            logging.debug(f"[REPORT-SERVICE] Found {len(expired_list)} expired loans")
            return expired_list
            
        except Exception as error:
            logging.error(f"[REPORT-SERVICE] Fail to get expired: {error} -> {traceback.format_exc()}")
            return []

    def get_available_books_report(self, book_isbn: str = None):
        try:
            if book_isbn:
                book_isbn = book_isbn.replace("-", "").replace(" ", "").strip()

            available = self.repo.get_available_portfolio(book_isbn)
            
            logging.debug(f"[REPORT-SERVICE] Found {len(available)} available items")
            return available

        except Exception as error:
            logging.error(f"[REPORT-SERVICE] Fail to get available report: {error} -> {traceback.format_exc()}")
            return []
            
    def get_taken_books_report(self, book_isbn: str = None, user_id: str = None):
        try:
            if book_isbn:
                book_isbn = book_isbn.replace("-", "").replace(" ", "").strip()
            
            if user_id:
                user_id = user_id.strip()

            taken = self.repo.get_taken_loans(book_isbn=book_isbn, user_id=user_id)
            
            logging.debug(f"[REPORT-SERVICE] Found {len(taken)} active loans")
            return taken

        except Exception as error:
            logging.error(f"[REPORT-SERVICE] Fail to get taken report: {error} -> {traceback.format_exc()}")
            return []
