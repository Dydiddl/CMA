"""
애플리케이션 설정 모듈
"""
import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

print(f"POSTGRES_SERVER: {os.environ.get('POSTGRES_SERVER')}")
print(f"POSTGRES_USER: {os.environ.get('POSTGRES_USER')}")
print(f"POSTGRES_PASSWORD: {os.environ.get('POSTGRES_PASSWORD')}")
print(f"POSTGRES_DB: {os.environ.get('POSTGRES_DB')}")

class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Construction Management API"
    VERSION: str = "1.0.0"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "http://localhost:8000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 데이터베이스 설정 (개발 환경에서는 SQLite 사용)
    USE_LOCAL_DB: bool = True
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "construction_management")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # 샤딩 설정
    ENABLE_SHARDING: bool = os.getenv("ENABLE_SHARDING", "false").lower() == "true"
    SHARD_1_DB: str = os.getenv("SHARD_1_DB", "construction_management_shard1")
    SHARD_2_DB: str = os.getenv("SHARD_2_DB", "construction_management_shard2")
    SHARD_1_DATABASE_URI: Optional[str] = None
    SHARD_2_DATABASE_URI: Optional[str] = None

    # 데이터베이스 성능 설정
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))
    SLOW_QUERY_THRESHOLD: float = float(os.getenv("SLOW_QUERY_THRESHOLD", "0.5"))

    # Excel 처리 설정
    MAX_EXCEL_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXCEL_EXTENSIONS: set = {".xlsx", ".xls"}
    EXCEL_TEMP_DIR: str = "temp/excel"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 개발 환경에서는 SQLite 사용
        if self.USE_LOCAL_DB:
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///./construction_management.db"
        else:
            # PostgreSQL 사용
            if not self.SQLALCHEMY_DATABASE_URI:
                self.SQLALCHEMY_DATABASE_URI = (
                    f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                    f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
                )
        
        # 샤드 데이터베이스 URI 설정
        if self.ENABLE_SHARDING:
            if self.USE_LOCAL_DB:
                self.SHARD_1_DATABASE_URI = "sqlite:///./construction_management_shard1.db"
                self.SHARD_2_DATABASE_URI = "sqlite:///./construction_management_shard2.db"
            else:
                self.SHARD_1_DATABASE_URI = (
                    f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                    f"@{self.POSTGRES_SERVER}/{self.SHARD_1_DB}"
                )
                self.SHARD_2_DATABASE_URI = (
                    f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                    f"@{self.POSTGRES_SERVER}/{self.SHARD_2_DB}"
                )

    # JWT 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        case_sensitive = True
        env_file = ".env"

# 설정 인스턴스 생성
settings = Settings() 