from pydantic import BaseModel, Field
from typing import Optional

class BookRequest(BaseModel):
    title: str
    isbn: str
    author: str
    release_year: int = Field(..., ge=1000, le=2100)  
    publisher: str
    page_len: int = Field(..., gt=0) 
    genre: str
    summary: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = Field(None, min_length=13, max_length=13)
    author: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1000, le=2100)
    publisher: Optional[str] = None
    page_len: Optional[int] = Field(None, gt=0)
    genre: Optional[str] = None
    summary: Optional[str] = None
