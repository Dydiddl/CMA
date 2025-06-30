#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 캐시 설정
"""

import redis
import json
import os
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

# Redis 연결 설정
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Redis 클라이언트 (성능 최적화)
redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
    health_check_interval=30
)

class CacheKeys:
    """캐시 키 상수"""
    LABOR_LIST = "labor:list"
    LABOR_DETAIL = "labor:detail"
    LABOR_COUNT = "labor:count"
    LABOR_SUMMARY = "labor:summary"
    CONTRACT_LIST = "contract:list"
    CONTRACT_DETAIL = "contract:detail"
    FINANCIAL_LIST = "financial:list"
    FINANCIAL_DETAIL = "financial:detail"

def get_cache() -> redis.Redis:
    """Redis 캐시 클라이언트 반환"""
    return redis_client

def set_cache(key: str, value: Any, ttl: int = 3600) -> bool:
    """캐시 설정"""
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        redis_client.setex(key, ttl, value)
        return True
    except Exception as e:
        logger.error(f"캐시 설정 실패: {e}")
        return False

def get_cache_value(key: str) -> Optional[Any]:
    """캐시 값 조회"""
    try:
        value = redis_client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    except Exception as e:
        logger.error(f"캐시 조회 실패: {e}")
        return None

def delete_cache(key: str) -> bool:
    """캐시 삭제"""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"캐시 삭제 실패: {e}")
        return False

def delete_pattern(pattern: str) -> bool:
    """패턴으로 캐시 삭제"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        logger.error(f"패턴 캐시 삭제 실패: {e}")
        return False

def clear_all_cache() -> bool:
    """모든 캐시 삭제"""
    try:
        redis_client.flushdb()
        return True
    except Exception as e:
        logger.error(f"전체 캐시 삭제 실패: {e}")
        return False

def get_cache_stats() -> dict:
    """캐시 통계 조회"""
    try:
        info = redis_client.info()
        return {
            "used_memory": info.get("used_memory", 0),
            "used_memory_human": info.get("used_memory_human", "0B"),
            "connected_clients": info.get("connected_clients", 0),
            "total_commands_processed": info.get("total_commands_processed", 0),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0)
        }
    except Exception as e:
        logger.error(f"캐시 통계 조회 실패: {e}")
        return {} 