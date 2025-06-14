from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean, JSON, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid
from backend.app.models.base import Base

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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    version = Column(String(20), nullable=False, default="1.0")
    status = Column(String(50), nullable=False, default="draft")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    document_metadata = Column(JSON, nullable=True)

    # 관계
    project = relationship("Project", back_populates="documents")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_documents")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_documents")
    versions = relationship("DocumentVersion", back_populates="document")
    tags = relationship("DocumentTag", back_populates="document")
    comments = relationship("DocumentComment", back_populates="document")
    shares = relationship("DocumentShare", back_populates="document")

    def __repr__(self):
        return f"<Document {self.title}>"

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    version = Column(String(20), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    changes = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    document = relationship("Document", back_populates="versions")
    creator = relationship("User", back_populates="document_versions")

    def __repr__(self):
        return f"<DocumentVersion {self.document_id} {self.version}>"

class DocumentTag(Base):
    __tablename__ = "document_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    name = Column(String(50), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    document = relationship("Document", back_populates="tags")
    creator = relationship("User", back_populates="document_tags")

    def __repr__(self):
        return f"<DocumentTag {self.name}>"

class DocumentComment(Base):
    __tablename__ = "document_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    document = relationship("Document", back_populates="comments")
    creator = relationship("User", back_populates="document_comments")

    def __repr__(self):
        return f"<DocumentComment {self.document_id}>"

class DocumentShare(Base):
    __tablename__ = "document_shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    permission = Column(String(20), nullable=False, default="read")  # read, write, admin
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # 관계
    document = relationship("Document", back_populates="shares")
    user = relationship("User", foreign_keys=[user_id], back_populates="shared_documents")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_shares")

    def __repr__(self):
        return f"<DocumentShare {self.document_id} {self.user_id}>" 