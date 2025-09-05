from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    
    amount: float
    type: str
    created_at: str
    account: int
    status: str
    model_config = ConfigDict(from_attributes=True)
