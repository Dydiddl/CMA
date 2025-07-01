#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인증 관련 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.api.deps import get_db, get_current_user
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse
)
from app.services.auth import AuthService
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    사용자 로그인
    
    Args:
        login_data: 로그인 데이터
        db: 데이터베이스 세션
        
    Returns:
        LoginResponse: 로그인 응답
        
    Raises:
        HTTPException: 401 - 인증 실패
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )
        
        access_token = create_access_token(data={"sub": user.email})
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            name=user.full_name
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[로그인 오류]", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그인 중 오류가 발생했습니다."
        )


@router.post("/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    사용자 회원가입
    
    Args:
        register_data: 회원가입 데이터
        db: 데이터베이스 세션
        
    Returns:
        RegisterResponse: 회원가입 응답
        
    Raises:
        HTTPException: 400 - 유효하지 않은 데이터
        HTTPException: 409 - 이미 존재하는 사용자
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(register_data)
        
        return RegisterResponse(
            user_id=user.id,
            email=user.email,
            name=user.full_name,
            message="회원가입이 성공적으로 완료되었습니다."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="회원가입 중 오류가 발생했습니다."
        )


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 토큰 발급
    
    Args:
        form_data: OAuth2 폼 데이터
        db: 데이터베이스 세션
        
    Returns:
        TokenResponse: 토큰 응답
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.email})
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="토큰 발급 중 오류가 발생했습니다."
        )


@router.post("/logout")
async def logout():
    """
    사용자 로그아웃
    
    Returns:
        Dict: 로그아웃 응답
    """
    return {
        "status": "success",
        "message": "로그아웃이 완료되었습니다."
    }


@router.get("/me")
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    현재 사용자 정보 조회
    
    Args:
        current_user: 현재 사용자
        
    Returns:
        Dict: 사용자 정보
    """
    return {
        "status": "success",
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.full_name,
            "role": current_user.role
        }
    } 