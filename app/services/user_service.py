# app/services/user_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models import accounts
from app.models.users import User
from app.auth.users import get_password_hash
from app.schemas.users import UserCreate, UserResponse, UserUpdateForm, UserWithAccountResponse,UserUpdateResponse
from .account_service import AccountService
from sqlalchemy.orm import joinedload

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.account_service = AccountService(db)

    def create_user(self, user: UserCreate):
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

    def get_current_user_details(self,user_id:UUID):
        user=self.db.query(User).options(joinedload(User.accounts)).filter(User.id==user_id).first()
        if not user:
            raise HTTPException(status_code=404,detail="user not found")
        if not user.accounts:
            raise HTTPException(status_code=404,detail="no account details found for the current user")
        account=user.accounts[0]   #$RElationship between user and account is one to manny and return list

        return UserWithAccountResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                account_number=account.account_number,
                account_type=account.account_type,
                balance=account.balance
 
        )

    def update_user_details(self,user_data:UserUpdateForm,user_id:UUID):
        user=self.db.query(User).filter(User.id==user_id).first()
        if not user:
            raise HTTPException(status_code=404,detail="user is not found")
        updated_fields = {}

        if user_data.full_name is not None:
            user.full_name = user_data.full_name
            updated_fields["full_name"] = user.full_name

        if user_data.email is not None:
            user.email = user_data.email
            updated_fields["email"] = user.email

        if user_data.username is not None:
            user.username = user_data.username
            updated_fields["username"] = user.username

        if user_data.password is not None:
            user.hashed_password = get_password_hash(user_data.password)

        self.db.commit()
        self.db.refresh(user)
        return UserUpdateResponse(message=f"user is updated successfully",updated_field=updated_fields) 

    

