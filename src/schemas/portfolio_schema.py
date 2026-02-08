from pydantic import BaseModel, Field

class PortfolioCreate(BaseModel):
    book_isbn: str = Field(..., min_length=13, max_length=13)
    condition_enum: str = Field(..., min_length=1) 
    cover_enum: str = Field(..., min_length=1)

class PortfolioUpdate(BaseModel):
    condition_enum: str = Field(..., min_length=1)