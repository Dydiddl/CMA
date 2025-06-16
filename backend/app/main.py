"""
FastAPI 애플리케이션 메인 모듈
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
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

# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 커스텀 미들웨어 추가
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# 예외 핸들러 등록
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(AuthenticationError, authentication_exception_handler)
app.add_exception_handler(AuthorizationError, authorization_exception_handler)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """
    루트 엔드포인트
    """
    return {"message": "Welcome to Construction Management API"} 