from sqlalchemy import Date, Numeric, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from app.models.base import Base

class LaborCost(Base):
    """
    인건비 지급 내역을 관리하는 모델
    """
    contract_id: Mapped[UUID] = mapped_column(ForeignKey('contract.id'), nullable=False)
    worker_id: Mapped[UUID] = mapped_column(ForeignKey('worker.id'), nullable=False)
    work_date: Mapped[Date] = mapped_column(Date, nullable=False)
    hours_worked: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)  # 작업시간
    hourly_rate: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # 시급
    total_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)  # 총액
    payment_status: Mapped[str] = mapped_column(String(20), default='pending')  # pending, paid

    # 관계 설정
    contract = relationship("Contract", back_populates="labor_costs")
    worker = relationship("Worker", back_populates="labor_costs")

    def __repr__(self):
        return f"<LaborCost {self.work_date} - {self.worker_id}>" 