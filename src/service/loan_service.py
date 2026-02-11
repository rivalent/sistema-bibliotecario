from src.repositories.loan_repository import LoanRepository
from src.repositories.portfolio_repository import PortfolioRepository
from src.repositories.user_repository import UserRepository
from src.models.enums import BookConditionEnum
from src.models.loan import Loan
from ulid import ULID
from datetime import datetime
import logging
import traceback

class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()
        self.portfolio_repo = PortfolioRepository()
        self.user_repo = UserRepository()

    def rent_book(self, user_id: str, portfolio_id: str, days: int = 7):
        try:
            user_id = user_id.replace(" ", "").strip()
            portfolio_id = portfolio_id.replace(" ", "").strip()

            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                logging.warning(f"[LOAN-SERVICE] User {user_id} not found.")
                return None
            
            if getattr(user, 'is_active', False) is False:
                logging.warning(f"[LOAN-SERVICE] Denied: User {user_id} is INACTIVE.")
                return None

            portfolio_item = self.portfolio_repo.get_portfolio_by_id(portfolio_id)
            if not portfolio_item:
                logging.warning(f"[LOAN-SERVICE] Portfolio Item {portfolio_id} not found.")
                return None

            active_loan = self.loan_repo.get_active_loan_by_portfolio_id(portfolio_id)
            if active_loan:
                logging.warning(f"[LOAN-SERVICE] Denied: Portfolio {portfolio_id} is already rented.")
                return None

            loan_id = str(ULID())
            start_at = datetime.now()
            current_condition = portfolio_item.condition 

            new_loan = Loan(
                id=loan_id,
                portfolio_id=portfolio_id,
                user_id=user_id,
                start_at=start_at,
                period=days,
                loan_condition=current_condition,
                return_at=None,
                return_condition=None
            )
            
            self.loan_repo.create_loan(new_loan)
            
            logging.debug(f"[LOAN-SERVICE] Loan created: {loan_id} for User {user_id}")
            return new_loan
            
        except Exception as error:
            logging.error(f"[LOAN-SERVICE] Fail to rent: {error} -> {traceback.format_exc()}")
            return None

    def return_book(self, loan_id: str, return_condition_str: str):
        try:
            loan_id = loan_id.replace(" ", "").strip()
            return_condition_enum = BookConditionEnum(return_condition_str)
            existing_loan = self.loan_repo.get_loan_by_id(loan_id)
            
            if not existing_loan:
                logging.warning(f"[LOAN-SERVICE] Return failed: Loan {loan_id} not found.")
                return False

            if existing_loan.return_at is not None:
                logging.warning(f"[LOAN-SERVICE] Loan {loan_id} was already returned at {existing_loan.return_at}.")
                return False 

            return_date = datetime.now()
            self.loan_repo.finish_loan(loan_id, return_date, return_condition_enum)
            self.portfolio_repo.update_condition(existing_loan.portfolio_id, return_condition_enum)

            logging.debug(f"[LOAN-SERVICE] Book returned. Loan {loan_id} finished. Portfolio condition updated.")
            return True

        except Exception as error:
             logging.error(f"[LOAN-SERVICE] Fail to return: {error} -> {traceback.format_exc()}")
             return False

    def get_my_loans(self, user_id: str):
        try:
            user_id = user_id.replace(" ", "").strip()
            return self.loan_repo.get_active_loans_by_user(user_id)

        except Exception as error:
            logging.error(f"[LOAN-SERVICE] Fail to list loans: {error}")
            return []
