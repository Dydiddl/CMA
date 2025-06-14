from sqlalchemy import Column, String, DateTime, Date, Numeric, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_type = Column(String, nullable=False, index=True)  # income(수입), expense(지출)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_date = Column(Date, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # 계약금, 중도금, 잔금, 자재비, 인건비 등
    description = Column(Text)
    
    # 외래키
    contract_id = Column(String, ForeignKey("contracts.id"), nullable=False)
    
    # JSON 필드로 관련 문서 메타데이터 저장
    documents = Column(JSON)  # {"receipt": "path/to/file", "invoice": "path/to/file"}
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    contract = relationship("Contract", back_populates="transactions") 