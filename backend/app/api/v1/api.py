#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API v1 라우터
CMA 시스템의 모든 API 엔드포인트를 통합 관리
"""

from fastapi import APIRouter
from app.api.v1.endpoints import projects, tasks

api_router = APIRouter()

# 프로젝트 관련 엔드포인트
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])

# 작업 관련 엔드포인트
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# 향후 추가될 엔드포인트들
# api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
# api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
# api_router.include_router(labor.router, prefix="/labor", tags=["labor"])
# api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
# api_router.include_router(ascr.router, prefix="/ascr", tags=["ascr"]) 