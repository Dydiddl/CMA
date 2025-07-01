from .contract import (
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    ContractListResponse,
    ContractDetailResponse,
    ContractDocumentCreate,
    ContractDocumentResponse,
    StandardResponse
)

# 임시 Project 스키마 (나중에 별도 파일로 분리)
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str = Field(..., description="프로젝트명")
    description: Optional[str] = Field(None, description="프로젝트 설명")
    status: str = Field(default="진행중", description="프로젝트 상태")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

from .labor import (
    Labor,
    LaborCreate,
    LaborUpdate,
    WorkLog,
    WorkLogCreate,
    WorkLogUpdate
)
from .financial import (
    FinancialRecord,
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialDocument,
    FinancialDocumentCreate
)
from .vendor import (
    Vendor,
    VendorCreate,
    VendorUpdate,
    VendorDocument,
    VendorDocumentCreate
)

__all__ = [
    "Contract",
    "ContractCreate",
    "ContractUpdate",
    "ContractDocument",
    "ContractDocumentCreate",
    "Labor",
    "LaborCreate",
    "LaborUpdate",
    "WorkLog",
    "WorkLogCreate",
    "WorkLogUpdate",
    "FinancialRecord",
    "FinancialRecordCreate",
    "FinancialRecordUpdate",
    "FinancialDocument",
    "FinancialDocumentCreate",
    "Vendor",
    "VendorCreate",
    "VendorUpdate",
    "VendorDocument",
    "VendorDocumentCreate"
] 