#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
대시보드 서비스 클래스
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import psutil
import logging
from app.models.contract import Contract
from app.models.financial import FinancialRecord
from app.models.labor import Labor
from app.models.user import User
from app.schemas.dashboard import (
    DashboardResponse,
    ContractSummary,
    FinancialSummary,
    LaborSummary,
    SystemStatus,
    RecentActivity,
    SystemHealth
)

logger = logging.getLogger(__name__)


class DashboardService:
    """대시보드 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_summary(self, user_id: str) -> DashboardResponse:
        """대시보드 요약 데이터 조회"""
        try:
            contract_summary = self.get_contract_summary(user_id)
            financial_summary = self.get_financial_summary(user_id)
            labor_summary = self.get_labor_summary(user_id)
            system_status = self.get_system_status()
            recent_activities = self.get_recent_activities(user_id, 10)
            
            return DashboardResponse(
                contract_summary=contract_summary,
                financial_summary=financial_summary,
                labor_summary=labor_summary,
                system_status=system_status,
                recent_activities=recent_activities,
                alerts=self._get_alerts()
            )
        except Exception as e:
            logger.error(f"대시보드 요약 조회 실패: {e}")
            raise
    
    def get_contract_summary(self, user_id: str) -> ContractSummary:
        """계약 요약 정보 조회"""
        try:
            # 총 계약 수
            total_contracts = self.db.query(Contract).filter(
                Contract.user_id == user_id
            ).count()
            
            # 활성 계약 수
            active_contracts = self.db.query(Contract).filter(
                and_(
                    Contract.user_id == user_id,
                    Contract.status == "active"
                )
            ).count()
            
            # 완료된 계약 수
            completed_contracts = self.db.query(Contract).filter(
                and_(
                    Contract.user_id == user_id,
                    Contract.status == "completed"
                )
            ).count()
            
            # 총 계약 금액
            total_amount_result = self.db.query(
                func.sum(Contract.contract_amount)
            ).filter(Contract.user_id == user_id).scalar()
            total_contract_amount = float(total_amount_result or 0)
            
            # 평균 계약 금액
            average_contract_amount = (
                total_contract_amount / total_contracts if total_contracts > 0 else 0
            )
            
            # 상태별 계약 수
            status_counts = self.db.query(
                Contract.status,
                func.count(Contract.id)
            ).filter(Contract.user_id == user_id).group_by(Contract.status).all()
            
            contracts_by_status = {status: count for status, count in status_counts}
            
            return ContractSummary(
                total_contracts=total_contracts,
                active_contracts=active_contracts,
                completed_contracts=completed_contracts,
                total_contract_amount=total_contract_amount,
                average_contract_amount=average_contract_amount,
                contracts_by_status=contracts_by_status
            )
        except Exception as e:
            logger.error(f"계약 요약 조회 실패: {e}")
            raise
    
    def get_financial_summary(self, user_id: str) -> FinancialSummary:
        """재무 요약 정보 조회"""
        try:
            # 총 수익
            total_revenue_result = self.db.query(
                func.sum(FinancialRecord.amount)
            ).filter(
                and_(
                    FinancialRecord.user_id == user_id,
                    FinancialRecord.type == "revenue"
                )
            ).scalar()
            total_revenue = float(total_revenue_result or 0)
            
            # 총 지출
            total_expenses_result = self.db.query(
                func.sum(FinancialRecord.amount)
            ).filter(
                and_(
                    FinancialRecord.user_id == user_id,
                    FinancialRecord.type == "expense"
                )
            ).scalar()
            total_expenses = float(total_expenses_result or 0)
            
            # 순이익
            net_profit = total_revenue - total_expenses
            
            # 이익률
            profit_margin = (
                (net_profit / total_revenue * 100) if total_revenue > 0 else 0
            )
            
            # 월별 수익 (최근 6개월)
            monthly_revenue = self._get_monthly_financial_data(user_id, "revenue", 6)
            
            # 월별 지출 (최근 6개월)
            monthly_expenses = self._get_monthly_financial_data(user_id, "expense", 6)
            
            # 상위 지출 카테고리
            top_expense_categories = self._get_top_expense_categories(user_id)
            
            return FinancialSummary(
                total_revenue=total_revenue,
                total_expenses=total_expenses,
                net_profit=net_profit,
                profit_margin=profit_margin,
                monthly_revenue=monthly_revenue,
                monthly_expenses=monthly_expenses,
                top_expense_categories=top_expense_categories
            )
        except Exception as e:
            logger.error(f"재무 요약 조회 실패: {e}")
            raise
    
    def get_labor_summary(self, user_id: str) -> LaborSummary:
        """노무 요약 정보 조회"""
        try:
            # 총 근로자 수
            total_workers = self.db.query(Labor).filter(
                Labor.user_id == user_id
            ).count()
            
            # 활성 근로자 수
            active_workers = self.db.query(Labor).filter(
                and_(
                    Labor.user_id == user_id,
                    Labor.status == "active"
                )
            ).count()
            
            # 총 노무비
            total_labor_cost_result = self.db.query(
                func.sum(Labor.total_cost)
            ).filter(Labor.user_id == user_id).scalar()
            total_labor_cost = float(total_labor_cost_result or 0)
            
            # 평균 일당
            avg_daily_wage_result = self.db.query(
                func.avg(Labor.daily_wage)
            ).filter(Labor.user_id == user_id).scalar()
            average_daily_wage = float(avg_daily_wage_result or 0)
            
            # 직종별 근로자 수
            position_counts = self.db.query(
                Labor.position,
                func.count(Labor.id)
            ).filter(Labor.user_id == user_id).group_by(Labor.position).all()
            
            workers_by_position = {position: count for position, count in position_counts}
            
            # 월별 노무비 (최근 6개월)
            monthly_labor_cost = self._get_monthly_labor_cost(user_id, 6)
            
            return LaborSummary(
                total_workers=total_workers,
                active_workers=active_workers,
                total_labor_cost=total_labor_cost,
                average_daily_wage=average_daily_wage,
                workers_by_position=workers_by_position,
                monthly_labor_cost=monthly_labor_cost
            )
        except Exception as e:
            logger.error(f"노무 요약 조회 실패: {e}")
            raise
    
    def get_system_status(self) -> SystemStatus:
        """시스템 상태 정보 조회"""
        try:
            # 시스템 리소스 사용률
            memory_usage = psutil.virtual_memory().percent
            cpu_usage = psutil.cpu_percent()
            storage_usage = psutil.disk_usage('/').percent
            
            # 시스템 건강도 판단
            if memory_usage > 90 or cpu_usage > 90 or storage_usage > 90:
                system_health = SystemHealth.CRITICAL
            elif memory_usage > 70 or cpu_usage > 70 or storage_usage > 70:
                system_health = SystemHealth.WARNING
            else:
                system_health = SystemHealth.HEALTHY
            
            return SystemStatus(
                database_status="connected",
                api_status="running",
                storage_usage=storage_usage,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                last_backup=datetime.now() - timedelta(hours=6),  # 임시 데이터
                system_health=system_health
            )
        except Exception as e:
            logger.error(f"시스템 상태 조회 실패: {e}")
            raise
    
    def get_recent_activities(self, user_id: str, limit: int = 10) -> List[RecentActivity]:
        """최근 활동 내역 조회"""
        try:
            # 실제 구현에서는 활동 로그 테이블에서 조회
            # 현재는 임시 데이터 반환
            activities = []
            
            # 계약 관련 활동
            recent_contracts = self.db.query(Contract).filter(
                Contract.user_id == user_id
            ).order_by(Contract.created_at.desc()).limit(limit).all()
            
            for contract in recent_contracts:
                activities.append(RecentActivity(
                    id=f"contract_{contract.id}",
                    type="contract_created",
                    description=f"새로운 계약 생성: {contract.name}",
                    user_id=user_id,
                    user_name="사용자",  # 실제로는 사용자 이름 조회
                    timestamp=contract.created_at,
                    metadata={"contract_id": contract.id, "amount": contract.contract_amount}
                ))
            
            return activities[:limit]
        except Exception as e:
            logger.error(f"최근 활동 조회 실패: {e}")
            return []
    
    def _get_monthly_financial_data(self, user_id: str, type_: str, months: int) -> List[Dict[str, Any]]:
        """월별 재무 데이터 조회"""
        try:
            monthly_data = []
            current_date = datetime.now()
            
            for i in range(months):
                month_start = current_date.replace(day=1) - timedelta(days=30*i)
                month_end = month_start.replace(day=28) + timedelta(days=4)
                month_end = month_end.replace(day=1) - timedelta(days=1)
                
                amount_result = self.db.query(
                    func.sum(FinancialRecord.amount)
                ).filter(
                    and_(
                        FinancialRecord.user_id == user_id,
                        FinancialRecord.type == type_,
                        FinancialRecord.date >= month_start,
                        FinancialRecord.date <= month_end
                    )
                ).scalar()
                
                monthly_data.append({
                    "month": month_start.strftime("%Y-%m"),
                    "amount": float(amount_result or 0)
                })
            
            return monthly_data
        except Exception as e:
            logger.error(f"월별 재무 데이터 조회 실패: {e}")
            return []
    
    def _get_top_expense_categories(self, user_id: str) -> List[Dict[str, Any]]:
        """상위 지출 카테고리 조회"""
        try:
            categories = self.db.query(
                FinancialRecord.category,
                func.sum(FinancialRecord.amount)
            ).filter(
                and_(
                    FinancialRecord.user_id == user_id,
                    FinancialRecord.type == "expense"
                )
            ).group_by(FinancialRecord.category).order_by(
                func.sum(FinancialRecord.amount).desc()
            ).limit(5).all()
            
            return [
                {"category": category, "amount": float(amount)}
                for category, amount in categories
            ]
        except Exception as e:
            logger.error(f"상위 지출 카테고리 조회 실패: {e}")
            return []
    
    def _get_monthly_labor_cost(self, user_id: str, months: int) -> List[Dict[str, Any]]:
        """월별 노무비 조회"""
        try:
            monthly_data = []
            current_date = datetime.now()
            
            for i in range(months):
                month_start = current_date.replace(day=1) - timedelta(days=30*i)
                month_end = month_start.replace(day=28) + timedelta(days=4)
                month_end = month_end.replace(day=1) - timedelta(days=1)
                
                cost_result = self.db.query(
                    func.sum(Labor.total_cost)
                ).filter(
                    and_(
                        Labor.user_id == user_id,
                        Labor.date >= month_start,
                        Labor.date <= month_end
                    )
                ).scalar()
                
                monthly_data.append({
                    "month": month_start.strftime("%Y-%m"),
                    "cost": float(cost_result or 0)
                })
            
            return monthly_data
        except Exception as e:
            logger.error(f"월별 노무비 조회 실패: {e}")
            return []
    
    def _get_alerts(self) -> List[Dict[str, Any]]:
        """알림 목록 조회"""
        try:
            alerts = []
            
            # 시스템 리소스 알림
            memory_usage = psutil.virtual_memory().percent
            if memory_usage > 80:
                alerts.append({
                    "type": "warning",
                    "message": f"메모리 사용률이 높습니다: {memory_usage:.1f}%",
                    "timestamp": datetime.now()
                })
            
            # 계약 만료 알림 (실제 구현에서는 계약 만료일 체크)
            # 현재는 임시 데이터
            
            return alerts
        except Exception as e:
            logger.error(f"알림 조회 실패: {e}")
            return []

    def get_monthly_financial_data(self, year: int, month: int) -> Dict[str, Any]:
        """월별 재무 데이터 조회"""
        try:
            # 해당 월의 재무 기록 조회
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            records = self.db.query(FinancialRecord).filter(
                FinancialRecord.transaction_date >= start_date,
                FinancialRecord.transaction_date < end_date
            ).all()
            
            # 수입/지출 분류
            income = sum(r.amount for r in records if r.type == "수입" and r.amount)
            expense = sum(r.amount for r in records if r.type == "지출" and r.amount)
            
            return {
                "income": income,
                "expense": expense,
                "profit": income - expense,
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"월별 재무 데이터 조회 실패: {e}")
            return {"income": 0, "expense": 0, "profit": 0, "count": 0} 