from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.construction import ConstructionStatus, ConstructionType

class ConstructionBase(BaseModel):
    name: str = Field(..., description="공사명")
    construction_number: str = Field(..., description="공사번호")
    description: Optional[str] = Field(None, description="공사 설명")
    type: ConstructionType = Field(..., description="공사 유형")
    status: ConstructionStatus = Field(default=ConstructionStatus.PLANNING, description="공사 상태")
    location: str = Field(..., description="공사 위치")
    area: Optional[float] = Field(None, description="공사 면적(㎡)")
    
    # 계약 정보
    contract_number: Optional[str] = Field(None, description="계약번호")
    contract_date: Optional[datetime] = Field(None, description="계약일")
    contract_amount: Optional[float] = Field(None, description="계약금액")
    contract_period: Optional[int] = Field(None, description="계약기간(일)")
    
    # 일정 정보
    start_date: Optional[datetime] = Field(None, description="착공일")
    planned_end_date: Optional[datetime] = Field(None, description="예정 완료일")
    actual_end_date: Optional[datetime] = Field(None, description="실제 완료일")
    
    # 비용 정보
    estimated_cost: Optional[float] = Field(None, description="예상 비용")
    actual_cost: Optional[float] = Field(None, description="실제 비용")
    payment_status: Optional[str] = Field(None, description="지급 상태")

class ConstructionCreate(ConstructionBase):
    client_id: int = Field(..., description="발주자 ID")
    contractor_id: Optional[int] = Field(None, description="수급자 ID")
    supervisor_id: Optional[int] = Field(None, description="감리자 ID")

class ConstructionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="공사명")
    description: Optional[str] = Field(None, description="공사 설명")
    type: Optional[ConstructionType] = Field(None, description="공사 유형")
    status: Optional[ConstructionStatus] = Field(None, description="공사 상태")
    location: Optional[str] = Field(None, description="공사 위치")
    area: Optional[float] = Field(None, description="공사 면적(㎡)")
    contract_number: Optional[str] = Field(None, description="계약번호")
    contract_date: Optional[datetime] = Field(None, description="계약일")
    contract_amount: Optional[float] = Field(None, description="계약금액")
    contract_period: Optional[int] = Field(None, description="계약기간(일)")
    start_date: Optional[datetime] = Field(None, description="착공일")
    planned_end_date: Optional[datetime] = Field(None, description="예정 완료일")
    actual_end_date: Optional[datetime] = Field(None, description="실제 완료일")
    estimated_cost: Optional[float] = Field(None, description="예상 비용")
    actual_cost: Optional[float] = Field(None, description="실제 비용")
    payment_status: Optional[str] = Field(None, description="지급 상태")
    contractor_id: Optional[int] = Field(None, description="수급자 ID")
    supervisor_id: Optional[int] = Field(None, description="감리자 ID")

class ConstructionInDB(ConstructionBase):
    id: int
    client_id: int
    contractor_id: Optional[int]
    supervisor_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ConstructionFilter(BaseModel):
    name: Optional[str] = None
    construction_number: Optional[str] = None
    type: Optional[ConstructionType] = None
    status: Optional[ConstructionStatus] = None
    location: Optional[str] = None
    client_id: Optional[int] = None
    contractor_id: Optional[int] = None
    supervisor_id: Optional[int] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    planned_end_date_from: Optional[datetime] = None
    planned_end_date_to: Optional[datetime] = None
    contract_amount_min: Optional[float] = None
    contract_amount_max: Optional[float] = None 