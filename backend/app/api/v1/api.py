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
    api_docs
)

api_router = APIRouter()

# 인증 관련 엔드포인트
api_router.include_router(auth.router, prefix="/auth", tags=["인증"])

# 사용자 관련 엔드포인트
api_router.include_router(users.router, prefix="/users", tags=["사용자"])

# 프로젝트 관련 엔드포인트
api_router.include_router(projects.router, prefix="/projects", tags=["프로젝트"])

# 작업 관련 엔드포인트
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# 계약 관련 엔드포인트
api_router.include_router(contracts.router, prefix="/contracts", tags=["계약"])

# 문서 관련 엔드포인트
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])

# 알림 관련 엔드포인트
api_router.include_router(notifications.router, prefix="/notifications", tags=["알림"])

# 인력 관련 엔드포인트
api_router.include_router(labor.router, prefix="/labor", tags=["인력"])

# API 문서 관련 엔드포인트
api_router.include_router(api_docs.router, prefix="/api-docs", tags=["API 문서"]) 