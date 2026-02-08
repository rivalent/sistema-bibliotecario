import logging
from src.repositories.report_repository import ReportRepository

class ReportService:
    def __init__(self):
        self.repo = ReportRepository()

    def get_expired_report(self):
        try:
            expired_list = self.repo.get_expired_loans()
            
            logging.debug(f"[REPORT-SERVICE] Found {len(expired_list)} expired loans")
            return expired_list
            
        except Exception as error:
            logging.error(f"[REPORT-SERVICE] Fail to get expired: {error}")
            return []

    def get_available_books_report(self, book_isbn=None):
        try:
            available = self.repo.get_available_portfolio(book_isbn)
            return available
        except Exception as error:
            logging.error(f"[REPORT-SERVICE] Fail: {error}")
            return []
            
    def get_taken_books_report(self):
        try:
            taken = self.repo.get_taken_loans()
            return taken
        except Exception as error:
            logging.error(f"[REPORT-SERVICE] Fail: {error}")
            return []