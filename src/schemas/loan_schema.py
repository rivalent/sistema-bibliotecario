from pydantic import BaseModel, Field
from typing import Optional

class RentRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    portfolio_id: str = Field(..., min_length=1)
    days: Optional[int] = Field(7, gt=0, le=45)

class ReturnRequest(BaseModel):
    condition_enum: str = Field(..., min_length=3)