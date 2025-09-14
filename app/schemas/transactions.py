from pydantic import BaseModel, ConfigDict,Field


class TransactionResponse(BaseModel):
    
    amount: float
    type: str
    created_at: str
    account: int
    status: str
    model_config = ConfigDict(from_attributes=True)


class TransferForm(BaseModel):
    receiver_account_number: int
    amount:float=Field(ge=0)
    account_type:str="savings"


class DepositForm(TransferForm):
    pass
