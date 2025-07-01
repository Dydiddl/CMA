from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import BaseModel
from datetime import datetime

class Vendor(BaseModel):
    __tablename__ = "vendors"
    
    name = Column(String, nullable=False, index=True)
    business_number = Column(String, unique=True, nullable=False, index=True)
    representative = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    bank_account = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # JSON 필드로 은행 정보 저장
    bank_info = Column(JSON)  # {"bank_name": "국민은행", "account_number": "123-456-789"}
    
    # JSON 필드로 문서 메타데이터 저장
    documents = Column(JSON)  # {"business_license": "path/to/file", "bank_copy": "path/to/file"}
    
    # 관계 설정
    contracts = relationship("Contract", back_populates="vendor")
    projects = relationship("Project", back_populates="vendor")
    financial_records = relationship("FinancialRecord", back_populates="vendor")
    vendor_documents = relationship("VendorDocument", back_populates="vendor")

class VendorDocument(BaseModel):
    __tablename__ = "vendor_documents"

    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    document_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    # 관계 설정
    vendor = relationship("Vendor", back_populates="vendor_documents") 