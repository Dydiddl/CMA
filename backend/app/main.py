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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 