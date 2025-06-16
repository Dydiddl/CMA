from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base
import uuid
from datetime import datetime

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
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
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 관계 설정
    contracts = relationship("Contract", back_populates="vendor")
    financial_records = relationship("FinancialRecord", back_populates="vendor")
    vendor_documents = relationship("VendorDocument", back_populates="vendor")

class VendorDocument(Base):
    __tablename__ = "vendor_documents"

    id = Column(Integer, primary_key=True)
    vendor_id = Column(String, ForeignKey("vendors.id"))
    document_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    # 관계 설정
    vendor = relationship("Vendor", back_populates="vendor_documents") 