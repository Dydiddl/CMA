#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 메인 애플리케이션 - 성능 최적화 버전
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any

from app.core.database import create_tables
from app.core.cache import get_cache_stats
from app.middleware.performance import PerformanceMiddleware, get_performance_middleware, set_performance_middleware
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware
from app.utils.error_handlers import (
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    validation_exception_handler,
    authentication_exception_handler,
    authorization_exception_handler
)
from app.api.v1.api import api_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시
    logger.info("CMA 애플리케이션 시작 중...")
    
    # 데이터베이스 테이블 생성
    try:
        create_tables()
        logger.info("데이터베이스 테이블 생성 완료")
    except Exception as e:
        logger.error(f"데이터베이스 테이블 생성 실패: {e}")
    
    # 성능 모니터링 미들웨어 설정
    performance_middleware = PerformanceMiddleware(app, threshold_ms=500.0)
    set_performance_middleware(performance_middleware)
    
    logger.info("CMA 애플리케이션 시작 완료")
    
    yield
    
    # 종료 시
    logger.info("CMA 애플리케이션 종료 중...")
    
    # 성능 통계 출력
    try:
        stats = performance_middleware.get_performance_stats()
        logger.info(f"최종 성능 통계: {stats}")
    except Exception as e:
        logger.error(f"성능 통계 수집 실패: {e}")
    
    logger.info("CMA 애플리케이션 종료 완료")

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="CMA (Construction Management System)",
    description="건설 관리 시스템 API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip 압축 미들웨어 (성능 향상)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 성능 모니터링 미들웨어 추가
performance_middleware = PerformanceMiddleware(app, threshold_ms=500.0)
app.add_middleware(PerformanceMiddleware, threshold_ms=500.0)

# 커스텀 미들웨어 추가
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# 예외 핸들러 등록
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(AuthenticationError, authentication_exception_handler)
app.add_exception_handler(AuthorizationError, authorization_exception_handler)

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "CMA (Construction Management System) API",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

@app.get("/performance/stats")
async def get_performance_stats():
    """성능 통계 조회"""
    try:
        middleware = get_performance_middleware()
        if middleware:
            stats = middleware.get_performance_stats()
        else:
            stats = {"error": "성능 모니터링 미들웨어가 초기화되지 않았습니다"}
        
        # 캐시 통계 추가
        cache_stats = get_cache_stats()
        stats["cache"] = cache_stats
        
        return stats
    except Exception as e:
        logger.error(f"성능 통계 조회 실패: {e}")
        return {"error": str(e)}

@app.get("/performance/database")
async def get_database_performance():
    """데이터베이스 성능 통계 조회"""
    try:
        from app.middleware.performance import get_database_middleware
        db_middleware = get_database_middleware()
        return db_middleware.get_database_stats()
    except Exception as e:
        logger.error(f"데이터베이스 성능 통계 조회 실패: {e}")
        return {"error": str(e)}

@app.middleware("http")
async def performance_middleware_func(request: Request, call_next):
    """성능 모니터링 미들웨어 함수"""
    start_time = time.time()
    
    # 요청 처리
    response = await call_next(request)
    
    # 처리 시간 계산
    process_time = (time.time() - start_time) * 1000
    
    # 성능 로그 기록
    logger.info(
        f"요청 처리: {request.method} {request.url.path} - "
        f"상태코드: {response.status_code}, "
        f"처리시간: {process_time:.2f}ms"
    )
    
    # 응답 헤더에 성능 정보 추가
    response.headers["X-Process-Time"] = f"{process_time:.2f}"
    
    return response

if __name__ == "__main__":
    import uvicorn
    
    # 성능 최적화된 서버 설정
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,  # 개발 환경에서는 1개 워커
        log_level="info",
        access_log=True
    ) 