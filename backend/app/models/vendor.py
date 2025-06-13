from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base
import uuid

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name = Column(String, nullable=False, index=True)
    business_number = Column(String, unique=True, nullable=False, index=True)
    representative = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String)
    
    # JSON 필드로 은행 정보 저장
    bank_info = Column(JSON)  # {"bank_name": "국민은행", "account_number": "123-456-789"}
    
    # JSON 필드로 문서 메타데이터 저장
    documents = Column(JSON)  # {"business_license": "path/to/file", "bank_copy": "path/to/file"}
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 관계 설정
    contracts = relationship("Contract", back_populates="vendor") 