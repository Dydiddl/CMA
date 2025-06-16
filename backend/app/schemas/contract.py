from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ContractDocumentBase(BaseModel):
    document_type: str = Field(..., description="문서 유형 (계약서, 견적서, 명세서 등)")
    file_name: str = Field(..., description="파일명")
    description: Optional[str] = Field(None, description="문서 설명")

class ContractDocumentCreate(ContractDocumentBase):
    pass

class ContractDocument(ContractDocumentBase):
    id: int
    contract_id: int
    file_path: str
    upload_date: datetime

    class Config:
        from_attributes = True

class ContractBase(BaseModel):
    name: str = Field(..., description="계약명")
    contract_number: str = Field(..., description="계약번호")
    contract_amount: float = Field(..., gt=0, description="계약금액")
    contract_date: datetime = Field(..., description="계약일")
    start_date: datetime = Field(..., description="시작일")
    end_date: datetime = Field(..., description="종료일")
    client_name: str = Field(..., description="발주처명")
    client_contact: str = Field(..., description="발주처 연락처")
    status: str = Field(..., description="계약 상태")
    description: Optional[str] = Field(None, description="계약 설명")
    vendor_id: int = Field(..., description="거래처 ID")

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('종료일은 시작일보다 이후여야 합니다')
        return v

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    name: Optional[str] = None
    contract_number: Optional[str] = None
    contract_amount: Optional[float] = None
    contract_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    client_name: Optional[str] = None
    client_contact: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    vendor_id: Optional[int] = None

class Contract(ContractBase):
    id: int
    created_at: datetime
    updated_at: datetime
    documents: List[ContractDocument] = []

    class Config:
        from_attributes = True 