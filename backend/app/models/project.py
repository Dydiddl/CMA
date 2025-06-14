from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from backend.app.models.base import Base

class Project(Base):
    """
    프로젝트 정보를 저장하는 테이블
    건설 프로젝트의 기본 정보와 진행 상태를 관리합니다.
    """
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, index=True)
    is_active = Column(Boolean(), default=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget = Column(Float, nullable=True)
    location = Column(String(200), nullable=True)
    
    # 관계 설정
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="projects", foreign_keys=[owner_id])
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    manager = relationship("User", back_populates="projects", foreign_keys=[manager_id])
    progresses = relationship("Progress", back_populates="project")
    financial_records = relationship("FinancialRecord", back_populates="project")
    documents = relationship("Document", back_populates="project")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Project {self.name}>" 