from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

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
    
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    versions = relationship("APIDocVersion", back_populates="api_doc")
    tags = relationship("APIDocTag", back_populates="api_doc")
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

class APIDocTag(Base):
    __tablename__ = "api_doc_tags"

    id = Column(Integer, primary_key=True, index=True)
    api_doc_id = Column(Integer, ForeignKey("api_docs.id"))
    name = Column(String(50), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    api_doc = relationship("APIDoc", back_populates="tags")
    creator = relationship("User", foreign_keys=[created_by])

class APIDocComment(Base):
    __tablename__ = "api_doc_comments"

    id = Column(Integer, primary_key=True, index=True)
    api_doc_id = Column(Integer, ForeignKey("api_docs.id"))
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)
    
    # Relationships
    api_doc = relationship("APIDoc", back_populates="comments")
    creator = relationship("User", foreign_keys=[created_by]) 