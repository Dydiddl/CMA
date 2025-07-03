"""
계약 관련 Pydantic 스키마
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class ContractBase(BaseModel):
    """계약 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=255, description="계약명")
    contract_number: str = Field(..., min_length=1, max_length=50, description="계약번호")
    contract_amount: float = Field(..., gt=0, description="계약금액")
    contract_date: datetime = Field(..., description="계약일")
    start_date: Optional[datetime] = Field(None, description="시작일")
    end_date: Optional[datetime] = Field(None, description="종료일")
    client_name: str = Field(..., min_length=1, max_length=255, description="발주처명")
    client_contact: Optional[str] = Field(None, max_length=100, description="발주처 연락처")
    status: str = Field(default="진행중", description="계약 상태")
    description: Optional[str] = Field(None, description="계약 설명")
    vendor_id: str = Field(..., description="거래처 ID")
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        """종료일 검증"""
        if v and 'start_date' in info.data and info.data['start_date']:
            if v <= info.data['start_date']:
                raise ValueError('종료일은 시작일보다 늦어야 합니다.')
        return v


class ContractCreate(ContractBase):
    """계약 생성 스키마"""
    pass


class ContractUpdate(BaseModel):
    """계약 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    contract_number: Optional[str] = Field(None, min_length=1, max_length=50)
    contract_amount: Optional[float] = Field(None, gt=0)
    contract_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    client_name: Optional[str] = Field(None, min_length=1, max_length=255)
    client_contact: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None
    description: Optional[str] = None
    vendor_id: Optional[str] = None


class ContractResponse(ContractBase):
    """계약 응답 스키마"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class ContractDocumentBase(BaseModel):
    """계약 문서 기본 스키마"""
    document_type: str = Field(..., min_length=1, max_length=50, description="문서 유형")
    file_path: str = Field(..., min_length=1, max_length=500, description="파일 경로")
    file_name: str = Field(..., min_length=1, max_length=255, description="파일명")
    description: Optional[str] = Field(None, description="문서 설명")


class ContractDocumentCreate(ContractDocumentBase):
    """계약 문서 생성 스키마"""
    contract_id: str = Field(..., description="계약 ID")


class ContractDocumentResponse(ContractDocumentBase):
    """계약 문서 응답 스키마"""
    id: str
    contract_id: str
    upload_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContractListResponse(BaseModel):
    """계약 목록 응답 스키마"""
    status: str = "success"
    data: List[ContractResponse]
    total: int
    page: int
    size: int
    message: Optional[str] = None


class ContractDetailResponse(BaseModel):
    """계약 상세 응답 스키마"""
    status: str = "success"
    data: ContractResponse
    documents: List[ContractDocumentResponse]
    message: Optional[str] = None


class StandardResponse(BaseModel):
    """표준 응답 스키마"""
    status: str = "success"
    data: Optional[dict] = None
    message: Optional[str] = None 