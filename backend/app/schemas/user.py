#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사용자 관련 Pydantic 스키마
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr = Field(..., description="이메일")
    full_name: str = Field(..., min_length=2, max_length=100, description="전체 이름")
    role: str = Field(default="user", description="사용자 역할")
    department: str = Field(default="", max_length=100, description="부서")
    phone: str = Field(default="", max_length=20, description="전화번호")
    is_active: bool = Field(default=True, description="활성 상태")
    
    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """사용자 생성 스키마"""
    password: str = Field(..., min_length=6, description="비밀번호")
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """사용자 수정 스키마"""
    email: Optional[EmailStr] = Field(None, description="이메일")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="전체 이름")
    role: Optional[str] = Field(None, description="사용자 역할")
    department: Optional[str] = Field(None, max_length=100, description="부서")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    is_active: Optional[bool] = Field(None, description="활성 상태")
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    id: str = Field(..., description="사용자 ID")
    created_at: datetime = Field(..., description="생성일")
    updated_at: datetime = Field(..., description="수정일")
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """사용자 목록 응답 스키마"""
    status: str = Field(default="success", description="응답 상태")
    data: List[UserResponse] = Field(..., description="사용자 목록")
    total: int = Field(..., description="전체 사용자 수")
    page: int = Field(..., description="현재 페이지")
    size: int = Field(..., description="페이지 크기")
    message: Optional[str] = Field(None, description="응답 메시지")
    
    class Config:
        from_attributes = True


class UserPasswordUpdate(BaseModel):
    """사용자 비밀번호 수정 스키마"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=6, description="새 비밀번호")
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """사용자 프로필 수정 스키마"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="전체 이름")
    department: Optional[str] = Field(None, max_length=100, description="부서")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """사용자 통계 스키마"""
    total_users: int = Field(..., description="전체 사용자 수")
    active_users: int = Field(..., description="활성 사용자 수")
    inactive_users: int = Field(..., description="비활성 사용자 수")
    users_by_role: dict = Field(..., description="역할별 사용자 수")
    
    class Config:
        from_attributes = True 