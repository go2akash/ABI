from datetime import UTC, datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
import os
from uuid import UUID
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from sqlalchemy.util import deprecated

from app.auth.users import ALGORITHM
from dotenv import load_dotenv

from app.db.base import get_db
from app.models.admin import Admin


load_dotenv()


ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")
if not ADMIN_SECRET_KEY:
    raise HTTPException(status_code=404, detail="Missing secrate key")
ALGORITHM = "HS256"
ADMIN_ACCESS_TOKEN_EXPIRE = timedelta(hours=6)


admin_oauth2_schema = OAuth2PasswordBearer(tokenUrl="/admin/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_admin_password(password: str):
    return pwd_context.hash(password)


def verify_admin_password(password: str, hash_password: str):
    return pwd_context.verify(password, hash_password)


def get_admin(db: Session, username: str | None, email: str | None):
    if not username and not email:
        return None
    admin = (
        db.query(Admin)
        .filter(or_(Admin.username == username, Admin.email == email))
        .first()
    )
    return admin


def authenticate_admin(
    db: Session, password: str, username: str | None = None, email: str | None = None
):
    if not username and not email:
        return False
    admin = get_admin(db, username, email)
    if not admin:
        return False
    if not verify_admin_password(password, admin.password):
        return False
    return admin


def create_admin_token(*, admin_id: UUID, expireDelta: timedelta | None = None):
    now = datetime.now(timezone.utc)
    payload = {
        "exp": now + (expireDelta or timedelta(minutes=30)),
        "sub": str(admin_id),
        "iat": now,
    }
    return jwt.encode(payload, key=ADMIN_SECRET_KEY, algorithm=ALGORITHM)


def get_admin_by_adminid(db: Session, admin_id: UUID):
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_current_admin(
    token: Annotated[str, Depends(admin_oauth2_schema)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ADMIN_SECRET_KEY, algorithms=[ALGORITHM])
        admin_id_in_str = payload.get("sub")
        if admin_id_in_str is None:
            raise credentials_exception
        admin_id = UUID(admin_id_in_str)
    except (InvalidTokenError, ValueError):
        raise credentials_exception
    admin = get_admin_by_adminid(db, admin_id)
    if admin is None:
        raise credentials_exception
    return admin
