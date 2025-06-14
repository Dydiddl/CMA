from app.schemas.common_types import *
from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional, Dict
from datetime import datetime

# User Base Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    department_id: Optional[UUID4] = None
    position: Optional[str] = None
    status: str = 'active'

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[UUID4] = None
    position: Optional[str] = None
    status: Optional[str] = None

class User(UserBase):
    id: UUID4
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# UserProfile Schema
class UserProfileBase(BaseModel):
    profile_image: Optional[str] = None
    language: str = 'ko'
    timezone: str = 'Asia/Seoul'
    notification_settings: Optional[Dict] = None
    theme_settings: Optional[Dict] = None

class UserProfileCreate(UserProfileBase):
    user_id: UUID4

class UserProfileUpdate(BaseModel):
    profile_image: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    notification_settings: Optional[Dict] = None
    theme_settings: Optional[Dict] = None

class UserProfile(UserProfileBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# UserHistory Schema
class UserHistoryBase(BaseModel):
    action_type: str
    previous_data: Optional[Dict] = None
    new_data: Optional[Dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class UserHistoryCreate(UserHistoryBase):
    user_id: UUID4

class UserHistory(UserHistoryBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True 