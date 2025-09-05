from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from app.auth.users import get_current_user
from app.db.base import get_db
from app.schemas.accounts import AccountResponse
from sqlalchemy.orm import Session
from app.models.users import User
from app.services.account_service import AccountService


router=APIRouter()



@router.get("/account/",response_model=AccountResponse)
def get_account_details(db:Annotated[Session,Depends(get_db)],current_user:Annotated[User,Depends(get_current_user)]):
    account_service = AccountService(db)
    account_details = account_service.get_account_by_user(current_user)
    return AccountResponse(
        full_name=current_user.full_name,
        account_number=account_details.account_number,
        balance=account_details.balance
    )
