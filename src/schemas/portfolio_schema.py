from pydantic import BaseModel, Field

class PortfolioCreate(BaseModel):
    book_isbn: str = Field(...)
    condition_enum: str = Field(..., min_length=1) 
    cover_enum: str = Field(..., min_length=1)

class PortfolioUpdate(BaseModel):
    condition_enum: str = Field(..., min_length=1)
