from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base
import uuid

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String, ForeignKey("contracts.id"), nullable=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    transaction_date = Column(Date)
    date = Column(Date, nullable=True)
    amount = Column(Float)
    type = Column(String)  # 수입, 지출
    category = Column(String)  # 자재비, 노무비, 경비 등
    description = Column(Text)
    payment_method = Column(String)  # 현금, 계좌이체, 카드 등
    status = Column(String)  # 미지급, 지급완료 등
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, comment="사용자 ID")

    # 관계 설정
    contract = relationship("Contract", back_populates="financial_records")
    project = relationship("Project", back_populates="financial_records")
    vendor = relationship("Vendor", back_populates="financial_records")
    documents = relationship("FinancialDocument", back_populates="financial_record", cascade="all, delete-orphan")

    @property
    def total_cost(self):
        """총 비용 계산"""
        return self.amount if self.amount else 0.0

    def __repr__(self):
        return f"<FinancialRecord(id={self.id}, amount={self.amount}, type={self.type})>"

class FinancialDocument(Base):
    __tablename__ = "financial_documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    financial_record_id = Column(String, ForeignKey("financial_records.id"))
    document_type = Column(String)  # 영수증, 세금계산서, 지출증빙 등
    file_path = Column(String)
    file_name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    # 관계 설정
    financial_record = relationship("FinancialRecord", back_populates="documents") 