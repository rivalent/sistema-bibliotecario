from pydantic import BaseModel, EmailStr, Field

class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr