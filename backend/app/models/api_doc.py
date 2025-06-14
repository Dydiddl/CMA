from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, JSON, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.app.models.base import Base

class APIDocStatus(str, enum.Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"

class APIDocType(str, enum.Enum):
    ENDPOINT = "endpoint"
    MODEL = "model"
    SCHEMA = "schema"
    UTILITY = "utility"

# API 문서와 태그의 다대다 관계를 위한 중간 테이블
api_doc_tag = Table(
    "api_doc_tag",
    Base.metadata,
    Column("api_doc_id", Integer, ForeignKey("api_docs.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class APIDoc(Base):
    __tablename__ = "api_docs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    doc_type = Column(Enum(APIDocType), nullable=False)
    status = Column(Enum(APIDocStatus), default=APIDocStatus.DRAFT)
    version = Column(String(50))
    endpoint = Column(String(255))
    method = Column(String(10))
    request_schema = Column(JSON)
    response_schema = Column(JSON)
    parameters = Column(JSON)
    examples = Column(JSON)
    metadata = Column(JSON)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    versions = relationship("APIDocVersion", back_populates="api_doc")
    tags = relationship("Tag", secondary=api_doc_tag, back_populates="api_docs")
    comments = relationship("APIDocComment", back_populates="api_doc")

class APIDocVersion(Base):
    __tablename__ = "api_doc_versions"

    id = Column(Integer, primary_key=True, index=True)
    api_doc_id = Column(Integer, ForeignKey("api_docs.id"))
    version_number = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    changes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    api_doc = relationship("APIDoc", back_populates="versions")
    creator = relationship("User", foreign_keys=[created_by])

class APIDocComment(Base):
    __tablename__ = "api_doc_comments"

    id = Column(Integer, primary_key=True, index=True)
    api_doc_id = Column(Integer, ForeignKey("api_docs.id"))
    parent_id = Column(Integer, ForeignKey("api_doc_comments.id"))  # 대댓글을 위한 필드
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, ForeignKey("users.id"))
    is_resolved = Column(Boolean, default=False)
    
    # Relationships
    api_doc = relationship("APIDoc", back_populates="comments")
    parent = relationship("APIDocComment", remote_side=[id], backref="replies")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))

    # 관계 설정
    api_docs = relationship("APIDoc", secondary=api_doc_tag, back_populates="tags")
    creator = relationship("User", back_populates="created_tags") 