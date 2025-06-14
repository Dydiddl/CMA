from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class DocumentType(str, enum.Enum):
    CONTRACT = "contract"  # 계약서
    DRAWING = "drawing"    # 도면
    REPORT = "report"      # 보고서
    PHOTO = "photo"        # 사진
    INSPECTION = "inspection"  # 검사서
    CERTIFICATE = "certificate"  # 인증서
    OTHER = "other"        # 기타

class DocumentStatus(str, enum.Enum):
    DRAFT = "draft"        # 초안
    PENDING = "pending"    # 검토중
    APPROVED = "approved"  # 승인됨
    REJECTED = "rejected"  # 반려됨
    ARCHIVED = "archived"  # 보관됨

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)  # 파일 크기 (바이트)
    version = Column(Integer, default=1)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

    # 관계
    project = relationship("Project", back_populates="documents")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_documents")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    tags = relationship("DocumentTag", back_populates="document", cascade="all, delete-orphan")
    comments = relationship("DocumentComment", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)
    changes = Column(Text)  # 변경 사항 설명
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    document = relationship("Document", back_populates="versions")
    creator = relationship("User", back_populates="document_versions")

class DocumentTag(Base):
    __tablename__ = "document_tags"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    name = Column(String(50), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    document = relationship("Document", back_populates="tags")
    creator = relationship("User", back_populates="document_tags")

class DocumentComment(Base):
    __tablename__ = "document_comments"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)

    # 관계
    document = relationship("Document", back_populates="comments")
    creator = relationship("User", back_populates="document_comments")

class DocumentShare(Base):
    __tablename__ = "document_shares"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission = Column(String(20), nullable=False)  # read, write, admin
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    # 관계
    document = relationship("Document")
    user = relationship("User", foreign_keys=[user_id])
    creator = relationship("User", foreign_keys=[created_by]) 