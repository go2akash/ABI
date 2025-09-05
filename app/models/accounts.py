from sqlalchemy import Float, ForeignKey, String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone
from app.db.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .transactions import BankTransaction

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    account_number: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="accounts")
    transactions: Mapped[List["BankTransaction"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="selectin"
    )