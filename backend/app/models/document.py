from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class DocumentType(str, enum.Enum):
    CONTRACT = "contract"           # 계약서
    DRAWING = "drawing"            # 도면
    SPECIFICATION = "specification" # 시방서
    PERMIT = "permit"              # 허가서
    REPORT = "report"              # 보고서
    INSPECTION = "inspection"      # 검사서
    SAFETY = "safety"              # 안전관련
    QUALITY = "quality"            # 품질관련
    FINANCIAL = "financial"        # 재무관련
    OTHER = "other"                # 기타

class DocumentStatus(str, enum.Enum):
    DRAFT = "draft"               # 초안
    UNDER_REVIEW = "under_review" # 검토중
    APPROVED = "approved"         # 승인됨
    REJECTED = "rejected"         # 반려됨
    ARCHIVED = "archived"         # 보관됨

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    description = Column(Text)
    file_url = Column(String(500))
    file_name = Column(String(200))
    file_size = Column(Integer)  # 파일 크기 (bytes)
    file_type = Column(String(50))  # 파일 MIME 타입
    version = Column(String(20))
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    metadata = Column(JSON)  # 추가 메타데이터 (예: 도면 번호, 검사 항목 등)
    
    # 관계
    construction_id = Column(Integer, ForeignKey("constructions.id"))
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # 생성/수정 시간
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    construction = relationship("Construction", back_populates="documents")
    contract = relationship("Contract", back_populates="documents")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    department = relationship("Department", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document")
    approvals = relationship("DocumentApproval", back_populates="document")

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    version_number = Column(String(20), nullable=False)
    file_url = Column(String(500))
    file_name = Column(String(200))
    file_size = Column(Integer)
    file_type = Column(String(50))
    changes = Column(Text)  # 변경 내용
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    document = relationship("Document", back_populates="versions")
    creator = relationship("User")

class DocumentApproval(Base):
    __tablename__ = "document_approvals"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    approver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UNDER_REVIEW)
    comments = Column(Text)
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    document = relationship("Document", back_populates="approvals")
    approver = relationship("User") 