from src.storage.db_manager import DBManager
from src.models.loan import Loan
import logging

class LoanRepository:
    def __init__(self):
        self.db = DBManager()

    def map_row_to_loan(self, row) -> Loan:
        return Loan(
            id = row["id"],
            portfolio_id = row["portfolio_id"],
            user_id = row["user_id"],
            start_at = row["start_at"],
            period = row["period"],
            loan_condition = row["loan_condition"],
            return_at = row["return_at"],
            return_condition = row["return_condition"]
        )

    def create_loan(self, loan: Loan):
        try:
            query = """
                INSERT INTO loan (id, portfolio_id, user_id, start_at, period, loan_condition, return_at, return_condition)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

            l_cond_val = getattr(loan.loan_condition, 'value', loan.loan_condition)
            r_cond_val = getattr(loan.return_condition, 'value', loan.return_condition)

            start_at_str = str(loan.start_at) if loan.start_at else None
            return_at_str = str(loan.return_at) if loan.return_at else None

            params = (
                loan.id,
                loan.portfolio_id,
                loan.user_id,
                start_at_str,
                loan.period,
                l_cond_val,
                return_at_str,
                r_cond_val
            )

            self.db.execute_query(query, params)
            logging.debug(f"[LOAN-REPO] Created loan ID: {loan.id} for User: {loan.user_id}")
            return loan

        except Exception as error:
            logging.error(f"[LOAN-REPO] Fail to create loan: {error}")
            raise error

    def get_loan_by_id(self, loan_id) -> Loan:
        try:
            query = """
                SELECT id, portfolio_id, user_id, start_at, period, loan_condition, return_at, return_condition 
                FROM loan WHERE id = ?
            """
            params = (loan_id,)
            result = self.db.execute_query(query, params)

            if result:
                return self.map_row_to_loan(result[0])

            logging.debug(f"[LOAN-REPO] Loan ID {loan_id} not found")
            return None

        except Exception as error:
            logging.error(f"[LOAN-REPO] Fail to get by ID: {error}")
            raise error

    def get_active_loans_by_user(self, user_id) -> list[Loan]:
        try:
            query = """
                SELECT id, portfolio_id, user_id, start_at, period, loan_condition, return_at, return_condition 
                FROM loan 
                WHERE user_id = ? AND return_at IS NULL
            """
            params = (user_id,)
            result = self.db.execute_query(query, params)

            loans = []
            if result:
                for row in result:
                    loans.append(self.map_row_to_loan(row))
            
            logging.debug(f"[LOAN-REPO] Found {len(loans)} active loans for User {user_id}")
            return loans

        except Exception as error:
            logging.error(f"[LOAN-REPO] Fail to get active loans: {error}")
            raise error

    def finish_loan(self, loan_id, return_at, return_condition):
        try:
            query = "UPDATE loan SET return_at = ?, return_condition = ? WHERE id = ?"
            
            return_at_str = str(return_at) if return_at else None
            r_cond_val = getattr(return_condition, 'value', return_condition)

            params = (return_at_str, r_cond_val, loan_id)
            self.db.execute_query(query, params)
            
            logging.debug(f"[LOAN-REPO] Finished Loan {loan_id}. Condition: {r_cond_val}")

        except Exception as error:
            logging.error(f"[LOAN-REPO] Fail to finish loan: {error}")
            raise error

    def get_active_loan_by_portfolio_id(self, portfolio_id) -> Loan:
        try:
            query = """
                SELECT id, portfolio_id, user_id, start_at, period, loan_condition, return_at, return_condition 
                FROM loan 
                WHERE portfolio_id = ? AND return_at IS NULL
            """
            params = (portfolio_id,)
            result = self.db.execute_query(query, params)

            if result:
                logging.debug(f"[LOAN-REPO] Portfolio {portfolio_id} is currently ON LOAN")
                return self.map_row_to_loan(result[0])
            
            return None

        except Exception as error:
            logging.error(f"[LOAN-REPO] Fail to check portfolio availability: {error}")
            raise error