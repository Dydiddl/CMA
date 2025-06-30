#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
거래처 관리 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.schemas.vendor import (
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    VendorListResponse
)
from app.services.vendor import VendorService
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    새로운 거래처를 생성합니다.
    
    Args:
        vendor: 거래처 생성 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        VendorResponse: 생성된 거래처 정보
        
    Raises:
        HTTPException: 400 - 유효하지 않은 데이터
        HTTPException: 500 - 서버 오류
    """
    try:
        vendor_service = VendorService(db)
        result = vendor_service.create_vendor(vendor, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="거래처 생성 중 오류가 발생했습니다."
        )


@router.get("/", response_model=VendorListResponse)
async def get_vendors(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 레코드 수"),
    search: Optional[str] = Query(None, description="검색어"),
    status_filter: Optional[str] = Query(None, alias="status", description="상태 필터"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    거래처 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 레코드 수
        limit: 가져올 레코드 수
        search: 검색어
        status_filter: 상태 필터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        VendorListResponse: 거래처 목록 및 페이징 정보
    """
    try:
        vendor_service = VendorService(db)
        vendors, total = vendor_service.get_vendors(
            skip=skip, limit=limit, search=search, status=status_filter
        )
        return VendorListResponse(
            data=vendors,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="거래처 목록 조회 중 오류가 발생했습니다."
        )


@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(
    vendor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 거래처의 정보를 조회합니다.
    
    Args:
        vendor_id: 거래처 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        VendorResponse: 거래처 정보
        
    Raises:
        HTTPException: 404 - 거래처를 찾을 수 없음
    """
    try:
        vendor_service = VendorService(db)
        vendor = vendor_service.get_vendor_by_id(vendor_id)
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="거래처를 찾을 수 없습니다."
            )
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="거래처 조회 중 오류가 발생했습니다."
        )


@router.put("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(
    vendor_id: str,
    vendor_update: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    거래처 정보를 수정합니다.
    
    Args:
        vendor_id: 거래처 ID
        vendor_update: 수정할 거래처 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        VendorResponse: 수정된 거래처 정보
        
    Raises:
        HTTPException: 400 - 유효하지 않은 데이터
        HTTPException: 404 - 거래처를 찾을 수 없음
    """
    try:
        vendor_service = VendorService(db)
        vendor = vendor_service.update_vendor(vendor_id, vendor_update)
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="거래처를 찾을 수 없습니다."
            )
        return vendor
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
            detail="거래처 수정 중 오류가 발생했습니다."
        )


@router.delete("/{vendor_id}")
async def delete_vendor(
    vendor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    거래처를 삭제합니다.
    
    Args:
        vendor_id: 거래처 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        Dict: 삭제 결과
        
    Raises:
        HTTPException: 404 - 거래처를 찾을 수 없음
    """
    try:
        vendor_service = VendorService(db)
        success = vendor_service.delete_vendor(vendor_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="거래처를 찾을 수 없습니다."
            )
        return {
            "status": "success",
            "message": "거래처가 성공적으로 삭제되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="거래처 삭제 중 오류가 발생했습니다."
        ) 