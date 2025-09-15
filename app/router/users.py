from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import (
    UserCreate,
    UserResponse,
    UserLogin,
    UserUpdateForm,
    UserUpdateResponse,
    UserWithAccountResponse,
)
from app.db.base import get_db
from app.auth.users import (
    get_current_user,
    get_password_hash,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_user_token,
)
from typing import Annotated
from app.schemas.token import Token
from datetime import timedelta
from app.services.user_service import UserService

router = APIRouter()


@router.post("/create", response_model=UserWithAccountResponse)
def register_user(db: Annotated[Session, Depends(get_db)], user: UserCreate):
    user_service = UserService(db)
    new_user = user_service.create_user(user)
    return new_user


@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Annotated[Session, Depends(get_db)]):
    auth_user = authenticate_user(db, user)
    access_token_expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_user_token(
        user_id=auth_user.id, expires_delta=access_token_expire_time
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserWithAccountResponse)
def current_users_details(
    db: Annotated[Session, Depends(get_db)],
    users: Annotated[User, Depends(get_current_user)],
):
    service = UserService(db)
    current_user_data = service.get_current_user_details(users.id)
    return current_user_data


@router.patch("/me", response_model=UserUpdateResponse)
def update_user_profile(
    user_update: UserUpdateForm,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service = UserService(db)
    updated_data = service.update_user_details(user_update, current_user.id)
    return updated_data
