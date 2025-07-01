from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date

class WorkLogBase(BaseModel):
    work_date: date = Field(..., description="작업일")
    start_time: datetime = Field(..., description="시작시간")
    end_time: datetime = Field(..., description="종료시간")
    work_hours: float = Field(..., gt=0, description="작업시간")
    daily_wage: float = Field(..., gt=0, description="일당")
    description: Optional[str] = Field(None, description="작업내용")
    status: str = Field(..., description="지급상태")

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('종료시간은 시작시간보다 이후여야 합니다')
        return v

    @validator('work_hours')
    def validate_work_hours(cls, v, values):
        if 'start_time' in values and 'end_time' in values:
            time_diff = values['end_time'] - values['start_time']
            calculated_hours = time_diff.total_seconds() / 3600
            if abs(v - calculated_hours) > 0.1:  # 6분 이상 차이나면 경고
                raise ValueError('작업시간이 시작/종료시간과 일치하지 않습니다')
        return v

class WorkLogCreate(WorkLogBase):
    labor_id: int = Field(..., description="근로자 ID")

class WorkLogUpdate(BaseModel):
    work_date: Optional[date] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    work_hours: Optional[float] = None
    daily_wage: Optional[float] = None
    description: Optional[str] = None
    status: Optional[str] = None

class WorkLog(WorkLogBase):
    id: int
    labor_id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LaborBase(BaseModel):
    name: str = Field(..., description="이름")
    phone: str = Field(..., description="연락처")
    id_number: str = Field(..., description="주민번호/외국인등록번호")
    bank_name: str = Field(..., description="은행명")
    bank_account: str = Field(..., description="계좌번호")
    daily_wage: float = Field(..., gt=0, description="일당")
    status: str = Field(..., description="재직상태")
    contract_id: int = Field(..., description="계약 ID")

class LaborCreate(LaborBase):
    pass

class LaborUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    daily_wage: Optional[float] = None
    status: Optional[str] = None
    contract_id: Optional[int] = None

class Labor(LaborBase):
    id: int
    created_at: datetime
    updated_at: datetime
    work_logs: List[WorkLog] = []

    class Config:
        from_attributes = True

class LaborResponse(LaborBase):
    """근로자 응답 스키마"""
    id: int = Field(..., description="근로자 ID")
    created_at: datetime = Field(..., description="생성일")
    updated_at: datetime = Field(..., description="수정일")
    work_logs: List[WorkLog] = Field(default=[], description="작업일지 목록")
    
    class Config:
        from_attributes = True

class LaborListResponse(BaseModel):
    """근로자 목록 응답 스키마"""
    status: str = Field(default="success", description="응답 상태")
    data: List[LaborResponse] = Field(..., description="근로자 목록")
    total: int = Field(..., description="전체 근로자 수")
    page: int = Field(..., description="현재 페이지")
    size: int = Field(..., description="페이지 크기")
    message: Optional[str] = Field(None, description="응답 메시지")
    
    class Config:
        from_attributes = True 