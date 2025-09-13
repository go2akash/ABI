# app/services/user_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.users import User
from app.auth.users import get_password_hash
from app.schemas.users import UserCreate, UserResponse, UserWithAccountResponse
from .account_service import AccountService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.account_service = AccountService(db)

    def create_user(self, user: UserCreate, return_account: bool = False):
        if self.db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
            raise HTTPException(status_code=409, detail="Username or email already exists")

        hashed_password = get_password_hash(user.password)

        new_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            is_active=user.is_active
        )

        try:
            self.db.add(new_user)
            self.db.flush()  # ensures new_user.id exists for account FK

            # Create first account
            account = self.account_service.create_account_for_user(
                new_user,
                account_type=user.account_type
            )

            self.db.commit()
            self.db.refresh(new_user)
            
            return UserWithAccountResponse(
                id=new_user.id,
                username=new_user.username,
                email=new_user.email,
                full_name=new_user.full_name,
                is_active=new_user.is_active,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at,
                account_number=account.account_number,
                account_type=account.account_type,
                balance=account.balance
            )

        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Failed to create user or account")
