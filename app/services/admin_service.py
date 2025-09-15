from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.auth.admin import get_hashed_admin_password
from app.models.accounts import Account
from app.models.admin import Admin 
from app.schemas.admin import AdminShow,AdminCreate, DashboardResponse
from app.models.users import User
from app.services.user_service import UserService
from app.services.transaction_service import BankTransaction


class AdminService:
    def __init__(self,db:Session):
        self.db=db

    def create_admin(self,data:AdminCreate):
        admin=self.db.query(Admin).filter(Admin.username==data.username or Admin.email==data.email).first()
        if admin:
            raise HTTPException(status_code=401,detail="username or password already exist")
        new_admin=Admin(
            email=data.email,
            name=data.name,
            password=get_hashed_admin_password(data.password),
            username=data.username
        )
        try:
            self.db.add(new_admin)
            self.db.commit()
            self.db.refresh(new_admin)
            return new_admin
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Failed to create admin")
        
    def get_all_users(self):
        users = self.db.query(User).all()
        return users
    def get_user_by_id(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def create_user(self, user_data):
        user_service = UserService(self.db)
        return user_service.create_user(user_data)
    
    def get_all_accounts(self):
        accounts=self.db.query(Account).all()
        if not accounts:
            raise HTTPException(status_code=404,detail="There is no accounts")
        return accounts


    def deopsit_to_account(self,account_number:int,amount:float):
        reciever_account=self.db.query(Account).filter(Account.account_number==account_number).first()
        if not reciever_account:
            raise HTTPException(status_code=404,detail="Account number not find")
        try:
            reciever_account.balance+=amount
            new_tx= BankTransaction(
                    account_id=reciever_account.id,
                    amount=amount,
                    type="deposit",
                    status="completed"

                )
            self.db.add_all([reciever_account,new_tx])
            self.db.commit()
            self.db.refresh(new_tx)
            return new_tx
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Transaction failed")
 

    def dashboard(self):
        total_users = self.db.query(func.count(User.id)).scalar()
        total_accounts = self.db.query(func.count(Account.id)).scalar()
        total_transactions = self.db.query(func.count(BankTransaction.id)).scalar()
        total_account_balance = self.db.query(func.coalesce(func.sum(Account.balance), 0)).scalar()

        return DashboardResponse(
            total_users=total_users,
            total_accounts=total_accounts,
            total_transactions=total_transactions,
            total_account_balance=total_account_balance
        )

