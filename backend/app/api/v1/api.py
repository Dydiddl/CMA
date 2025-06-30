#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API v1 라우터
CMA 시스템의 모든 API 엔드포인트를 통합 관리
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    projects, 
    tasks, 
    contracts, 
    financial, 
    labor, 
    ascr, 
    auth, 
    users, 
    vendors, 
    dashboard,
    performance
)

api_router = APIRouter()

# 인증 관련 엔드포인트
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# 사용자 관련 엔드포인트
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 프로젝트 관련 엔드포인트
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])

# 작업 관련 엔드포인트
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# 계약 관련 엔드포인트
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])

# 재무 관련 엔드포인트
api_router.include_router(financial.router, prefix="/financial", tags=["financial"])

# 노무 관련 엔드포인트
api_router.include_router(labor.router, prefix="/labor", tags=["labor"])

# 거래처 관련 엔드포인트
api_router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])

# ASCR 모듈 엔드포인트
api_router.include_router(ascr.router, prefix="/ascr", tags=["ascr"])

# 대시보드 엔드포인트
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# 성능 모니터링 엔드포인트
api_router.include_router(performance.router, prefix="/performance", tags=["performance"])

# 향후 추가될 엔드포인트들
# api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
# api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
# api_router.include_router(labor.router, prefix="/labor", tags=["labor"])
# api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
# api_router.include_router(ascr.router, prefix="/ascr", tags=["ascr"]) 