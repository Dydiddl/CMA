from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models.base import Base

class DependencyType(str, enum.Enum):
    BLOCKS = "blocks"  # 차단 관계
    BLOCKED_BY = "blocked_by"  # 차단됨 관계
    RELATES_TO = "relates_to"  # 관련 관계
    DUPLICATES = "duplicates"  # 중복 관계
    DUPLICATED_BY = "duplicated_by"  # 중복됨 관계

class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id = Column(Integer, primary_key=True, index=True)
    source_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    target_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    dependency_type = Column(Enum(DependencyType), nullable=False)
    description = Column(String(500), nullable=True)
    
    # 관계 설정
    source_task = relationship("Task", foreign_keys=[source_task_id], back_populates="outgoing_dependencies")
    target_task = relationship("Task", foreign_keys=[target_task_id], back_populates="incoming_dependencies")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<TaskDependency {self.source_task_id} -> {self.target_task_id}>" 