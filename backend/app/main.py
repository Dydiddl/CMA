#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 시스템 메인 애플리케이션
건설 관리 시스템의 FastAPI 애플리케이션 진입점
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.middleware.performance import PerformanceMiddleware
from app.core.cache import HybridCache, cleanup_cache_periodically

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="CMA - Construction Management System",
    description="건설 관리 시스템 API",
    version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 성능 모니터링 미들웨어 추가
performance_middleware = PerformanceMiddleware(app)
app.add_middleware(PerformanceMiddleware)

# 전역 캐시 인스턴스 생성
cache = HybridCache(redis_url=getattr(settings, 'REDIS_URL', None))

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행되는 이벤트"""
    # 성능 모니터링 시작
    await performance_middleware.start_monitoring()
    
    # 캐시 정리 작업 시작
    import asyncio
    asyncio.create_task(cleanup_cache_periodically())

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "CMA - Construction Management System",
        "version": "3.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

@app.get("/performance")
async def get_performance_info():
    """성능 정보 엔드포인트"""
    return performance_middleware.get_performance_stats()

@app.get("/cache/status")
async def get_cache_status():
    """캐시 상태 엔드포인트"""
    return {
        "cache_type": "hybrid",
        "redis_available": cache.use_redis,
        "memory_cache_size": len(cache.memory_cache.cache)
    }

# 테스트용 엔드포인트 (인증 없이)
@app.get("/test/contracts")
async def test_get_contracts():
    """테스트용 계약 목록 조회"""
    return {
        "status": "success",
        "data": [
            {
                "id": "1",
                "name": "테스트 계약 1",
                "contract_number": "CON-2024-001",
                "contract_amount": 1000000,
                "client_name": "테스트 발주처",
                "status": "진행중"
            },
            {
                "id": "2",
                "name": "테스트 계약 2",
                "contract_number": "CON-2024-002",
                "contract_amount": 2000000,
                "client_name": "테스트 발주처 2",
                "status": "완료"
            }
        ],
        "total": 2
    }

@app.get("/test/financial")
async def test_get_financial():
    """테스트용 재무 정보 조회"""
    return {
        "status": "success",
        "data": {
            "total_revenue": 5000000,
            "total_expenses": 3000000,
            "profit": 2000000
        }
    }

@app.get("/test/labor")
async def test_get_labor():
    """테스트용 노무 정보 조회"""
    return {
        "status": "success",
        "data": [
            {
                "id": "1",
                "worker_name": "홍길동",
                "position": "현장소장",
                "salary": 5000000,
                "work_hours": 160
            },
            {
                "id": "2",
                "worker_name": "김철수",
                "position": "기술자",
                "salary": 3500000,
                "work_hours": 160
            }
        ],
        "total": 2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 