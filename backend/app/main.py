from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from backend.app.core.config import settings
from backend.app.api.v1.api import api_router
from backend.app.core.error_handlers import (
    validation_exception_handler,
    integrity_error_handler,
    permission_error_handler,
    not_found_error_handler,
    general_exception_handler
)
from backend.app.schemas.error import (
    ErrorResponse,
    ValidationErrorResponse,
    PermissionErrorResponse,
    NotFoundErrorResponse
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="""
    건설 프로젝트 관리 시스템 API
    
    ## 기능
    * 프로젝트 관리
    * 작업 관리
    * 파일 업로드/다운로드
    * 사용자 관리
    
    ## 인증
    * JWT 토큰 기반 인증
    * OAuth2 비밀번호 흐름
    
    ## 권한
    * 관리자: 모든 기능 접근 가능
    * 일반 사용자: 자신의 프로젝트와 작업만 접근 가능
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        401: {"model": ErrorResponse, "description": "인증되지 않은 요청"},
        403: {"model": PermissionErrorResponse, "description": "권한이 없는 요청"},
        404: {"model": NotFoundErrorResponse, "description": "리소스를 찾을 수 없음"},
        422: {"model": ValidationErrorResponse, "description": "유효성 검사 실패"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)

# CORS 설정
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 에러 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(PermissionErrorResponse, permission_error_handler)
app.add_exception_handler(NotFoundErrorResponse, not_found_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    """
    API 루트 엔드포인트
    """
    return {
        "message": "건설 프로젝트 관리 시스템 API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    } 