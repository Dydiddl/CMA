from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date

class FinancialDocumentBase(BaseModel):
    document_type: str = Field(..., description="문서 유형 (영수증, 세금계산서, 지출증빙 등)")
    file_name: str = Field(..., description="파일명")
    description: Optional[str] = Field(None, description="문서 설명")

class FinancialDocumentCreate(FinancialDocumentBase):
    pass

class FinancialDocument(FinancialDocumentBase):
    id: int
    financial_record_id: int
    file_path: str
    upload_date: datetime

    class Config:
        from_attributes = True

class FinancialRecordBase(BaseModel):
    contract_id: int = Field(..., description="계약 ID")
    transaction_date: date = Field(..., description="거래일")
    amount: float = Field(..., description="금액")
    type: str = Field(..., description="거래 유형 (수입/지출)")
    category: str = Field(..., description="카테고리 (자재비, 노무비, 경비 등)")
    description: Optional[str] = Field(None, description="거래 설명")
    payment_method: str = Field(..., description="결제 방법")
    status: str = Field(..., description="지급 상태")
    vendor_id: Optional[int] = Field(None, description="거래처 ID")

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('금액은 0보다 커야 합니다')
        return v

class FinancialRecordCreate(FinancialRecordBase):
    pass

class FinancialRecordUpdate(BaseModel):
    contract_id: Optional[int] = None
    transaction_date: Optional[date] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    vendor_id: Optional[int] = None

class FinancialRecord(FinancialRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    documents: List[FinancialDocument] = []

    class Config:
        from_attributes = True 