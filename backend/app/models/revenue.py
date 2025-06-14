from sqlalchemy import Date, Numeric, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from app.models.base import Base

class Revenue(Base):
    """
    수입 내역을 관리하는 모델
    """
    contract_id: Mapped[UUID] = mapped_column(ForeignKey('contract.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)  # 수입금액
    payment_date: Mapped[Date] = mapped_column(Date, nullable=False)  # 수입일
    payment_type: Mapped[str] = mapped_column(String(20), nullable=False)  # cash, transfer, check
    status: Mapped[str] = mapped_column(String(20), default='pending')  # pending, received
    description: Mapped[str] = mapped_column(Text, nullable=True)  # 비고

    # 관계 설정
    contract = relationship("Contract", back_populates="revenues")

    def __repr__(self):
        return f"<Revenue {self.payment_date} - {self.amount}>" 