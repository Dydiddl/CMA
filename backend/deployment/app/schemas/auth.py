#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인증 관련 Pydantic 스키마
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    """로그인 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """로그인 응답 스키마"""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(..., description="토큰 타입")
    user_id: str = Field(..., description="사용자 ID")
    email: str = Field(..., description="이메일")
    name: str = Field(..., description="사용자 이름")
    
    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    """회원가입 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    name: str = Field(..., min_length=2, max_length=50, description="사용자 이름")
    
    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    """회원가입 응답 스키마"""
    user_id: str = Field(..., description="사용자 ID")
    email: str = Field(..., description="이메일")
    name: str = Field(..., description="사용자 이름")
    message: str = Field(..., description="응답 메시지")
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """토큰 응답 스키마"""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(..., description="토큰 타입")
    
    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    """사용자 정보 스키마"""
    id: str = Field(..., description="사용자 ID")
    email: str = Field(..., description="이메일")
    name: str = Field(..., description="사용자 이름")
    role: str = Field(..., description="사용자 역할")
    is_active: bool = Field(..., description="활성 상태")
    
    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청 스키마"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=6, description="새 비밀번호")
    
    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    """비밀번호 재설정 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    
    class Config:
        from_attributes = True


class PasswordResetConfirm(BaseModel):
    """비밀번호 재설정 확인 스키마"""
    token: str = Field(..., description="재설정 토큰")
    new_password: str = Field(..., min_length=6, description="새 비밀번호")
    
    class Config:
        from_attributes = True 