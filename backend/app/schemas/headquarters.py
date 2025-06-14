from app.schemas.common_types import *
from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional, Dict
from datetime import date, datetime

# Headquarters Base Schema
class HeadquartersBase(BaseModel):
    name: str
    business_number: str
    address: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    established_date: Optional[date] = None
    representative_name: Optional[str] = None
    description: Optional[str] = None

class HeadquartersCreate(HeadquartersBase):
    pass

class HeadquartersUpdate(BaseModel):
    name: Optional[str] = None
    business_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    established_date: Optional[date] = None
    representative_name: Optional[str] = None
    description: Optional[str] = None

class Headquarters(HeadquartersBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# HeadquartersDetail Schema
class HeadquartersDetailBase(BaseModel):
    industry: Optional[str] = None
    business_type: Optional[str] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    main_business: Optional[str] = None

class HeadquartersDetailCreate(HeadquartersDetailBase):
    headquarters_id: UUID4

class HeadquartersDetailUpdate(BaseModel):
    industry: Optional[str] = None
    business_type: Optional[str] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    main_business: Optional[str] = None

class HeadquartersDetail(HeadquartersDetailBase):
    id: UUID4
    headquarters_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# HeadquartersFacility Schema
class HeadquartersFacilityBase(BaseModel):
    name: str
    type: str
    location: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None

class HeadquartersFacilityCreate(HeadquartersFacilityBase):
    headquarters_id: UUID4

class HeadquartersFacilityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None

class HeadquartersFacility(HeadquartersFacilityBase):
    id: UUID4
    headquarters_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# HeadquartersHistory Schema
class HeadquartersHistoryBase(BaseModel):
    action_type: str
    previous_data: Optional[Dict] = None
    new_data: Optional[Dict] = None
    changed_by: UUID4

class HeadquartersHistoryCreate(HeadquartersHistoryBase):
    headquarters_id: UUID4

class HeadquartersHistory(HeadquartersHistoryBase):
    id: UUID4
    headquarters_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True 