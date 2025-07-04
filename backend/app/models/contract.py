"""
계약 모델 모듈
"""
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base
import uuid

class Contract(Base):
    """계약 모델"""
    __tablename__ = "contracts"

    # 기본 정보
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True, comment="계약명")
    contract_number = Column(String(50), unique=True, nullable=False, index=True, comment="계약번호")
    contract_amount = Column(Float, nullable=False, comment="계약금액")
    contract_date = Column(DateTime, nullable=False, comment="계약일")
    start_date = Column(DateTime, nullable=True, comment="시작일")
    end_date = Column(DateTime, nullable=True, comment="종료일")
    
    # 발주처 정보
    client_name = Column(String(255), nullable=False, comment="발주처명")
    client_contact = Column(String(100), nullable=True, comment="발주처 연락처")
    
    # 상태 및 설명
    status = Column(String(50), nullable=False, default="진행중", comment="계약 상태")
    description = Column(Text, nullable=True, comment="계약 설명")
    
    # 소프트 삭제
    deleted_at = Column(DateTime, nullable=True, comment="삭제일")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="삭제 여부")
    
    # 외래키
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False, comment="거래처 ID")
    project_id = Column(String, ForeignKey("projects.id"), nullable=True, comment="프로젝트 ID")
    user_id = Column(String, ForeignKey("users.id"), nullable=True, comment="사용자 ID")
    
    # 관계 설정
    vendor = relationship("Vendor", back_populates="contracts")
    project = relationship("Project", back_populates="contracts")
    user = relationship("User")
    documents = relationship("ContractDocument", back_populates="contract", cascade="all, delete-orphan")
    financial_records = relationship("FinancialRecord", back_populates="contract", cascade="all, delete-orphan")
    labors = relationship("Labor", back_populates="contract", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="contract")
    
    def __repr__(self) -> str:
        """문자열 표현"""
        return f"<Contract(id={self.id}, name='{self.name}', contract_number='{self.contract_number}')>"

class ContractDocument(Base):
    """계약 문서 모델"""
    __tablename__ = "contract_documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String, ForeignKey("contracts.id"), nullable=False, comment="계약 ID")
    document_type = Column(String(50), nullable=False, comment="문서 유형")
    file_path = Column(String(500), nullable=False, comment="파일 경로")
    file_name = Column(String(255), nullable=False, comment="파일명")
    upload_date = Column(DateTime, default=datetime.utcnow, comment="업로드일")
    description = Column(Text, nullable=True, comment="문서 설명")

    # 관계 설정
    contract = relationship("Contract", back_populates="documents")
    
    def __repr__(self) -> str:
        """문자열 표현"""
        return f"<ContractDocument(id={self.id}, document_type='{self.document_type}', file_name='{self.file_name}')>" 