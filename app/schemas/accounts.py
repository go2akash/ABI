from pydantic import BaseModel, EmailStr


class AccountResponse(BaseModel):
    full_name: str
    account_number: int
    balance: float
