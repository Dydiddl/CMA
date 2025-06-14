from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# 공유 속성
class ProjectBase(BaseModel):
    """
    프로젝트 기본 정보 스키마
    프로젝트의 필수 정보를 포함합니다.
    """
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
    """
    프로젝트 생성 요청 스키마
    기본 정보를 그대로 사용합니다.
    """
    pass

# 업데이트 시 필요한 속성
class ProjectUpdate(BaseModel):
    """
    프로젝트 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    name: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# API 응답에 포함되는 속성
class Project(ProjectBase):
    """
    프로젝트 정보 응답 스키마
    데이터베이스에서 조회된 프로젝트 정보를 반환할 때 사용됩니다.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 