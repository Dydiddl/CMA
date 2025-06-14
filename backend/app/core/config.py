from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, validator
import os
from pathlib import Path
from functools import lru_cache
import secrets
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    환경변수와 기본값을 통해 설정을 관리합니다.
    """
    
    # 프로젝트 기본 정보
    PROJECT_NAME: str = "CMA"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = "건설회사 관리 시스템 API"
    
    # 환경 설정
    ENV: str = os.getenv("ENV", "development")
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # 데이터베이스 설정
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # sqlite, postgresql
    DB_HOST: Optional[str] = os.getenv("DB_HOST", "localhost")
    DB_PORT: Optional[str] = os.getenv("DB_PORT", "5432")
    DB_USER: Optional[str] = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "construction_management")
    
    # SQLite 설정
    SQLALCHEMY_DATABASE_URI: str = None
    
    # Redis 설정
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    
    # JWT 설정
    SECRET_KEY: str
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
    LOG_FILE: str = "logs/app.log"
    
    # 보안 설정
    BCRYPT_ROUNDS: int = 12
    
    # 애플리케이션 경로 설정
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # 데이터베이스 파일 경로 설정
    @property
    def db_path(self) -> Path:
        """데이터베이스 파일 경로 반환"""
        if self.ENV == "development":
            return self.BASE_DIR / self.SQLALCHEMY_DATABASE_URI.split("///")[1]
        elif self.ENV == "test":
            return self.BASE_DIR / "test.db"
        else:
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
        return self.ENV == "development"
    
    def get_database_url(self) -> str:
        """사용할 데이터베이스 URL 반환"""
        if self.ENV == "development":
            return self.SQLALCHEMY_DATABASE_URI
        elif self.ENV == "test":
            return "sqlite:///./test.db"
        else:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def get_redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    def get_cors_config(self) -> dict:
        """CORS 설정 반환"""
        return {
            "allow_origins": self.ALLOWED_ORIGINS,
            "allow_methods": self.ALLOWED_METHODS,
            "allow_headers": self.ALLOWED_HEADERS,
            "allow_credentials": self.ALLOW_CREDENTIALS
        }
    
    # 추가된 필드
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 이메일 설정
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str
    EMAILS_FROM_NAME: str

    # API 문서화 설정
    API_DOCS_TITLE: str = "CMA API Documentation"
    API_DOCS_DESCRIPTION: str = "CMA 프로젝트의 API 문서입니다."
    API_DOCS_VERSION: str = "1.0.0"
    API_DOCS_TERMS_OF_SERVICE: str = "http://example.com/terms/"
    API_DOCS_CONTACT_NAME: str = "CMA Team"
    API_DOCS_CONTACT_URL: str = "http://example.com/contact/"
    API_DOCS_CONTACT_EMAIL: str = "contact@example.com"
    API_DOCS_LICENSE_NAME: str = "MIT"
    API_DOCS_LICENSE_URL: str = "http://example.com/license/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# 개발 환경에서 설정 검증
if settings.is_development:
    if settings.ENV == "development":
        print(f"🗄️  로컬 SQLite 데이터베이스 사용: {settings.db_path}")
    else:
        if not settings.DB_HOST:
            print("⚠️  Warning: DB_HOST가 설정되지 않았습니다.")
        if not settings.DB_PORT:
            print("⚠️  Warning: DB_PORT가 설정되지 않았습니다.")
    
    if settings.SECRET_KEY == "your-secret-key-here":
        print("⚠️  Warning: SECRET_KEY를 변경해주세요.") 