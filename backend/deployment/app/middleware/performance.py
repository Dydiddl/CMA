#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 성능 모니터링 미들웨어
"""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Any
import psutil
import asyncio

logger = logging.getLogger(__name__)

class PerformanceMiddleware(BaseHTTPMiddleware):
    """성능 모니터링 미들웨어"""
    
    def __init__(self, app, threshold_ms: float = 1000.0):
        super().__init__(app)
        self.threshold_ms = threshold_ms
        self.request_count = 0
        self.slow_requests = 0
        self.total_response_time = 0.0
    
    async def dispatch(self, request: Request, call_next):
        """요청 처리 및 성능 측정"""
        start_time = time.time()
        
        # 시스템 리소스 정보 수집
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        
        # 요청 처리
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000  # ms로 변환
            
            # 성능 지표 업데이트
            self.request_count += 1
            self.total_response_time += process_time
            
            # 느린 요청 감지
            if process_time > self.threshold_ms:
                self.slow_requests += 1
                logger.warning(
                    f"느린 요청 감지: {request.method} {request.url.path} - "
                    f"{process_time:.2f}ms (임계값: {self.threshold_ms}ms)"
                )
            
            # 성능 로그 기록
            logger.info(
                f"요청 처리 완료: {request.method} {request.url.path} - "
                f"상태코드: {response.status_code}, "
                f"처리시간: {process_time:.2f}ms, "
                f"CPU: {cpu_percent:.1f}%, "
                f"메모리: {memory_percent:.1f}%"
            )
            
            # 응답 헤더에 성능 정보 추가
            response.headers["X-Process-Time"] = f"{process_time:.2f}"
            response.headers["X-CPU-Usage"] = f"{cpu_percent:.1f}"
            response.headers["X-Memory-Usage"] = f"{memory_percent:.1f}"
            
            return response
            
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"요청 처리 실패: {request.method} {request.url.path} - "
                f"오류: {e}, 처리시간: {process_time:.2f}ms"
            )
            raise
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """성능 통계 반환"""
        avg_response_time = (
            self.total_response_time / self.request_count 
            if self.request_count > 0 else 0.0
        )
        
        slow_request_rate = (
            (self.slow_requests / self.request_count) * 100 
            if self.request_count > 0 else 0.0
        )
        
        return {
            "total_requests": self.request_count,
            "slow_requests": self.slow_requests,
            "average_response_time_ms": round(avg_response_time, 2),
            "slow_request_rate_percent": round(slow_request_rate, 2),
            "system_cpu_percent": psutil.cpu_percent(),
            "system_memory_percent": psutil.virtual_memory().percent,
            "system_disk_percent": psutil.disk_usage('/').percent
        }

class DatabasePerformanceMiddleware:
    """데이터베이스 성능 모니터링"""
    
    def __init__(self):
        self.query_count = 0
        self.total_query_time = 0.0
        self.slow_queries = []
    
    def record_query(self, query: str, execution_time: float):
        """쿼리 실행 시간 기록"""
        self.query_count += 1
        self.total_query_time += execution_time
        
        # 느린 쿼리 기록 (100ms 이상)
        if execution_time > 100:
            self.slow_queries.append({
                "query": query[:100] + "..." if len(query) > 100 else query,
                "execution_time": execution_time,
                "timestamp": time.time()
            })
            
            # 최근 100개만 유지
            if len(self.slow_queries) > 100:
                self.slow_queries = self.slow_queries[-100:]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """데이터베이스 성능 통계"""
        avg_query_time = (
            self.total_query_time / self.query_count 
            if self.query_count > 0 else 0.0
        )
        
        return {
            "total_queries": self.query_count,
            "average_query_time_ms": round(avg_query_time, 2),
            "slow_queries_count": len(self.slow_queries),
            "recent_slow_queries": self.slow_queries[-10:]  # 최근 10개
        }

# 전역 성능 모니터링 인스턴스
performance_middleware = None
database_middleware = DatabasePerformanceMiddleware()

def get_performance_middleware() -> PerformanceMiddleware:
    """성능 모니터링 미들웨어 반환"""
    global performance_middleware
    return performance_middleware

def set_performance_middleware(middleware: PerformanceMiddleware):
    """성능 모니터링 미들웨어 설정"""
    global performance_middleware
    performance_middleware = middleware

def get_database_middleware() -> DatabasePerformanceMiddleware:
    """데이터베이스 성능 모니터링 반환"""
    return database_middleware 