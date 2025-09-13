from uuid import UUID
from pydantic import BaseModel, EmailStr,ConfigDict



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
    username:str
    email:EmailStr
    password:str



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
