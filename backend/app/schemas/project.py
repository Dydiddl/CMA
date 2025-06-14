from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# 공유 속성
class ProjectBase(BaseModel):
    name: str = Field(..., description="프로젝트 이름")
    description: Optional[str] = Field(None, description="프로젝트 설명")
    status: str = Field(..., description="프로젝트 상태")
    is_active: bool = Field(True, description="프로젝트 활성화 여부")
    start_date: Optional[datetime] = Field(None, description="시작일")
    end_date: Optional[datetime] = Field(None, description="종료일")
    budget: Optional[float] = Field(None, description="예산")
    location: Optional[str] = Field(None, description="위치")

# 생성 시 필요한 속성
class ProjectCreate(ProjectBase):
    pass

# 업데이트 시 필요한 속성
class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

# API 응답에 포함되는 속성
class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 