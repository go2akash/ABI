# app/services/account_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.accounts import Account
from app.models.users import User
import random


class AccountService:
    VALID_ACCOUNT_TYPES = {"savings", "current", "business"}

    def __init__(self, db: Session):
        self.db = db

    def _generate_account_number(self) -> int:
        """
        Generate a unique 10-digit account number.
        Retry if collision occurs.
        """
        for _ in range(10):
            number = random.randint(10**9, 10**10 - 1)
            exists = (
                self.db.query(Account).filter(Account.account_number == number).first()
            )
            if not exists:
                return number
        raise HTTPException(
            status_code=500, detail="Failed to generate unique account number"
        )

    def create_account_for_user(
        self, user: User, account_type: str = "savings"
    ) -> Account:
        """
        Create a new account for the user.
        """
        account_type = account_type.lower()
        if account_type not in self.VALID_ACCOUNT_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Invalid account type '{account_type}'"
            )

        account_number = self._generate_account_number()
        new_account = Account(
            user_id=user.id,
            account_number=account_number,
            account_type=account_type,
            balance=0.0,
        )

        self.db.add(new_account)
        try:
            self.db.flush()  # ensures new_account.id exists for relationship
            return new_account
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail="Failed to create account")

    def get_account_by_user(self, user: User) -> Account:
        account = self.db.query(Account).filter(Account.user_id == user.id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
