#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 메인 애플리케이션
건설 관리 시스템 메인 서버
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/cma.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# API 라우터 임포트
from app.api.v1.endpoints import contracts, financial, labor, users, vendors
from app.services.ascr.api_integration import router as ascr_router
from app.services.ascr.web_interface import router as ascr_web_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("CMA 애플리케이션 시작")
    
    # 필요한 디렉토리 생성
    Path("logs").mkdir(exist_ok=True)
    Path("uploads").mkdir(exist_ok=True)
    Path("uploads/ascr").mkdir(exist_ok=True)
    Path("temp").mkdir(exist_ok=True)
    
    yield
    
    # 종료 시 실행
    logger.info("CMA 애플리케이션 종료")

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="CMA - Construction Management System",
    description="건설 관리 시스템 API",
    version="2.0.0",
    lifespan=lifespan
)

# 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# API 라우터 등록
app.include_router(contracts.router, prefix="/api/v1")
app.include_router(financial.router, prefix="/api/v1")
app.include_router(labor.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(vendors.router, prefix="/api/v1")

# ASCR 모듈 라우터 등록
app.include_router(ascr_router)
app.include_router(ascr_web_router)

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "CMA Construction Management System",
        "version": "2.0.0",
        "status": "running",
        "modules": {
            "contracts": "available",
            "financial": "available", 
            "labor": "available",
            "users": "available",
            "vendors": "available",
            "ascr": "available"
        }
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "2.0.0"
    }

@app.get("/api/v1/status")
async def api_status():
    """API 상태 조회"""
    return {
        "api_version": "v1",
        "status": "active",
        "endpoints": {
            "contracts": "/api/v1/contracts",
            "financial": "/api/v1/financial", 
            "labor": "/api/v1/labor",
            "users": "/api/v1/users",
            "vendors": "/api/v1/vendors",
            "ascr": "/api/v1/ascr"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 