from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class ContractType(enum.Enum):
    CONSTRUCTION = "construction"  # 공사 계약
    MATERIAL = "material"  # 자재 계약
    EQUIPMENT = "equipment"  # 장비 계약
    SERVICE = "service"  # 용역 계약
    OTHER = "other"  # 기타 계약

class ContractStatus(enum.Enum):
    DRAFT = "draft"  # 초안
    PENDING = "pending"  # 검토중
    APPROVED = "approved"  # 승인됨
    ACTIVE = "active"  # 진행중
    COMPLETED = "completed"  # 완료
    TERMINATED = "terminated"  # 종료
    CANCELLED = "cancelled"  # 취소

class PaymentStatus(enum.Enum):
    UNPAID = "unpaid"  # 미지급
    PARTIALLY_PAID = "partially_paid"  # 부분지급
    PAID = "paid"  # 지급완료
    OVERDUE = "overdue"  # 연체

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), unique=True, nullable=False)
    contract_type = Column(Enum(ContractType), nullable=False)
    status = Column(Enum(ContractStatus), default=ContractStatus.DRAFT)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # 계약 당사자 정보
    client_name = Column(String(100), nullable=False)
    client_contact = Column(String(100))
    client_address = Column(String(200))
    client_phone = Column(String(20))
    client_email = Column(String(100))
    
    # 계약 기간
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    actual_start_date = Column(DateTime)
    actual_end_date = Column(DateTime)
    
    # 금액 정보
    contract_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="KRW")
    payment_terms = Column(Text)
    payment_schedule = Column(JSON)  # 지급 일정
    
    # 담당자 정보
    manager_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # 계약서 파일
    contract_file_url = Column(String(200))
    attachments = Column(JSON)  # 첨부파일 목록
    
    # 기타 정보
    terms_and_conditions = Column(Text)
    special_conditions = Column(Text)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    manager = relationship("User", back_populates="managed_contracts")
    department = relationship("Department", back_populates="contracts")
    amendments = relationship("ContractAmendment", back_populates="contract")
    payments = relationship("ContractPayment", back_populates="contract")

class ContractAmendment(Base):
    __tablename__ = "contract_amendments"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    amendment_number = Column(String(50), nullable=False)
    amendment_date = Column(DateTime, nullable=False)
    reason = Column(Text, nullable=False)
    changes = Column(JSON, nullable=False)  # 변경사항 상세
    status = Column(Enum(ContractStatus), default=ContractStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    contract = relationship("Contract", back_populates="amendments")
    approver = relationship("User", back_populates="approved_amendments")

class ContractPayment(Base):
    __tablename__ = "contract_payments"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    payment_number = Column(String(50), nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)
    payment_date = Column(DateTime)
    payment_method = Column(String(50))
    payment_reference = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    contract = relationship("Contract", back_populates="payments") 