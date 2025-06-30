#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사용자 관리 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse
)
from app.services.user import UserService
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 레코드 수"),
    search: Optional[str] = Query(None, description="검색어"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 레코드 수
        limit: 가져올 레코드 수
        search: 검색어
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        UserListResponse: 사용자 목록 및 페이징 정보
    """
    try:
        user_service = UserService(db)
        users, total = user_service.get_users(
            skip=skip, limit=limit, search=search
        )
        return UserListResponse(
            data=users,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 목록 조회 중 오류가 발생했습니다."
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 사용자의 정보를 조회합니다.
    
    Args:
        user_id: 사용자 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        UserResponse: 사용자 정보
        
    Raises:
        HTTPException: 404 - 사용자를 찾을 수 없음
    """
    try:
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 조회 중 오류가 발생했습니다."
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자 정보를 수정합니다.
    
    Args:
        user_id: 사용자 ID
        user_update: 수정할 사용자 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        UserResponse: 수정된 사용자 정보
        
    Raises:
        HTTPException: 400 - 유효하지 않은 데이터
        HTTPException: 404 - 사용자를 찾을 수 없음
    """
    try:
        user_service = UserService(db)
        user = user_service.update_user(user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 수정 중 오류가 발생했습니다."
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자를 삭제합니다.
    
    Args:
        user_id: 사용자 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        Dict: 삭제 결과
        
    Raises:
        HTTPException: 404 - 사용자를 찾을 수 없음
    """
    try:
        user_service = UserService(db)
        success = user_service.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        return {
            "status": "success",
            "message": "사용자가 성공적으로 삭제되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 삭제 중 오류가 발생했습니다."
        )


@router.post("/{user_id}/activate")
async def activate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자를 활성화합니다.
    
    Args:
        user_id: 사용자 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        Dict: 활성화 결과
    """
    try:
        user_service = UserService(db)
        success = user_service.activate_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        return {
            "status": "success",
            "message": "사용자가 활성화되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 활성화 중 오류가 발생했습니다."
        )


@router.post("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    사용자를 비활성화합니다.
    
    Args:
        user_id: 사용자 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        Dict: 비활성화 결과
    """
    try:
        user_service = UserService(db)
        success = user_service.deactivate_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        return {
            "status": "success",
            "message": "사용자가 비활성화되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 비활성화 중 오류가 발생했습니다."
        ) 