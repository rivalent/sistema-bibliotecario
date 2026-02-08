from pydantic import BaseModel, Field
from typing import Optional

class BookRequest(BaseModel):
    title: str
    isbn: str = Field(..., min_length=13, max_length=13)
    author: str
    release_year: int = Field(..., ge=1000, le=2100)  
    publisher: str
    page_len: int = Field(..., gt=0) 
    genre: str
    summary: Optional[str] = None
