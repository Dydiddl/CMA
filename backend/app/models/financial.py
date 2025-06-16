from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class FinancialRecord(BaseModel):
    __tablename__ = "financial_records"

    contract_id = Column(Integer, ForeignKey("contracts.id"))
    transaction_date = Column(Date)
    amount = Column(Float)
    type = Column(String)  # 수입, 지출
    category = Column(String)  # 자재비, 노무비, 경비 등
    description = Column(Text)
    payment_method = Column(String)  # 현금, 계좌이체, 카드 등
    status = Column(String)  # 미지급, 지급완료 등
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)

    # 관계 설정
    contract = relationship("Contract", back_populates="financial_records")
    vendor = relationship("Vendor", back_populates="financial_records")

class FinancialDocument(BaseModel):
    __tablename__ = "financial_documents"

    financial_record_id = Column(Integer, ForeignKey("financial_records.id"))
    document_type = Column(String)  # 영수증, 세금계산서, 지출증빙 등
    file_path = Column(String)
    file_name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    # 관계 설정
    financial_record = relationship("FinancialRecord", back_populates="documents") 