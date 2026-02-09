from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None