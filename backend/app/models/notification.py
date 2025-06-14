from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Enum, Boolean, Date, JSON
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
    """
    알림 정보를 저장하는 테이블
    사용자에게 전달되는 알림을 관리합니다.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    type = Column(String)  # 'info', 'warning', 'error', 'success'
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=0)  # 0: 낮음, 1: 보통, 2: 높음
    group = Column(String, nullable=True)  # 알림 그룹 (예: 'project', 'task', 'system')
    category = Column(String, nullable=True)  # 알림 카테고리 (예: 'update', 'alert', 'reminder')
    expires_at = Column(DateTime, nullable=True)  # 알림 만료 시간
    metadata = Column(JSON, nullable=True)  # 추가 메타데이터 (예: 관련 리소스 ID)
    
    user = relationship("User", back_populates="notifications")

class NotificationTemplate(Base):
    """
    알림 템플릿을 저장하는 테이블
    재사용 가능한 알림 템플릿을 관리합니다.
    """
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    title_template = Column(String)
    message_template = Column(String)
    type = Column(String)  # 'info', 'warning', 'error', 'success'
    group = Column(String)
    category = Column(String)
    priority = Column(Integer, default=0)
    variables = Column(JSON)  # 템플릿에서 사용할 변수 목록
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    versions = relationship("NotificationTemplateVersion", back_populates="template")

class NotificationTemplateCategory(Base):
    """
    알림 템플릿 카테고리를 저장하는 테이블
    알림 템플릿의 계층적 분류를 관리합니다.
    """
    __tablename__ = "notification_template_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("notification_template_categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent = relationship("NotificationTemplateCategory", remote_side=[id], backref="subcategories")

class NotificationTemplateVersion(Base):
    """
    알림 템플릿 버전을 저장하는 테이블
    알림 템플릿의 버전 관리를 담당합니다.
    """
    __tablename__ = "notification_template_versions"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("notification_templates.id"))
    version = Column(String)  # 예: "1.0.0"
    title_template = Column(String)
    message_template = Column(String)
    type = Column(String)
    group = Column(String)
    category = Column(String)
    priority = Column(Integer, default=0)
    variables = Column(JSON)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    change_log = Column(String, nullable=True)

    template = relationship("NotificationTemplate", back_populates="versions")
    creator = relationship("User")

class NotificationStats(Base):
    """
    알림 통계를 저장하는 테이블
    사용자별 알림 통계를 관리합니다.
    """
    __tablename__ = "notification_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, index=True)
    total_count = Column(Integer, default=0)
    read_count = Column(Integer, default=0)
    unread_count = Column(Integer, default=0)
    by_type = Column(JSON)  # 타입별 통계
    by_priority = Column(JSON)  # 우선순위별 통계
    by_group = Column(JSON)  # 그룹별 통계
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notification_stats")

class NotificationCleanupSchedule(Base):
    """
    알림 정리 일정을 저장하는 테이블
    오래된 알림의 자동 정리 일정을 관리합니다.
    """
    __tablename__ = "notification_cleanup_schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    days_to_keep = Column(Integer)
    keep_unread = Column(Boolean, default=True)
    keep_high_priority = Column(Boolean, default=True)
    schedule_type = Column(String)  # 'daily', 'weekly', 'monthly'
    schedule_time = Column(String)  # cron 표현식 또는 시간
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NotificationReport(Base):
    """
    알림 리포트를 저장하는 테이블
    사용자별 알림 리포트를 관리합니다.
    """
    __tablename__ = "notification_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String)  # 'daily', 'weekly', 'monthly', 'custom'
    start_date = Column(Date)
    end_date = Column(Date)
    report_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=True)  # 생성된 리포트 파일 경로

    user = relationship("User")

    def __repr__(self):
        return f"<Notification {self.type} for user {self.user_id}>" 