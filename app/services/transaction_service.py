from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.transactions import BankTransaction
from app.auth import users
from app.auth.users import get_current_user
from app.models.users import User
from app.models.accounts import Account
from app.schemas.transactions import TransferForm



class TransactionService:
    def __init__(self,db:Session):
        self.db=db
    
    def transfer_to_account(self,sender_user:User,receiver_data:TransferForm):
        sender_account=self.db.query(Account).filter(Account.user_id==sender_user.id).first()
        if not sender_account:
            raise HTTPException(status_code=404,detail="no account is linked to the user")
        receiver_account=self.db.query(Account).filter(Account.account_number==receiver_data.receiver_account_number).first()
        if not receiver_account:
            raise HTTPException(status_code=404, detail="Receiver account not found")
        
        if sender_account.balance<receiver_data.amount:
            raise HTTPException(status_code=400,detail="insufficient balance")
        try:
            sender_account.balance   -= receiver_data.amount
            receiver_account.balance += receiver_data.amount

            new_tx = BankTransaction(
                account_id=sender_account.id,
                amount=receiver_data.amount,
                type="transfer",
                status="completed"
            )
            self.db.add_all([sender_account, receiver_account, new_tx])
            self.db.commit()
            self.db.refresh(new_tx)
            return new_tx
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Transaction failed")



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
 



