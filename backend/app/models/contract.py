from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class Contract(BaseModel):
    __tablename__ = "contracts"

    name = Column(String, index=True)
    contract_number = Column(String, unique=True, index=True)
    contract_amount = Column(Float)
    contract_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    client_name = Column(String)
    client_contact = Column(String)
    status = Column(String)  # 진행중, 완료, 중단 등
    description = Column(Text)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    # 관계 설정
    vendor = relationship("Vendor", back_populates="contracts")
    documents = relationship("ContractDocument", back_populates="contract")
    financial_records = relationship("FinancialRecord", back_populates="contract")

class ContractDocument(BaseModel):
    __tablename__ = "contract_documents"

    contract_id = Column(Integer, ForeignKey("contracts.id"))
    document_type = Column(String)  # 계약서, 견적서, 명세서 등
    file_path = Column(String)
    file_name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    # 관계 설정
    contract = relationship("Contract", back_populates="documents") 