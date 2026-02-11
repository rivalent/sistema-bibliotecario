from json import dumps
from typing import Optional, Union
from datetime import datetime
from src.models.enums import BookConditionEnum

class Loan:
    def __init__(
        self, 
        portfolio_id: str, 
        user_id: str,
        start_at: datetime, 
        loan_condition: Union[BookConditionEnum, str], 
        return_condition: Union[BookConditionEnum, str] = None, 
        return_at: Optional[datetime] = None, 
        period: int = 30,
        id: Optional[str] = None
    ):
        self.id = id
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        self.start_at = start_at
        self.loan_condition = loan_condition
        self.return_condition = return_condition
        self.return_at = return_at
        self.period = period

    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "user_id": self.user_id,
            "period": self.period,
            "start_at": self.start_at if self.start_at else None,
            "return_at": self.return_at if self.return_at else None,
            "loan_condition": self.loan_condition.value if hasattr(self.loan_condition, 'value') else self.loan_condition,
            "return_condition": self.return_condition.value if hasattr(self.return_condition, 'value') else self.return_condition
        }

    def to_json(self):
        return dumps(self.to_dict())
