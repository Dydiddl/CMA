from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NotificationBase(BaseModel):
    """
    알림 기본 정보 스키마
    알림의 필수 정보를 포함합니다.
    """
    title: str       # 알림 제목
    message: str     # 알림 내용
    type: str        # 알림 유형
    user_id: int     # 수신자 ID

class NotificationCreate(NotificationBase):
    """
    알림 생성 요청 스키마
    기본 정보를 그대로 사용합니다.
    """
    pass

class NotificationUpdate(BaseModel):
    """
    알림 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    title: Optional[str] = None    # 알림 제목
    message: Optional[str] = None  # 알림 내용
    type: Optional[str] = None     # 알림 유형
    is_read: Optional[bool] = None # 읽음 여부

class Notification(NotificationBase):
    """
    알림 정보 응답 스키마
    데이터베이스에서 조회된 알림 정보를 반환할 때 사용됩니다.
    """
    id: int          # 알림 ID
    is_read: bool    # 읽음 여부
    created_at: datetime  # 생성 일시
    updated_at: datetime  # 수정 일시

    class Config:
        from_attributes = True  # ORM 모델과의 호환성을 위한 설정

class NotificationTemplateBase(BaseModel):
    """
    알림 템플릿 기본 정보 스키마
    템플릿의 필수 정보를 포함합니다.
    """
    name: str        # 템플릿 이름
    content: str     # 템플릿 내용
    category: str    # 템플릿 카테고리
    version: str     # 템플릿 버전

class NotificationTemplateCreate(NotificationTemplateBase):
    """
    알림 템플릿 생성 요청 스키마
    기본 정보를 그대로 사용합니다.
    """
    pass

class NotificationTemplateUpdate(BaseModel):
    """
    알림 템플릿 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    name: Optional[str] = None     # 템플릿 이름
    content: Optional[str] = None  # 템플릿 내용
    category: Optional[str] = None # 템플릿 카테고리
    version: Optional[str] = None  # 템플릿 버전

class NotificationTemplate(NotificationTemplateBase):
    """
    알림 템플릿 정보 응답 스키마
    데이터베이스에서 조회된 템플릿 정보를 반환할 때 사용됩니다.
    """
    id: int          # 템플릿 ID
    created_at: datetime  # 생성 일시
    updated_at: datetime  # 수정 일시

    class Config:
        from_attributes = True  # ORM 모델과의 호환성을 위한 설정

class NotificationStats(BaseModel):
    """
    알림 통계 정보 스키마
    알림 관련 통계 정보를 포함합니다.
    """
    total_notifications: int       # 전체 알림 수
    unread_notifications: int      # 읽지 않은 알림 수
    notifications_by_type: dict    # 유형별 알림 수
    notifications_by_category: dict # 카테고리별 알림 수

    class Config:
        from_attributes = True  # ORM 모델과의 호환성을 위한 설정 