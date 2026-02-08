from json import dumps
from src.models.enums import BookConditionEnum

class Loan:
    def __init__(self, id, portfolio_id, user_id, start_at, loan_condition: BookConditionEnum, return_condition: BookConditionEnum = None, return_at=None, period=30):
        self.id = id
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        self.start_at = start_at
        self.return_at = return_at
        self.period = period
        self.loan_condition = loan_condition
        self.return_condition = return_condition

    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "user_id": self.user_id,
            "period": self.period,
            "start_at": str(self.start_at) if self.start_at else None,
            "return_at": str(self.return_at) if self.return_at else None,
            "loan_condition": self.loan_condition.value if hasattr(self.loan_condition, 'value') else self.loan_condition,
            "return_condition": self.return_condition.value if hasattr(self.return_condition, 'value') else self.return_condition
        }

    def to_json(self):
        return dumps(self.to_dict())
