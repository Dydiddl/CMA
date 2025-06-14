from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./construction_management.db"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # 보안 설정
    SECRET_KEY: str = "your-secret-key"  # 실제 운영에서는 반드시 변경
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 서버 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "건설 관리 시스템"
    DEBUG: bool = True
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 캐시 설정
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 300  # 5분
    
    # 알림 설정
    NOTIFICATION_CLEANUP_DAYS: int = 30
    NOTIFICATION_BATCH_SIZE: int = 100
    
    # 성능 모니터링 설정
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 