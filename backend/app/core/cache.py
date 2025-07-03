#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
캐싱 시스템
성능 최적화를 위한 메모리 캐시와 Redis 캐시 지원
"""

import json
import time
import logging
from typing import Any, Optional, Dict, Union
from functools import wraps
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

class MemoryCache:
    """메모리 캐시 클래스"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def get(self, key: str) -> Optional[Any]:
        """캐시에서 값 가져오기"""
        if key in self.cache:
            # 접근 시간 업데이트
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """캐시에 값 설정"""
        try:
            # 캐시 크기 제한 확인
            if len(self.cache) >= self.max_size:
                self._evict_oldest()
            
            self.cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
            self.access_times[key] = time.time()
            return True
        except Exception as e:
            logger.error(f"메모리 캐시 설정 실패: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """캐시에서 값 삭제"""
        try:
            if key in self.cache:
                del self.cache[key]
                del self.access_times[key]
                return True
            return False
        except Exception as e:
            logger.error(f"메모리 캐시 삭제 실패: {e}")
            return False
    
    def clear(self) -> bool:
        """캐시 전체 삭제"""
        try:
            self.cache.clear()
            self.access_times.clear()
            return True
        except Exception as e:
            logger.error(f"메모리 캐시 전체 삭제 실패: {e}")
            return False
    
    def _evict_oldest(self):
        """가장 오래된 항목 제거 (LRU)"""
        if not self.access_times:
            return
        
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        self.delete(oldest_key)
    
    def cleanup_expired(self):
        """만료된 항목 정리"""
        current_time = time.time()
        expired_keys = [
            key for key, data in self.cache.items()
            if data['expires_at'] < current_time
        ]
        
        for key in expired_keys:
            self.delete(key)

class RedisCache:
    """Redis 캐시 클래스"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """Redis 연결"""
        try:
            import redis
            self.redis_client = redis.from_url(self.redis_url)
            # 연결 테스트
            self.redis_client.ping()
            logger.info("Redis 연결 성공")
        except ImportError:
            logger.warning("Redis 라이브러리가 설치되지 않았습니다. 메모리 캐시만 사용합니다.")
            self.redis_client = None
        except Exception as e:
            logger.error(f"Redis 연결 실패: {e}")
            self.redis_client = None
    
    async def get(self, key: str) -> Optional[Any]:
        """Redis에서 값 가져오기"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis 캐시 조회 실패: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Redis에 값 설정"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = json.dumps(value, ensure_ascii=False)
            self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Redis 캐시 설정 실패: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Redis에서 값 삭제"""
        if not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Redis 캐시 삭제 실패: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> bool:
        """패턴에 맞는 키들 삭제"""
        if not self.redis_client:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Redis 패턴 삭제 실패: {e}")
            return False

class HybridCache:
    """하이브리드 캐싱 시스템"""
    
    def __init__(self, redis_url: Optional[str] = None):
        self.memory_cache = MemoryCache()
        self.redis_cache = RedisCache(redis_url) if redis_url else None
        self.use_redis = self.redis_cache and self.redis_cache.redis_client is not None
    
    async def get(self, key: str) -> Optional[Any]:
        """캐시에서 값 가져오기 (메모리 → Redis 순서)"""
        # 메모리 캐시에서 먼저 확인
        value = self.memory_cache.get(key)
        if value is not None:
            return value['value']
        
        # Redis에서 확인
        if self.use_redis:
            value = await self.redis_cache.get(key)
            if value is not None:
                # 메모리 캐시에도 저장
                self.memory_cache.set(key, value, ttl=300)  # 5분
                return value
        
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """캐시에 값 설정 (메모리 + Redis)"""
        success = True
        
        # 메모리 캐시에 저장
        if not self.memory_cache.set(key, value, ttl=min(ttl, 300)):  # 메모리는 최대 5분
            success = False
        
        # Redis에 저장
        if self.use_redis:
            if not await self.redis_cache.set(key, value, ttl):
                success = False
        
        return success
    
    async def delete(self, key: str) -> bool:
        """캐시에서 값 삭제"""
        success = True
        
        # 메모리 캐시에서 삭제
        if not self.memory_cache.delete(key):
            success = False
        
        # Redis에서 삭제
        if self.use_redis:
            if not await self.redis_cache.delete(key):
                success = False
        
        return success
    
    async def clear_pattern(self, pattern: str) -> bool:
        """패턴에 맞는 키들 삭제"""
        success = True
        
        # 메모리 캐시 전체 삭제 (패턴 매칭이 복잡하므로)
        if not self.memory_cache.clear():
            success = False
        
        # Redis에서 패턴 삭제
        if self.use_redis:
            if not await self.redis_cache.clear_pattern(pattern):
                success = False
        
        return success
    
    def cleanup(self):
        """캐시 정리"""
        self.memory_cache.cleanup_expired()

def cache_result(ttl: int = 3600, key_prefix: str = ""):
    """함수 결과 캐싱 데코레이터"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 캐시 키 생성
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 캐시에서 확인
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 함수 실행
            result = await func(*args, **kwargs)
            
            # 결과 캐싱
            await cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# 전역 캐시 매니저 인스턴스
cache_manager = HybridCache()

# 주기적 캐시 정리
async def cleanup_cache_periodically():
    """주기적으로 캐시 정리"""
    while True:
        try:
            # 메모리 캐시 정리
            memory_cache.cleanup_expired()
            
            # 1시간마다 실행
            await asyncio.sleep(3600)
        except Exception as e:
            logger.error(f"캐시 정리 중 오류: {e}")
            await asyncio.sleep(60)  # 오류 시 1분 후 재시도


# 전역 캐시 인스턴스
memory_cache = MemoryCache()
hybrid_cache = HybridCache()

class CacheKeys:
    """캐시 키 상수"""
    USER_PROFILE = "user_profile"
    DASHBOARD_STATS = "dashboard_stats"
    LABOR_STATS = "labor_stats"
    LABOR_LIST = "labor_list"
    LABOR_DETAIL = "labor_detail"
    LABOR_SUMMARY = "labor_summary"
    CONTRACT_STATS = "contract_stats"
    CONTRACT_LIST = "contract_list"
    CONTRACT_DETAIL = "contract_detail"
    FINANCIAL_STATS = "financial_stats"
    PROJECT_STATS = "project_stats"
    PROJECT_LIST = "project_list"
    PROJECT_DETAIL = "project_detail"
    VENDOR_STATS = "vendor_stats"
    VENDOR_LIST = "vendor_list"
    VENDOR_DETAIL = "vendor_detail"


def get_cache():
    """캐시 인스턴스 반환"""
    return hybrid_cache 