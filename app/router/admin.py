from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.openapi.models import Server
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.admin import (
    AdminCreate, 
    AdminShow, 
    AdminLogin,
    DashboardResponse,
    UserDetailResponse,
)
from app.schemas.transactions import DepositForm
from app.schemas.users import UserCreate, UserWithAccountResponse
from app.services.admin_service import AdminService
from app.auth.admin import get_current_admin, create_admin_token, authenticate_admin
from app.schemas.token import AdminToken
from app.models.admin import Admin
from uuid import UUID

from app.services.transaction_service import TransactionService

router = APIRouter(tags=["Admin"], prefix="/admin")

@router.post("/auth/register", response_model=AdminShow, status_code=status.HTTP_201_CREATED)
def register_admin(
    db: Annotated[Session, Depends(get_db)], 
    admin_data: AdminCreate
):
    service = AdminService(db)
    admin = service.create_admin(admin_data)
    return AdminShow(
        name=admin.name,
        username=admin.username,
        email=admin.email,
    )

@router.post("/auth/login", response_model=AdminToken)
def login_admin(
    db: Annotated[Session, Depends(get_db)],
    login_data: AdminLogin
):
    admin = authenticate_admin(db, login_data.password, login_data.username,login_data.email)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = create_admin_token(admin_id=admin.id)
    return AdminToken(
        access_token=access_token,
        token_type="bearer",
        admin_id=admin.id
    )

#  USER MANAGEMENT
@router.get("/users", response_model=List[UserDetailResponse])
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Get complete list of all users with full details (admin only)
    """
    service = AdminService(db)
    return service.get_all_users()

@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user_details(
    user_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Get detailed information about a specific user
    """
    service = AdminService(db)
    return service.get_user_by_id(user_id)


@router.post("/users", response_model=UserWithAccountResponse)
def create_user_as_admin(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Create a new user account (admin privilege)
    """
    service = AdminService(db)
    return service.create_user(user_data)

@router.get("/accounts")
def get_account_details(
    db:Annotated[Session,Depends(get_db)],
    current_admin:Annotated[Admin,Depends(get_current_admin)]
):
    service=AdminService(db)
    return service.get_all_accounts()
@router.post("/deposit")
def deposit_to_account(db:Annotated[Session,Depends(get_db)],current_admin:Annotated[Admin,Depends(get_current_admin)],depositor_details:DepositForm):
    service=AdminService(db)
    return service.deopsit_to_account(depositor_details.receiver_account_number,depositor_details.amount)

@router.get("/dashboard",response_model=DashboardResponse)
def dashboard(db:Annotated[Session,Depends(get_db)],current_admin:Annotated[Admin,Depends(get_current_admin)]):
    service=AdminService(db)
    return service.dashboard()
'''
# 💳 TRANSACTION MANAGEMENT
@router.get("/transactions", response_model=List[TransactionDetailResponse])
def get_all_transactions(
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Get complete transaction history
    """
    service = AdminService(db)
    return service.get_all_transactions()

@router.get("/transactions/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction_details(
    transaction_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Get detailed information about a specific transaction
    """
    service = AdminService(db)
    return service.get_transaction_by_id(transaction_id)

@router.post("/transactions/manual")
def create_manual_transaction(
    transaction_data: ManualTransactionCreate,
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Create a manual transaction (admin override)
    """
    service = AdminService(db)
    transaction = service.create_manual_transaction(transaction_data)
    return {"message": "Manual transaction created", "transaction_id": transaction.id}

# 📊 DASHBOARD & ANALYTICS
@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Get admin dashboard statistics
    """
    service = AdminService(db)
    return service.get_dashboard_stats()

@router.get("/reports/transactions")
def generate_transaction_report(
    start_date: datetime,
    end_date: datetime,
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[Admin, Depends(get_current_admin)]
):
    """
    Generate transaction report for given date range
    """
    service = AdminService(db)
    return service.generate_transaction_report(start_date, end_date)
'''
