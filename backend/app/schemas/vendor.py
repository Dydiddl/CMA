from app.schemas.common_types import *
from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional, Dict
from datetime import datetime

# Vendor Base Schema
class VendorBase(BaseModel):
    company_name: str
    business_number: str
    representative_name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    bank_info: Optional[Dict] = None
    documents: Optional[Dict] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    company_name: Optional[str] = None
    business_number: Optional[str] = None
    representative_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    bank_info: Optional[Dict] = None
    documents: Optional[Dict] = None

class Vendor(VendorBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# VendorHistory Schema
class VendorHistoryBase(BaseModel):
    action_type: str
    previous_data: Optional[Dict] = None
    new_data: Optional[Dict] = None
    changed_by: UUID4

class VendorHistoryCreate(VendorHistoryBase):
    vendor_id: UUID4

class VendorHistory(VendorHistoryBase):
    id: UUID4
    vendor_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True 