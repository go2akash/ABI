from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # default to "bearer"

class AdminToken(Token):
    admin_id: UUID
