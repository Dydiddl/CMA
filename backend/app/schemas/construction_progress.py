from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.construction_progress import ProgressStatus

class ConstructionPhotoBase(BaseModel):
    photo_url: str = Field(..., description="사진 URL")
    description: Optional[str] = Field(None, description="사진 설명")
    taken_at: datetime = Field(default_factory=datetime.utcnow, description="촬영 시간")

class ConstructionPhotoCreate(ConstructionPhotoBase):
    pass

class ConstructionPhotoUpdate(BaseModel):
    description: Optional[str] = None

class ConstructionPhoto(ConstructionPhotoBase):
    id: int
    progress_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SafetyCheckBase(BaseModel):
    check_type: str = Field(..., description="점검 종류")
    check_result: str = Field(..., description="점검 결과")
    issues: Optional[str] = Field(None, description="발견된 문제점")
    actions: Optional[str] = Field(None, description="조치사항")
    checker: str = Field(..., description="점검자")

class SafetyCheckCreate(SafetyCheckBase):
    pass

class SafetyCheckUpdate(BaseModel):
    check_type: Optional[str] = None
    check_result: Optional[str] = None
    issues: Optional[str] = None
    actions: Optional[str] = None
    checker: Optional[str] = None

class SafetyCheck(SafetyCheckBase):
    id: int
    progress_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class QualityCheckBase(BaseModel):
    check_type: str = Field(..., description="점검 종류")
    check_result: str = Field(..., description="점검 결과")
    issues: Optional[str] = Field(None, description="발견된 문제점")
    actions: Optional[str] = Field(None, description="조치사항")
    checker: str = Field(..., description="점검자")

class QualityCheckCreate(QualityCheckBase):
    pass

class QualityCheckUpdate(BaseModel):
    check_type: Optional[str] = None
    check_result: Optional[str] = None
    issues: Optional[str] = None
    actions: Optional[str] = None
    checker: Optional[str] = None

class QualityCheck(QualityCheckBase):
    id: int
    progress_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ConstructionProgressBase(BaseModel):
    date: datetime = Field(default_factory=datetime.utcnow, description="작업일")
    progress_percentage: float = Field(..., description="공정률")
    status: ProgressStatus = Field(default=ProgressStatus.ON_SCHEDULE, description="진행 상태")
    description: Optional[str] = Field(None, description="작업 내용")
    work_type: str = Field(..., description="작업 종류")
    work_area: Optional[str] = Field(None, description="작업 구역")
    worker_count: Optional[int] = Field(None, description="작업자 수")
    equipment_count: Optional[int] = Field(None, description="장비 수")
    weather: Optional[str] = Field(None, description="날씨")
    temperature: Optional[float] = Field(None, description="기온")
    humidity: Optional[float] = Field(None, description="습도")
    issues: Optional[str] = Field(None, description="특이사항")
    solutions: Optional[str] = Field(None, description="해결방안")

class ConstructionProgressCreate(ConstructionProgressBase):
    construction_id: int = Field(..., description="공사 ID")

class ConstructionProgressUpdate(BaseModel):
    date: Optional[datetime] = None
    progress_percentage: Optional[float] = None
    status: Optional[ProgressStatus] = None
    description: Optional[str] = None
    work_type: Optional[str] = None
    work_area: Optional[str] = None
    worker_count: Optional[int] = None
    equipment_count: Optional[int] = None
    weather: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    issues: Optional[str] = None
    solutions: Optional[str] = None

class ConstructionProgress(ConstructionProgressBase):
    id: int
    construction_id: int
    created_at: datetime
    updated_at: datetime
    photos: List[ConstructionPhoto] = []
    safety_checks: List[SafetyCheck] = []
    quality_checks: List[QualityCheck] = []

    class Config:
        orm_mode = True

class ConstructionProgressFilter(BaseModel):
    construction_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    status: Optional[ProgressStatus] = None
    work_type: Optional[str] = None
    work_area: Optional[str] = None
    progress_percentage_min: Optional[float] = None
    progress_percentage_max: Optional[float] = None 