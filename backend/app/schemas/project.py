#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프로젝트 스키마 - API 요청/응답 모델
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    """프로젝트 상태 열거형"""
    PLANNING = "planning"  # 기획
    PREPARATION = "preparation"  # 준비
    IN_PROGRESS = "in_progress"  # 진행중
    COMPLETED = "completed"  # 완료
    ON_HOLD = "on_hold"  # 일시중단
    CANCELLED = "cancelled"  # 취소

class ProjectType(str, Enum):
    """프로젝트 유형 열거형"""
    RESIDENTIAL = "residential"  # 주거
    COMMERCIAL = "commercial"  # 상업
    INFRASTRUCTURE = "infrastructure"  # 인프라
    INDUSTRIAL = "industrial"  # 산업
    MIXED_USE = "mixed_use"  # 복합용도
    OTHER = "other"  # 기타

class ProjectBase(BaseModel):
    """프로젝트 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=255, description="프로젝트명")
    project_number: str = Field(..., min_length=1, max_length=50, description="프로젝트 번호")
    description: Optional[str] = Field(None, description="프로젝트 설명")
    project_type: ProjectType = Field(default=ProjectType.OTHER, description="프로젝트 유형")
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING, description="프로젝트 상태")
    location: Optional[str] = Field(None, max_length=500, description="프로젝트 위치")
    address: Optional[str] = Field(None, max_length=500, description="상세 주소")
    start_date: Optional[datetime] = Field(None, description="시작일")
    end_date: Optional[datetime] = Field(None, description="종료일")
    planned_start_date: Optional[datetime] = Field(None, description="계획 시작일")
    planned_end_date: Optional[datetime] = Field(None, description="계획 종료일")
    total_budget: Optional[float] = Field(None, ge=0, description="총 예산")
    current_cost: Optional[float] = Field(None, ge=0, description="현재 비용")
    project_manager: Optional[str] = Field(None, max_length=100, description="프로젝트 매니저")
    client_name: Optional[str] = Field(None, max_length=255, description="발주처명")
    client_contact: Optional[str] = Field(None, max_length=100, description="발주처 연락처")
    building_area: Optional[float] = Field(None, ge=0, description="건축면적 (㎡)")
    floor_area: Optional[float] = Field(None, ge=0, description="연면적 (㎡)")
    floors: Optional[int] = Field(None, ge=0, description="층수")
    vendor_id: Optional[str] = Field(None, description="거래처 ID")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('종료일은 시작일보다 늦어야 합니다.')
        return v
    
    @validator('planned_end_date')
    def validate_planned_end_date(cls, v, values):
        if v and 'planned_start_date' in values and values['planned_start_date']:
            if v <= values['planned_start_date']:
                raise ValueError('계획 종료일은 계획 시작일보다 늦어야 합니다.')
        return v

class ProjectCreate(ProjectBase):
    """프로젝트 생성 스키마"""
    pass

class ProjectUpdate(BaseModel):
    """프로젝트 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    project_number: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    status: Optional[ProjectStatus] = None
    location: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = Field(None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    total_budget: Optional[float] = Field(None, ge=0)
    current_cost: Optional[float] = Field(None, ge=0)
    project_manager: Optional[str] = Field(None, max_length=100)
    client_name: Optional[str] = Field(None, max_length=255)
    client_contact: Optional[str] = Field(None, max_length=100)
    building_area: Optional[float] = Field(None, ge=0)
    floor_area: Optional[float] = Field(None, ge=0)
    floors: Optional[int] = Field(None, ge=0)
    vendor_id: Optional[str] = None

class ProjectResponse(ProjectBase):
    """프로젝트 응답 스키마"""
    id: str
    remaining_budget: Optional[float] = None
    progress_percentage: Optional[float] = None
    budget_usage_percentage: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    """프로젝트 목록 응답 스키마"""
    status: str = "success"
    data: List[ProjectResponse]
    total: int
    page: int
    size: int
    message: Optional[str] = None

class ProjectDocumentBase(BaseModel):
    """프로젝트 문서 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=255, description="문서 제목")
    file_name: str = Field(..., min_length=1, max_length=255, description="파일명")
    file_path: str = Field(..., min_length=1, max_length=500, description="파일 경로")
    file_size: Optional[int] = Field(None, ge=0, description="파일 크기 (bytes)")
    file_type: Optional[str] = Field(None, max_length=50, description="파일 유형")
    document_type: Optional[str] = Field(None, max_length=100, description="문서 유형")
    category: Optional[str] = Field(None, max_length=100, description="문서 카테고리")
    description: Optional[str] = Field(None, description="문서 설명")
    tags: Optional[str] = Field(None, max_length=500, description="태그 (쉼표로 구분)")
    version: Optional[str] = Field(None, max_length=20, description="문서 버전")

class ProjectDocumentCreate(ProjectDocumentBase):
    """프로젝트 문서 생성 스키마"""
    project_id: str = Field(..., description="프로젝트 ID")

class ProjectDocumentUpdate(BaseModel):
    """프로젝트 문서 수정 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    file_name: Optional[str] = Field(None, min_length=1, max_length=255)
    file_path: Optional[str] = Field(None, min_length=1, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    file_type: Optional[str] = Field(None, max_length=50)
    document_type: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    tags: Optional[str] = Field(None, max_length=500)
    version: Optional[str] = Field(None, max_length=20)

class ProjectDocumentResponse(ProjectDocumentBase):
    """프로젝트 문서 응답 스키마"""
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectDocumentListResponse(BaseModel):
    """프로젝트 문서 목록 응답 스키마"""
    status: str = "success"
    data: List[ProjectDocumentResponse]
    total: int
    page: int
    size: int
    message: Optional[str] = None

class ProjectStatistics(BaseModel):
    """프로젝트 통계 스키마"""
    total_projects: int
    active_projects: int
    completed_projects: int
    total_budget: float
    total_spent: float
    average_progress: float
    projects_by_status: dict
    projects_by_type: dict
    
    class Config:
        from_attributes = True 