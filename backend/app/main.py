from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
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
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
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