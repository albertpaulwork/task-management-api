from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base User schema
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

# Schema for returning user data (response)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True  # Allows reading from SQLAlchemy models

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
