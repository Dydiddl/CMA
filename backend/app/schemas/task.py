from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority

# 공유 속성
class TaskBase(BaseModel):
    title: str = Field(..., description="작업 제목")
    description: Optional[str] = Field(None, description="작업 설명")
    status: TaskStatus = Field(TaskStatus.TODO, description="작업 상태")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="작업 우선순위")
    due_date: Optional[datetime] = Field(None, description="마감일")
    is_completed: bool = Field(False, description="완료 여부")

# 생성 시 필요한 속성
class TaskCreate(TaskBase):
    project_id: int = Field(..., description="프로젝트 ID")
    assignee_id: Optional[int] = Field(None, description="담당자 ID")

# 업데이트 시 필요한 속성
class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    is_completed: Optional[bool] = None
    assignee_id: Optional[int] = None

# API 응답에 포함되는 속성
class Task(TaskBase):
    id: int
    project_id: int
    creator_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 