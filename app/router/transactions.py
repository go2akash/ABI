from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.users import get_current_user
from app.db.base import get_db
from app.models.users import User
from app.schemas.transactions import TransactionResponse, TransferForm
from app.services.transaction_service import TransactionService


router = APIRouter()


@router.post("/transfers", response_model=TransactionResponse)
def send_to_account(
    form: TransferForm,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = TransactionService(db)
    tx = service.transfer_to_account(current_user, form)

    return TransactionResponse(
        amount=tx.amount,
        type=tx.type,
        created_at=tx.created_at.isoformat(),  # ← string for JSON
        account=tx.account.account_number,  # ← relationship magic
        status=tx.status,
    )
