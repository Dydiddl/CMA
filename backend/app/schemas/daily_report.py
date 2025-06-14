from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.daily_report import WeatherCondition, WorkStatus

# 기본 스키마
class DailyReportBase(BaseModel):
    project_id: int
    report_date: datetime
    weather_condition: WeatherCondition
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    work_status: WorkStatus
    work_description: str
    work_progress: Optional[float] = None
    issues: Optional[str] = None
    solutions: Optional[str] = None
    next_day_plan: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 생성 스키마
class DailyReportCreate(DailyReportBase):
    pass

# 업데이트 스키마
class DailyReportUpdate(BaseModel):
    weather_condition: Optional[WeatherCondition] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    work_status: Optional[WorkStatus] = None
    work_description: Optional[str] = None
    work_progress: Optional[float] = None
    issues: Optional[str] = None
    solutions: Optional[str] = None
    next_day_plan: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# 작업 항목 스키마
class WorkEntryBase(BaseModel):
    work_type: str
    description: str
    start_time: datetime
    end_time: datetime
    worker_count: int
    equipment_used: Optional[str] = None
    materials_used: Optional[str] = None
    progress: Optional[float] = None
    notes: Optional[str] = None

class WorkEntryCreate(WorkEntryBase):
    pass

class WorkEntryUpdate(BaseModel):
    work_type: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    worker_count: Optional[int] = None
    equipment_used: Optional[str] = None
    materials_used: Optional[str] = None
    progress: Optional[float] = None
    notes: Optional[str] = None

class WorkEntry(WorkEntryBase):
    id: int
    daily_report_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 안전 점검 스키마
class SafetyCheckBase(BaseModel):
    check_type: str
    check_item: str
    status: bool
    issue: Optional[str] = None
    action_taken: Optional[str] = None
    checked_at: datetime

class SafetyCheckCreate(SafetyCheckBase):
    pass

class SafetyCheckUpdate(BaseModel):
    check_type: Optional[str] = None
    check_item: Optional[str] = None
    status: Optional[bool] = None
    issue: Optional[str] = None
    action_taken: Optional[str] = None
    checked_at: Optional[datetime] = None

class SafetyCheck(SafetyCheckBase):
    id: int
    daily_report_id: int
    checked_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 품질 점검 스키마
class QualityCheckBase(BaseModel):
    check_type: str
    check_item: str
    standard: str
    result: str
    status: bool
    issue: Optional[str] = None
    action_taken: Optional[str] = None
    checked_at: datetime

class QualityCheckCreate(QualityCheckBase):
    pass

class QualityCheckUpdate(BaseModel):
    check_type: Optional[str] = None
    check_item: Optional[str] = None
    standard: Optional[str] = None
    result: Optional[str] = None
    status: Optional[bool] = None
    issue: Optional[str] = None
    action_taken: Optional[str] = None
    checked_at: Optional[datetime] = None

class QualityCheck(QualityCheckBase):
    id: int
    daily_report_id: int
    checked_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 첨부파일 스키마
class DailyReportAttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    description: Optional[str] = None

class DailyReportAttachmentCreate(DailyReportAttachmentBase):
    pass

class DailyReportAttachment(DailyReportAttachmentBase):
    id: int
    daily_report_id: int
    uploaded_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# 일일 작업 일지 응답 스키마
class DailyReport(DailyReportBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    work_entries: List[WorkEntry] = []
    safety_checks: List[SafetyCheck] = []
    quality_checks: List[QualityCheck] = []
    attachments: List[DailyReportAttachment] = []

    class Config:
        orm_mode = True

# 필터 스키마
class DailyReportFilter(BaseModel):
    project_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    weather_condition: Optional[WeatherCondition] = None
    work_status: Optional[WorkStatus] = None
    created_by: Optional[int] = None
    skip: int = 0
    limit: int = 100

# 통계 스키마
class DailyReportStatistics(BaseModel):
    total_reports: int
    total_work_entries: int
    total_safety_checks: int
    total_quality_checks: int
    work_status_distribution: Dict[str, int]
    weather_distribution: Dict[str, int]
    average_progress: float
    safety_check_pass_rate: float
    quality_check_pass_rate: float
    monthly_trend: Dict[str, int] 