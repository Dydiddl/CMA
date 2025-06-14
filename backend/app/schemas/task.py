from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority

# 공유 속성
class TaskBase(BaseModel):
    """
    작업 기본 정보 스키마
    작업의 필수 정보를 포함합니다.
    """
    name: str        # 작업명
    description: str # 작업 설명
    status: str      # 작업 상태
    progress: int    # 진행률
    start_date: datetime  # 시작일
    end_date: datetime    # 종료일
    project_id: int  # 프로젝트 ID
    assignee_id: int # 담당자 ID

# 생성 시 필요한 속성
class TaskCreate(TaskBase):
    """
    작업 생성 요청 스키마
    기본 정보를 그대로 사용합니다.
    """
    pass

# 업데이트 시 필요한 속성
class TaskUpdate(BaseModel):
    """
    작업 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    name: Optional[str] = None        # 작업명
    description: Optional[str] = None  # 작업 설명
    status: Optional[str] = None      # 작업 상태
    progress: Optional[int] = None    # 진행률
    start_date: Optional[datetime] = None  # 시작일
    end_date: Optional[datetime] = None    # 종료일
    assignee_id: Optional[int] = None # 담당자 ID

# API 응답에 포함되는 속성
class Task(TaskBase):
    """
    작업 정보 응답 스키마
    데이터베이스에서 조회된 작업 정보를 반환할 때 사용됩니다.
    """
    id: int          # 작업 ID
    created_at: datetime  # 생성 일시
    updated_at: datetime  # 수정 일시

    class Config:
        from_attributes = True  # ORM 모델과의 호환성을 위한 설정 