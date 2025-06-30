from sqlalchemy import String, Boolean, Numeric, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import BaseModel

class Worker(BaseModel):
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

    # 관계 설정
    work_records = relationship("WorkRecord", back_populates="worker")
    salaries = relationship("Salary", back_populates="worker")
    documents = relationship("WorkerDocument", back_populates="worker")

    def __repr__(self):
        return f"<Worker {self.full_name}>"

class WorkRecord(BaseModel):
    """
    작업자의 일일 작업 기록을 관리하는 모델
    """
    worker_id: Mapped[UUID] = mapped_column(ForeignKey('worker.id'), nullable=False)
    work_date: Mapped[Date] = mapped_column(Date, nullable=False)
    hours_worked: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정
    worker = relationship("Worker", back_populates="work_records")

    def __repr__(self):
        return f"<WorkRecord {self.work_date} - {self.worker_id}>"

class Salary(BaseModel):
    """
    작업자의 급여 지급 내역을 관리하는 모델
    """
    worker_id: Mapped[UUID] = mapped_column(ForeignKey('worker.id'), nullable=False)
    payment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), default='pending')  # pending, paid

    # 관계 설정
    worker = relationship("Worker", back_populates="salaries")

    def __repr__(self):
        return f"<Salary {self.payment_date} - {self.worker_id}>"

class WorkerDocument(BaseModel):
    """
    작업자 관련 문서를 관리하는 모델
    """
    worker_id: Mapped[UUID] = mapped_column(ForeignKey('worker.id'), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)  # id_card, contract, etc.
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정
    worker = relationship("Worker", back_populates="documents")

    def __repr__(self):
        return f"<WorkerDocument {self.file_name}>" 