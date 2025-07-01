# ...existing code from schemas.py...

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskStatus(str):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'

class TaskPriority(str):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

class TaskBase(BaseModel):
    name: str = Field(..., description="작업명")
    description: Optional[str] = Field('', description="설명")
    status: str = Field('TODO', description="상태")
    progress: int = Field(0, ge=0, le=100, description="진행률(%)")
    start_date: Optional[datetime] = Field(None, description="시작일")
    end_date: Optional[datetime] = Field(None, description="종료일")
    project_id: int = Field(..., description="프로젝트 ID")
    assignee: Optional[str] = Field('', description="담당자")
    priority: str = Field('MEDIUM', description="우선순위")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_id: Optional[int] = None
    assignee: Optional[str] = None
    priority: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
