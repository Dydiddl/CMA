"""
API 요청/응답 스키마 정의
이 파일은 Pydantic을 사용하여 API의 요청과 응답 데이터의 구조를 정의합니다.
각 클래스는 특정 API 엔드포인트에서 사용되는 데이터의 유효성 검사와 직렬화를 담당합니다.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# 사용자 관련 스키마
class UserBase(BaseModel):
    """
    사용자 기본 정보 스키마
    이메일과 사용자 이름을 포함합니다.
    """
    email: EmailStr  # 이메일 주소 (이메일 형식 검증)
    username: str    # 사용자 이름

class UserCreate(UserBase):
    """
    사용자 생성 요청 스키마
    기본 정보에 비밀번호를 추가합니다.
    """
    password: str    # 비밀번호

class User(UserBase):
    """
    사용자 정보 응답 스키마
    데이터베이스에서 조회된 사용자 정보를 반환할 때 사용됩니다.
    """
    id: int          # 사용자 ID
    is_active: bool  # 계정 활성화 상태
    role: str        # 사용자 역할
    created_at: datetime  # 계정 생성 일시
    updated_at: datetime  # 정보 수정 일시

    class Config:
        orm_mode = True  # ORM 모델과의 호환성을 위한 설정

# 프로젝트 관련 스키마
class ProjectBase(BaseModel):
    """
    프로젝트 기본 정보 스키마
    프로젝트의 필수 정보를 포함합니다.
    """
    name: str        # 프로젝트명
    description: str # 프로젝트 설명
    status: str      # 프로젝트 상태
    start_date: datetime  # 시작일
    end_date: datetime    # 종료일

class ProjectCreate(ProjectBase):
    """
    프로젝트 생성 요청 스키마
    기본 정보를 그대로 사용합니다.
    """
    pass

class ProjectUpdate(BaseModel):
    """
    프로젝트 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    name: Optional[str] = None        # 프로젝트명
    description: Optional[str] = None  # 프로젝트 설명
    status: Optional[str] = None      # 프로젝트 상태
    start_date: Optional[datetime] = None  # 시작일
    end_date: Optional[datetime] = None    # 종료일

class Project(ProjectBase):
    """
    프로젝트 정보 응답 스키마
    데이터베이스에서 조회된 프로젝트 정보를 반환할 때 사용됩니다.
    """
    id: int          # 프로젝트 ID
    owner_id: int    # 소유자 ID
    created_at: datetime  # 생성 일시
    updated_at: datetime  # 수정 일시

    class Config:
        orm_mode = True  # ORM 모델과의 호환성을 위한 설정

# 태스크 관련 스키마
class TaskBase(BaseModel):
    """
    태스크 기본 정보 스키마
    태스크의 필수 정보를 포함합니다.
    """
    name: str        # 태스크명
    description: str # 태스크 설명
    status: str      # 태스크 상태
    progress: float  # 진행률
    start_date: datetime  # 시작일
    end_date: datetime    # 종료일
    project_id: int  # 소속 프로젝트 ID

class TaskCreate(TaskBase):
    """
    태스크 생성 요청 스키마
    기본 정보를 그대로 사용합니다.
    """
    pass

class TaskUpdate(BaseModel):
    """
    태스크 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    name: Optional[str] = None        # 태스크명
    description: Optional[str] = None  # 태스크 설명
    status: Optional[str] = None      # 태스크 상태
    progress: Optional[float] = None  # 진행률
    start_date: Optional[datetime] = None  # 시작일
    end_date: Optional[datetime] = None    # 종료일

class Task(TaskBase):
    """
    태스크 정보 응답 스키마
    데이터베이스에서 조회된 태스크 정보를 반환할 때 사용됩니다.
    """
    id: int          # 태스크 ID
    created_at: datetime  # 생성 일시
    updated_at: datetime  # 수정 일시

    class Config:
        orm_mode = True  # ORM 모델과의 호환성을 위한 설정 