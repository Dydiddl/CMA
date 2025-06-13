from sqlalchemy import String, Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base

class Contract(Base):
    """
    계약 정보를 관리하는 모델
    """
    contract_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    client_id: Mapped[UUID] = mapped_column(ForeignKey('client.id'), nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # pending, active, completed, cancelled
    contract_type: Mapped[str] = mapped_column(String(50), nullable=False)  # construction, maintenance, consulting
    created_by: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)

    # 관계 설정
    client = relationship("Client", back_populates="contracts")
    creator = relationship("User", back_populates="created_contracts")
    labor_costs = relationship("LaborCost", back_populates="contract")
    revenues = relationship("Revenue", back_populates="contract")
    expenses = relationship("Expense", back_populates="contract")
    documents = relationship("Document", back_populates="contract")

    def __repr__(self):
        return f"<Contract {self.contract_number}>" 