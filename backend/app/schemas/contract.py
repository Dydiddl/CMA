from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.contract import ContractType, ContractStatus, PaymentStatus

# Contract 스키마
class ContractBase(BaseModel):
    contract_number: str
    contract_type: ContractType
    title: str
    description: Optional[str] = None
    client_name: str
    client_contact: Optional[str] = None
    client_address: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[EmailStr] = None
    start_date: datetime
    end_date: datetime
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    contract_amount: float
    currency: str = "KRW"
    payment_terms: Optional[str] = None
    payment_schedule: Optional[Dict[str, Any]] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None
    contract_file_url: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    terms_and_conditions: Optional[str] = None
    special_conditions: Optional[str] = None
    notes: Optional[str] = None

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    client_contact: Optional[str] = None
    client_address: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[EmailStr] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    contract_amount: Optional[float] = None
    payment_terms: Optional[str] = None
    payment_schedule: Optional[Dict[str, Any]] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None
    contract_file_url: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    terms_and_conditions: Optional[str] = None
    special_conditions: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[ContractStatus] = None

class Contract(ContractBase):
    id: int
    status: ContractStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ContractAmendment 스키마
class ContractAmendmentBase(BaseModel):
    amendment_number: str
    amendment_date: datetime
    reason: str
    changes: Dict[str, Any]
    notes: Optional[str] = None

class ContractAmendmentCreate(ContractAmendmentBase):
    contract_id: int

class ContractAmendmentUpdate(BaseModel):
    reason: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None
    status: Optional[ContractStatus] = None
    notes: Optional[str] = None

class ContractAmendment(ContractAmendmentBase):
    id: int
    contract_id: int
    status: ContractStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ContractPayment 스키마
class ContractPaymentBase(BaseModel):
    payment_number: str
    due_date: datetime
    amount: float
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    notes: Optional[str] = None

class ContractPaymentCreate(ContractPaymentBase):
    contract_id: int

class ContractPaymentUpdate(BaseModel):
    due_date: Optional[datetime] = None
    amount: Optional[float] = None
    status: Optional[PaymentStatus] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    notes: Optional[str] = None

class ContractPayment(ContractPaymentBase):
    id: int
    contract_id: int
    status: PaymentStatus
    payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 필터 스키마
class ContractFilter(BaseModel):
    contract_number: Optional[str] = None
    contract_type: Optional[ContractType] = None
    status: Optional[ContractStatus] = None
    client_name: Optional[str] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    end_date_from: Optional[datetime] = None
    end_date_to: Optional[datetime] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None

class ContractAmendmentFilter(BaseModel):
    contract_id: Optional[int] = None
    amendment_date_from: Optional[datetime] = None
    amendment_date_to: Optional[datetime] = None
    status: Optional[ContractStatus] = None
    approved_by: Optional[int] = None

class ContractPaymentFilter(BaseModel):
    contract_id: Optional[int] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    status: Optional[PaymentStatus] = None
    payment_date_from: Optional[datetime] = None
    payment_date_to: Optional[datetime] = None 