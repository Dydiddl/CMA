#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
대시보드 관련 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta
from app.api.deps import get_db, get_current_user
from app.schemas.dashboard import (
    DashboardResponse,
    ContractSummary,
    FinancialSummary,
    LaborSummary,
    SystemStatus
)
from app.services.dashboard import DashboardService
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=DashboardResponse)
async def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    대시보드 데이터를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        DashboardResponse: 대시보드 요약 데이터
        
    Raises:
        HTTPException: 500 - 서버 오류
    """
    try:
        dashboard_service = DashboardService(db)
        dashboard_data = dashboard_service.get_dashboard_summary(current_user.id)
        return dashboard_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="대시보드 데이터 조회 중 오류가 발생했습니다."
        )


@router.get("/contracts/summary", response_model=ContractSummary)
async def get_contract_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    계약 요약 정보를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        ContractSummary: 계약 요약 정보
    """
    try:
        dashboard_service = DashboardService(db)
        contract_summary = dashboard_service.get_contract_summary(current_user.id)
        return contract_summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="계약 요약 조회 중 오류가 발생했습니다."
        )


@router.get("/financial/summary", response_model=FinancialSummary)
async def get_financial_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    재무 요약 정보를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        FinancialSummary: 재무 요약 정보
    """
    try:
        dashboard_service = DashboardService(db)
        financial_summary = dashboard_service.get_financial_summary(current_user.id)
        return financial_summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="재무 요약 조회 중 오류가 발생했습니다."
        )


@router.get("/labor/summary", response_model=LaborSummary)
async def get_labor_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    노무 요약 정보를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        LaborSummary: 노무 요약 정보
    """
    try:
        dashboard_service = DashboardService(db)
        labor_summary = dashboard_service.get_labor_summary(current_user.id)
        return labor_summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="노무 요약 조회 중 오류가 발생했습니다."
        )


@router.get("/system/status", response_model=SystemStatus)
async def get_system_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    시스템 상태 정보를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        SystemStatus: 시스템 상태 정보
    """
    try:
        dashboard_service = DashboardService(db)
        system_status = dashboard_service.get_system_status()
        return system_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="시스템 상태 조회 중 오류가 발생했습니다."
        )


@router.get("/recent-activities")
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    최근 활동 내역을 조회합니다.
    
    Args:
        limit: 조회할 활동 수
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        List[Dict]: 최근 활동 목록
    """
    try:
        dashboard_service = DashboardService(db)
        activities = dashboard_service.get_recent_activities(current_user.id, limit)
        return {
            "status": "success",
            "data": activities,
            "message": "최근 활동 조회 완료"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="최근 활동 조회 중 오류가 발생했습니다."
        ) 