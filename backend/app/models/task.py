from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.app.models.base import Base

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(Base):
    """
    태스크 정보를 저장하는 테이블
    프로젝트 내의 개별 작업 항목을 관리합니다.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # 태스크 고유 식별자
    name = Column(String, index=True)  # 태스크명
    description = Column(String)  # 태스크 설명
    status = Column(String)  # 태스크 상태 (대기중, 진행중, 완료 등)
    progress = Column(Float, default=0.0)  # 진행률 (0.0 ~ 1.0)
    start_date = Column(DateTime)  # 태스크 시작일
    end_date = Column(DateTime)  # 태스크 종료일
    project_id = Column(Integer, ForeignKey("projects.id"))  # 소속 프로젝트 ID
    assignee_id = Column(Integer, ForeignKey("users.id"))  # 담당자 ID
    created_at = Column(DateTime, default=datetime.utcnow)  # 태스크 생성 일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 정보 수정 일시

    # 관계 설정
    project = relationship("Project", back_populates="tasks")  # 태스크가 속한 프로젝트
    assignee = relationship("User", back_populates="tasks")  # 태스크 담당자

    def __repr__(self):
        return f"<Task {self.name}>" 