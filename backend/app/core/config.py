from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    환경변수와 기본값을 통해 설정을 관리합니다.
    """
    
    # 프로젝트 기본 정보
    PROJECT_NAME: str = "Construction Management App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = "건설회사 관리 시스템 API"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # 데이터베이스 설정 (로컬 우선)
    USE_LOCAL_DB: bool = True  # True: SQLite 사용, False: Supabase 사용
    DATABASE_URL: str = "sqlite:///./construction_management.db"
    
    # Supabase 설정 (선택사항 - 클라우드 사용시에만)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # JWT 인증 설정
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS 설정
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "tauri://localhost",
        "https://tauri.localhost"
    ]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    
    # 파일 업로드 설정
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_EXTENSIONS: List[str] = [
        ".pdf", ".doc", ".docx", ".hwp", 
        ".xls", ".xlsx", ".jpg", ".jpeg", ".png"
    ]
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    # 보안 설정
    BCRYPT_ROUNDS: int = 12
    
    # 애플리케이션 경로 설정
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # 데이터베이스 파일 경로 설정
    @property
    def db_path(self) -> Path:
        """데이터베이스 파일 경로 반환"""
        if self.USE_LOCAL_DB:
            return self.BASE_DIR / "construction_management.db"
        return None
    
    @property
    def upload_path(self) -> Path:
        """업로드 디렉토리 경로 반환"""
        path = self.BASE_DIR / self.UPLOAD_DIR
        path.mkdir(exist_ok=True)
        return path
    
    @property
    def is_development(self) -> bool:
        """개발 환경 여부 확인"""
        return self.DEBUG
    
    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부 확인"""
        return not self.DEBUG
    
    @property
    def is_using_local_db(self) -> bool:
        """로컬 DB 사용 여부 확인"""
        return self.USE_LOCAL_DB
    
    def get_database_url(self) -> str:
        """사용할 데이터베이스 URL 반환"""
        if self.USE_LOCAL_DB:
            return self.DATABASE_URL
        else:
            # Supabase PostgreSQL URL 형식으로 변환
            if self.SUPABASE_URL and self.SUPABASE_KEY:
                return f"postgresql://postgres:[password]@[host]:5432/postgres"
            raise ValueError("Supabase 설정이 필요합니다.")
    
    def get_supabase_config(self) -> dict:
        """Supabase 설정 반환 (클라우드 사용시에만)"""
        if not self.USE_LOCAL_DB:
            return {
                "url": self.SUPABASE_URL,
                "key": self.SUPABASE_KEY,
                "service_key": self.SUPABASE_SERVICE_KEY
            }
        return {}
    
    def get_cors_config(self) -> dict:
        """CORS 설정 반환"""
        return {
            "allow_origins": self.ALLOWED_ORIGINS,
            "allow_methods": self.ALLOWED_METHODS,
            "allow_headers": self.ALLOWED_HEADERS,
            "allow_credentials": self.ALLOW_CREDENTIALS
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# 전역 설정 인스턴스
settings = Settings()

# 개발 환경에서 설정 검증
if settings.is_development:
    if settings.USE_LOCAL_DB:
        print(f"🗄️  로컬 SQLite 데이터베이스 사용: {settings.db_path}")
    else:
        if not settings.SUPABASE_URL:
            print("⚠️  Warning: SUPABASE_URL이 설정되지 않았습니다.")
        if not settings.SUPABASE_KEY:
            print("⚠️  Warning: SUPABASE_KEY가 설정되지 않았습니다.")
    
    if settings.SECRET_KEY == "your-secret-key-change-this-in-production":
        print("⚠️  Warning: SECRET_KEY를 변경해주세요.") 