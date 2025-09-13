from uuid import UUID
from pydantic import BaseModel, EmailStr,ConfigDict,model_validator
from typing import Optional


class AdminCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    name:str


class AdminShow(BaseModel):
    name:str
    username:str
    email:EmailStr
    model_config = ConfigDict(from_attributes=True)

class AdminLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    @model_validator(mode='after')
    def check_username_or_email(self):
        if not self.username and not self.email:
            raise ValueError('Either username or email must be provided')
        return self


class UserDetailResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)




#UserDetailResponse,
#AccountDetailResponse, 
#TransactionDetailResponse
