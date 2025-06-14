from app.schemas.common_types import *
from pydantic import BaseModel, UUID4, EmailStr, constr, validator
from typing import Optional, Dict
from datetime import datetime

# User Base Schema
class UserBase(BaseModel):
    """
    사용자 기본 정보 스키마
    이메일과 사용자 이름을 포함합니다.
    """
    email: EmailStr  # 이메일 주소 (이메일 형식 검증)
    username: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: str
    phone: Optional[str] = None
    department_id: Optional[UUID4] = None
    position: Optional[str] = None
    status: str = 'active'

class UserCreate(UserBase):
    """
    사용자 생성 요청 스키마
    기본 정보에 비밀번호를 추가합니다.
    """
    password: constr(min_length=8, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('비밀번호는 최소 1개의 대문자를 포함해야 합니다')
        if not any(c.islower() for c in v):
            raise ValueError('비밀번호는 최소 1개의 소문자를 포함해야 합니다')
        if not any(c.isdigit() for c in v):
            raise ValueError('비밀번호는 최소 1개의 숫자를 포함해야 합니다')
        if not any(c in '!@#$%^&*()' for c in v):
            raise ValueError('비밀번호는 최소 1개의 특수문자를 포함해야 합니다')
        return v

class UserUpdate(BaseModel):
    """
    사용자 정보 수정 요청 스키마
    모든 필드가 선택적(Optional)입니다.
    """
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")] = None
    password: Optional[constr(min_length=8, max_length=100)] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[UUID4] = None
    position: Optional[str] = None
    status: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

# UserProfile Schema
class UserProfileBase(BaseModel):
    full_name: constr(min_length=2, max_length=100)
    phone_number: constr(regex="^[0-9]{10,11}$")
    position: Optional[constr(max_length=100)] = None
    profile_image: Optional[str] = None
    language: str = 'ko'
    timezone: str = 'Asia/Seoul'
    notification_settings: Optional[Dict] = None
    theme_settings: Optional[Dict] = None

class UserProfileCreate(UserProfileBase):
    user_id: UUID4

class UserProfileUpdate(UserProfileBase):
    full_name: Optional[constr(min_length=2, max_length=100)] = None
    phone_number: Optional[constr(regex="^[0-9]{10,11}$")] = None

class UserProfileInDBBase(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserProfile(UserProfileInDBBase):
    pass

class UserProfileInDB(UserProfileInDBBase):
    pass

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