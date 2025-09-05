from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone
from app.db.base import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .accounts import Account

class BankTransaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    type: Mapped[str] = mapped_column(String(50), nullable=False) 
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    account: Mapped["Account"] = relationship(back_populates="transactions")