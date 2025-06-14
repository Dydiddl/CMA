import redis
from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings

# Redis 연결
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

def add_to_blacklist(token: str, expires_delta: Optional[timedelta] = None) -> None:
    """
    토큰을 블랙리스트에 추가합니다.
    """
    if expires_delta:
        expire_seconds = int(expires_delta.total_seconds())
    else:
        expire_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    redis_client.setex(
        f"blacklist:{token}",
        expire_seconds,
        str(datetime.utcnow().timestamp())
    )

def is_blacklisted(token: str) -> bool:
    """
    토큰이 블랙리스트에 있는지 확인합니다.
    """
    return bool(redis_client.exists(f"blacklist:{token}"))

def remove_from_blacklist(token: str) -> None:
    """
    토큰을 블랙리스트에서 제거합니다.
    """
    redis_client.delete(f"blacklist:{token}")

def clear_expired_blacklist() -> None:
    """
    만료된 블랙리스트 항목을 제거합니다.
    """
    # Redis의 자동 만료 기능을 사용하므로 별도의 작업이 필요하지 않습니다.
    pass 