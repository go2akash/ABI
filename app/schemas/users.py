from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from typing import Dict, Optional, Any
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    username: str
    password: str
    is_active: bool = True
    account_type: str = "savings"  # Default account type


class UserUpdateForm(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    username: Optional[str]
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    username: str
    is_active: bool
    full_name: str
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str


class UserWithAccountResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    account_number: int
    account_type: str
    balance: float

    model_config = ConfigDict(from_attributes=True)


class UserUpdateResponse(BaseModel):
    message: str
    updated_field: Dict[str, Any]
