#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
대시보드 관련 Pydantic 스키마
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ContractStatus(str, Enum):
    """계약 상태 열거형"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FinancialStatus(str, Enum):
    """재무 상태 열거형"""
    PROFIT = "profit"
    LOSS = "loss"
    BREAKEVEN = "breakeven"


class SystemHealth(str, Enum):
    """시스템 상태 열거형"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


class ContractSummary(BaseModel):
    """계약 요약 정보"""
    total_contracts: int = Field(..., description="총 계약 수")
    active_contracts: int = Field(..., description="진행중인 계약 수")
    completed_contracts: int = Field(..., description="완료된 계약 수")
    total_contract_amount: float = Field(..., description="총 계약 금액")
    average_contract_amount: float = Field(..., description="평균 계약 금액")
    contracts_by_status: Dict[str, int] = Field(..., description="상태별 계약 수")
    
    class Config:
        from_attributes = True


class FinancialSummary(BaseModel):
    """재무 요약 정보"""
    total_revenue: float = Field(..., description="총 수익")
    total_expenses: float = Field(..., description="총 지출")
    net_profit: float = Field(..., description="순이익")
    profit_margin: float = Field(..., description="이익률 (%)")
    monthly_revenue: List[Dict[str, Any]] = Field(..., description="월별 수익")
    monthly_expenses: List[Dict[str, Any]] = Field(..., description="월별 지출")
    top_expense_categories: List[Dict[str, Any]] = Field(..., description="상위 지출 카테고리")
    
    class Config:
        from_attributes = True


class LaborSummary(BaseModel):
    """노무 요약 정보"""
    total_workers: int = Field(..., description="총 근로자 수")
    active_workers: int = Field(..., description="활성 근로자 수")
    total_labor_cost: float = Field(..., description="총 노무비")
    average_daily_wage: float = Field(..., description="평균 일당")
    workers_by_position: Dict[str, int] = Field(..., description="직종별 근로자 수")
    monthly_labor_cost: List[Dict[str, Any]] = Field(..., description="월별 노무비")
    
    class Config:
        from_attributes = True


class SystemStatus(BaseModel):
    """시스템 상태 정보"""
    database_status: str = Field(..., description="데이터베이스 상태")
    api_status: str = Field(..., description="API 상태")
    storage_usage: float = Field(..., description="저장소 사용률 (%)")
    memory_usage: float = Field(..., description="메모리 사용률 (%)")
    cpu_usage: float = Field(..., description="CPU 사용률 (%)")
    last_backup: Optional[datetime] = Field(None, description="마지막 백업 시간")
    system_health: SystemHealth = Field(..., description="시스템 건강도")
    
    class Config:
        from_attributes = True


class RecentActivity(BaseModel):
    """최근 활동 정보"""
    id: str = Field(..., description="활동 ID")
    type: str = Field(..., description="활동 유형")
    description: str = Field(..., description="활동 설명")
    user_id: str = Field(..., description="사용자 ID")
    user_name: str = Field(..., description="사용자 이름")
    timestamp: datetime = Field(..., description="활동 시간")
    metadata: Optional[Dict[str, Any]] = Field(None, description="추가 메타데이터")
    
    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    """대시보드 응답 모델"""
    contract_summary: ContractSummary = Field(..., description="계약 요약")
    financial_summary: FinancialSummary = Field(..., description="재무 요약")
    labor_summary: LaborSummary = Field(..., description="노무 요약")
    system_status: SystemStatus = Field(..., description="시스템 상태")
    recent_activities: List[RecentActivity] = Field(..., description="최근 활동")
    alerts: List[Dict[str, Any]] = Field(default_factory=list, description="알림 목록")
    
    class Config:
        from_attributes = True


class DashboardFilter(BaseModel):
    """대시보드 필터 모델"""
    start_date: Optional[datetime] = Field(None, description="시작 날짜")
    end_date: Optional[datetime] = Field(None, description="종료 날짜")
    contract_status: Optional[ContractStatus] = Field(None, description="계약 상태 필터")
    include_inactive: bool = Field(default=True, description="비활성 포함 여부")
    
    class Config:
        from_attributes = True 