from sqlalchemy import String, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Worker(Base):
    """
    작업자(인력) 정보를 관리하는 모델
    """
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    id_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    bank_account: Mapped[str] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str] = mapped_column(String(50), nullable=True)
    hourly_rate: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"<Worker {self.full_name}>" 