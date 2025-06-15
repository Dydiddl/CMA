from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    projects,
    tasks,
    contracts,
    documents,
    notifications,
    labor,
    api_docs,
    construction_sites,
    departments,
    daily_reports,
    costs,
    budgets
)

api_router = APIRouter()

# 인증 관련 엔드포인트
api_router.include_router(auth.router, prefix="/auth", tags=["인증"])

# 사용자 관련 엔드포인트
api_router.include_router(users.router, prefix="/users", tags=["사용자"])

# 프로젝트 관련 엔드포인트
api_router.include_router(projects.router, prefix="/projects", tags=["프로젝트"])

# 작업 관련 엔드포인트
api_router.include_router(tasks.router, prefix="/tasks", tags=["작업"])

# 계약 관련 엔드포인트
api_router.include_router(contracts.router, prefix="/contracts", tags=["계약"])

# 문서 관련 엔드포인트
api_router.include_router(documents.router, prefix="/documents", tags=["문서"])

# 알림 관련 엔드포인트
api_router.include_router(notifications.router, prefix="/notifications", tags=["알림"])

# 인력 관련 엔드포인트
api_router.include_router(labor.router, prefix="/labor", tags=["인력"])

# API 문서 관련 엔드포인트
api_router.include_router(api_docs.router, prefix="/api-docs", tags=["API 문서"])

# 현장 관련 엔드포인트
api_router.include_router(construction_sites.router, prefix="/construction-sites", tags=["현장"])

# 부서 관련 엔드포인트
api_router.include_router(departments.router, prefix="/departments", tags=["부서"])

# 일일 보고서 관련 엔드포인트
api_router.include_router(daily_reports.router, prefix="/daily-reports", tags=["일일 보고서"])

# 비용 관련 엔드포인트
api_router.include_router(costs.router, prefix="/costs", tags=["비용"])

# 예산 관련 엔드포인트
api_router.include_router(budgets.router, prefix="/budgets", tags=["예산"]) 