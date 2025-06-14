from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class NotificationType(str, enum.Enum):
    TASK_DUE = "task_due"  # 작업 마감일
    TASK_STATUS = "task_status"  # 작업 상태 변경
    TASK_ASSIGNED = "task_assigned"  # 작업 할당
    FILE_UPLOADED = "file_uploaded"  # 파일 업로드
    FILE_MODIFIED = "file_modified"  # 파일 수정
    PROJECT_STATUS = "project_status"  # 프로젝트 상태 변경
    COMMENT_ADDED = "comment_added"  # 댓글 추가
    MENTION = "mention"  # 멘션

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    
    # 관련 엔티티 ID (선택적)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    
    # 관계 설정
    user = relationship("User", back_populates="notifications")
    project = relationship("Project", back_populates="notifications")
    task = relationship("Task", back_populates="notifications")
    file = relationship("File", back_populates="notifications")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Notification {self.type} for user {self.user_id}>" 