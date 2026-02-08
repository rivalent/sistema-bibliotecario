from src.storage.db_manager import DBManager
from src.models.loan import Loan

class LoanRepository:
    def __init__(self):
        self.db = DBManager()

    def create_loan(self, loan: Loan):
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
        return loan

    def get_loan_by_id(self, loan_id) -> Loan:
        query = "SELECT * FROM loan WHERE id = ?"
        params = (loan_id,)
        result = self.db.execute_query(query, params)

        if result:
            row = result[0]
            return Loan(*row)
        return None

    def get_active_loans_by_user(self, user_id) -> list[Loan]:
        query = "SELECT * FROM loan WHERE user_id = ? AND return_at IS NULL"
        params = (user_id,)
        result = self.db.execute_query(query, params)

        loans = []
        if result:
            for row in result:
                loans.append(Loan(*row))
        return loans

    def finish_loan(self, loan_id, return_at, return_condition):
        query = "UPDATE loan SET return_at = ?, return_condition = ? WHERE id = ?"
        
        return_at_str = str(return_at) if return_at else None
        r_cond_val = getattr(return_condition, 'value', return_condition)

        params = (return_at_str, r_cond_val, loan_id)
        self.db.execute_query(query, params)

    def get_active_loan_by_portfolio_id(self, portfolio_id):
        query = "SELECT * FROM loan WHERE portfolio_id = ? AND return_at IS NULL"
        params = (portfolio_id,)
        result = self.db.execute_query(query, params)

        if result:
            row = result[0]
            return Loan(*row)
        return None