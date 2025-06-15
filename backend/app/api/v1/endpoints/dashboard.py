from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.crud import project as project_crud
from app.crud import budget as budget_crud
from app.crud import cost as cost_crud
from app.crud import contract as contract_crud
from app.schemas.dashboard import (
    ProjectDashboard,
    FinancialDashboard,
    DashboardResponse
)

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> DashboardResponse:
    """
    대시보드의 주요 지표를 조회합니다.
    """
    if not check_permissions(current_user, ["read:dashboard"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="대시보드 조회 권한이 없습니다"
        )
    
    # 프로젝트 현황 조회
    project_stats = get_project_stats(db, current_user)
    
    # 재무 현황 조회
    financial_stats = get_financial_stats(db, current_user)
    
    return DashboardResponse(
        project_stats=project_stats,
        financial_stats=financial_stats
    )

def get_project_stats(
    db: Session,
    current_user: User
) -> ProjectDashboard:
    """
    프로젝트 현황 통계를 조회합니다.
    """
    # 진행 중인 프로젝트
    in_progress_projects = project_crud.get_projects_by_status(
        db=db,
        status="in_progress",
        user_id=current_user.id
    )
    
    # 완료된 프로젝트
    completed_projects = project_crud.get_projects_by_status(
        db=db,
        status="completed",
        user_id=current_user.id
    )
    
    # 예정된 프로젝트
    planned_projects = project_crud.get_projects_by_status(
        db=db,
        status="planned",
        user_id=current_user.id
    )
    
    # 프로젝트별 진행률 계산
    project_progress = []
    for project in in_progress_projects:
        progress = project_crud.calculate_project_progress(db=db, project_id=project.id)
        project_progress.append({
            "project_id": project.id,
            "project_name": project.name,
            "progress": progress
        })
    
    return ProjectDashboard(
        total_projects=len(in_progress_projects) + len(completed_projects) + len(planned_projects),
        in_progress_count=len(in_progress_projects),
        completed_count=len(completed_projects),
        planned_count=len(planned_projects),
        project_progress=project_progress
    )

def get_financial_stats(
    db: Session,
    current_user: User
) -> FinancialDashboard:
    """
    재무 현황 통계를 조회합니다.
    """
    # 총 예산
    total_budget = budget_crud.get_total_budget(db=db, user_id=current_user.id)
    
    # 사용 금액
    total_cost = cost_crud.get_total_cost(db=db, user_id=current_user.id)
    
    # 계약 금액
    total_contract = contract_crud.get_total_contract_amount(db=db, user_id=current_user.id)
    
    # 미수금
    total_receivable = contract_crud.get_total_receivable(db=db, user_id=current_user.id)
    
    # 월별 비용 추이 (최근 6개월)
    monthly_costs = []
    for i in range(6):
        month = datetime.now() - timedelta(days=30*i)
        cost = cost_crud.get_monthly_cost(
            db=db,
            year=month.year,
            month=month.month,
            user_id=current_user.id
        )
        monthly_costs.append({
            "year": month.year,
            "month": month.month,
            "amount": cost
        })
    
    return FinancialDashboard(
        total_budget=total_budget,
        total_cost=total_cost,
        total_contract=total_contract,
        total_receivable=total_receivable,
        monthly_costs=monthly_costs
    ) 