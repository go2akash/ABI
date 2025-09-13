from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.admin import Admin 
from app.schemas.admin import AdminShow,AdminCreate
from app.models.users import User
from app.services.user_service import UserService



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
            password=data.password,
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
        return user_service.create_user(user_data, return_account=True)