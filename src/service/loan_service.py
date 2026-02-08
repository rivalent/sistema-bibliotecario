import logging
import traceback
import datetime
from ulid import ULID
from src.repositories.loan_repository import LoanRepository
from src.models.loan import Loan

class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()

    def rent_book(self, user_id, portfolio_id, days=7):
        try:
            active_loan = self.loan_repo.get_active_loan_by_portfolio_id(portfolio_id)
            
            if active_loan:
                logging.warning(f"[LOAN-SERVICE] Denied: Portfolio {portfolio_id} is already rented.")
                return None

            loan_id = str(ULID())
            start_at = datetime.datetime.now()
            
            new_loan = Loan(
                id=loan_id,
                portfolio_id=portfolio_id,
                user_id=user_id,
                start_at=start_at,
                period=days,
                loan_condition=None,
                return_at=None,
                return_condition=None
            )

            self.loan_repo.create_loan(new_loan)
            
            logging.debug(f"[LOAN-SERVICE] Loan created: {loan_id} for User {user_id}")
            return new_loan
            
        except Exception as error:
            logging.error(f"[LOAN-SERVICE] Fail to rent: {error} -> {traceback.format_exc()}")
            return None

    def return_book(self, loan_id, condition_enum):
        try:
            existing_loan = self.loan_repo.get_loan_by_id(loan_id)
            
            if not existing_loan:
                logging.warning(f"[LOAN-SERVICE] Return failed: Loan {loan_id} not found.")
                return False

            if existing_loan.return_at is not None:
                logging.warning(f"[LOAN-SERVICE] Loan {loan_id} was already returned at {existing_loan.return_at}.")
                return False 

            return_date = datetime.datetime.now()
            
            self.loan_repo.finish_loan(loan_id, return_date, condition_enum)
            
            logging.debug(f"[LOAN-SERVICE] Book returned. Loan {loan_id} finished.")
            return True
            
        except Exception as error:
             logging.error(f"[LOAN-SERVICE] Fail to return: {error} -> {traceback.format_exc()}")
             return False

    def get_my_loans(self, user_id):
        try:
            return self.loan_repo.get_active_loans_by_user(user_id)
        except Exception as error:
            logging.error(f"[LOAN-SERVICE] Fail to list loans: {error}")
            return []