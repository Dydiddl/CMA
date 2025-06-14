from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.labor import WorkerType, WorkerStatus

# Worker 스키마
class WorkerBase(BaseModel):
    name: str
    worker_type: WorkerType
    status: WorkerStatus = WorkerStatus.ACTIVE
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    hire_date: datetime
    resignation_date: Optional[datetime] = None
    hourly_rate: Optional[float] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    bank_holder: Optional[str] = None
    notes: Optional[str] = None

class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    worker_type: Optional[WorkerType] = None
    status: Optional[WorkerStatus] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    resignation_date: Optional[datetime] = None
    hourly_rate: Optional[float] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    bank_holder: Optional[str] = None
    notes: Optional[str] = None

class Worker(WorkerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# AttendanceRecord 스키마
class AttendanceRecordBase(BaseModel):
    date: datetime
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    work_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    worker_id: int

class AttendanceRecordUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    work_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AttendanceRecord(AttendanceRecordBase):
    id: int
    worker_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# SafetyTraining 스키마
class SafetyTrainingBase(BaseModel):
    training_date: datetime
    training_type: str
    trainer: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[float] = None
    score: Optional[float] = None
    passed: Optional[bool] = None
    notes: Optional[str] = None

class SafetyTrainingCreate(SafetyTrainingBase):
    worker_id: int

class SafetyTrainingUpdate(BaseModel):
    training_date: Optional[datetime] = None
    training_type: Optional[str] = None
    trainer: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[float] = None
    score: Optional[float] = None
    passed: Optional[bool] = None
    notes: Optional[str] = None

class SafetyTraining(SafetyTrainingBase):
    id: int
    worker_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Certification 스키마
class CertificationBase(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: datetime
    expiry_date: Optional[datetime] = None
    certificate_number: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class CertificationCreate(CertificationBase):
    worker_id: int

class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    certificate_number: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Certification(CertificationBase):
    id: int
    worker_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# PayrollRecord 스키마
class PayrollRecordBase(BaseModel):
    payment_date: datetime
    period_start: datetime
    period_end: datetime
    regular_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    regular_pay: Optional[float] = None
    overtime_pay: Optional[float] = None
    deductions: Optional[float] = None
    net_pay: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class PayrollRecordCreate(PayrollRecordBase):
    worker_id: int

class PayrollRecordUpdate(BaseModel):
    payment_date: Optional[datetime] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    regular_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    regular_pay: Optional[float] = None
    overtime_pay: Optional[float] = None
    deductions: Optional[float] = None
    net_pay: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class PayrollRecord(PayrollRecordBase):
    id: int
    worker_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 필터 스키마
class WorkerFilter(BaseModel):
    name: Optional[str] = None
    worker_type: Optional[WorkerType] = None
    status: Optional[WorkerStatus] = None
    hire_date_from: Optional[datetime] = None
    hire_date_to: Optional[datetime] = None

class AttendanceFilter(BaseModel):
    worker_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    status: Optional[str] = None

class SafetyTrainingFilter(BaseModel):
    worker_id: Optional[int] = None
    training_date_from: Optional[datetime] = None
    training_date_to: Optional[datetime] = None
    training_type: Optional[str] = None
    passed: Optional[bool] = None

class CertificationFilter(BaseModel):
    worker_id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    expiry_date_from: Optional[datetime] = None
    expiry_date_to: Optional[datetime] = None

class PayrollFilter(BaseModel):
    worker_id: Optional[int] = None
    payment_date_from: Optional[datetime] = None
    payment_date_to: Optional[datetime] = None
    status: Optional[str] = None 