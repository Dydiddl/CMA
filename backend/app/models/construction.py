from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float, Enum, JSON, UUID, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid
from backend.app.models.base import Base

class ConstructionStatus(str, enum.Enum):
    PLANNING = "planning"  # 계획
    BIDDING = "bidding"  # 입찰
    CONTRACTED = "contracted"  # 계약
    IN_PROGRESS = "in_progress"  # 진행중
    COMPLETED = "completed"  # 완료
    SUSPENDED = "suspended"  # 중단
    TERMINATED = "terminated"  # 해지

class ConstructionType(str, enum.Enum):
    NEW_CONSTRUCTION = "new_construction"  # 신축
    RENOVATION = "renovation"  # 리모델링
    REPAIR = "repair"  # 보수
    DEMOLITION = "demolition"  # 철거

class Construction(Base):
    __tablename__ = "constructions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="PLANNING")  # PLANNING, IN_PROGRESS, COMPLETED, ON_HOLD
    budget = Column(Float, nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    manager = relationship("User", back_populates="managed_constructions")
    documents = relationship("ConstructionDocument", back_populates="construction")
    history = relationship("ConstructionHistory", back_populates="construction")
    progress = relationship("ConstructionProgress", back_populates="construction")

    def __repr__(self):
        return f"<Construction {self.name}>"

class ConstructionProgress(Base):
    __tablename__ = "construction_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    construction_id = Column(UUID(as_uuid=True), ForeignKey("constructions.id"), nullable=False)
    progress_date = Column(Date, nullable=False)
    progress_percentage = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    construction = relationship("Construction", back_populates="progress")

    def __repr__(self):
        return f"<ConstructionProgress {self.construction_id} {self.progress_date}>"

class ConstructionDocument(Base):
    __tablename__ = "construction_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    construction_id = Column(UUID(as_uuid=True), ForeignKey("constructions.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    construction = relationship("Construction", back_populates="documents")
    uploader = relationship("User", back_populates="uploaded_documents")

    def __repr__(self):
        return f"<ConstructionDocument {self.title}>"

class ConstructionHistory(Base):
    __tablename__ = "construction_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    construction_id = Column(UUID(as_uuid=True), ForeignKey("constructions.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    previous_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    construction = relationship("Construction", back_populates="history")
    user = relationship("User", back_populates="construction_changes")

    def __repr__(self):
        return f"<ConstructionHistory {self.construction_id} {self.action_type}>" 