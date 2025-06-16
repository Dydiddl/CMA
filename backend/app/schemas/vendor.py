from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime

class VendorDocumentBase(BaseModel):
    document_type: str = Field(..., description="문서 유형 (사업자등록증, 통장사본 등)")
    file_name: str = Field(..., description="파일명")
    description: Optional[str] = Field(None, description="문서 설명")

class VendorDocumentCreate(VendorDocumentBase):
    pass

class VendorDocument(VendorDocumentBase):
    id: int
    vendor_id: int
    file_path: str
    upload_date: datetime

    class Config:
        from_attributes = True

class VendorBase(BaseModel):
    name: str = Field(..., description="거래처명")
    business_number: str = Field(..., description="사업자등록번호")
    representative: str = Field(..., description="대표자명")
    address: str = Field(..., description="주소")
    phone: str = Field(..., description="연락처")
    email: EmailStr = Field(..., description="이메일")
    bank_name: str = Field(..., description="은행명")
    bank_account: str = Field(..., description="계좌번호")
    status: str = Field(..., description="거래 상태")
    description: Optional[str] = Field(None, description="비고")

    @validator('business_number')
    def validate_business_number(cls, v):
        # 사업자등록번호 형식 검증 (10자리 숫자)
        if not v.isdigit() or len(v) != 10:
            raise ValueError('사업자등록번호는 10자리 숫자여야 합니다')
        return v

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: Optional[str] = None
    business_number: Optional[str] = None
    representative: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class Vendor(VendorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    documents: List[VendorDocument] = []

    class Config:
        from_attributes = True 