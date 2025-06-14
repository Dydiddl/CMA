from sqlalchemy import Date, Numeric, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from app.models.base import Base

class Expense(Base):
    """
    비용 지출 내역을 관리하는 모델
    """
    contract_id: Mapped[UUID] = mapped_column(ForeignKey('contract.id'), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # material, equipment, subcontract, other
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)  # 비용금액
    expense_date: Mapped[Date] = mapped_column(Date, nullable=False)  # 지출일
    description: Mapped[str] = mapped_column(Text, nullable=True)  # 비고
    payment_status: Mapped[str] = mapped_column(String(20), default='pending')  # pending, paid

    # 관계 설정
    contract = relationship("Contract", back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.expense_date} - {self.amount}>" 