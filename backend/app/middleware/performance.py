#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 모니터링 미들웨어
API 응답 시간, 메모리 사용량, CPU 사용률 등을 모니터링
"""

import time
import logging
import psutil
import asyncio
from typing import Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """성능 모니터링 클래스"""
    
    def __init__(self):
        self.metrics = {}
        self.alerts = []
        self.performance_thresholds = {
            "api_response_time": 1000,  # ms
            "memory_usage": 85,  # %
            "cpu_usage": 80,  # %
            "disk_usage": 90  # %
        }
    
    async def monitor_system_performance(self):
        """시스템 성능 모니터링"""
        while True:
            try:
                # CPU 사용률
                cpu_usage = psutil.cpu_percent()
                
                # 메모리 사용률
                memory_usage = psutil.virtual_memory().percent
                
                # 디스크 사용률
                disk_usage = psutil.disk_usage('/').percent
                
                # 성능 지표 저장
                self.metrics = {
                    'cpu_usage': cpu_usage,
                    'memory_usage': memory_usage,
                    'disk_usage': disk_usage,
                    'timestamp': time.time()
                }
                
                # 임계값 체크
                await self._check_thresholds()
                
                # 30초 대기
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"성능 모니터링 오류: {e}")
                await asyncio.sleep(30)
    
    async def _check_thresholds(self):
        """임계값 체크 및 알림"""
        if self.metrics['cpu_usage'] > self.performance_thresholds['cpu_usage']:
            await self._send_alert("CPU 사용률 높음", self.metrics['cpu_usage'])
        
        if self.metrics['memory_usage'] > self.performance_thresholds['memory_usage']:
            await self._send_alert("메모리 사용률 높음", self.metrics['memory_usage'])
        
        if self.metrics['disk_usage'] > self.performance_thresholds['disk_usage']:
            await self._send_alert("디스크 사용률 높음", self.metrics['disk_usage'])
    
    async def _send_alert(self, message: str, value: float):
        """알림 전송"""
        alert = {
            'message': message,
            'value': value,
            'timestamp': time.time()
        }
        self.alerts.append(alert)
        logger.warning(f"성능 알림: {message} - {value}%")
    
    def get_metrics(self) -> Dict[str, Any]:
        """현재 메트릭 반환"""
        return self.metrics
    
    def get_alerts(self) -> list:
        """알림 목록 반환"""
        return self.alerts

class PerformanceMiddleware(BaseHTTPMiddleware):
    """성능 모니터링 미들웨어"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.performance_monitor = PerformanceMonitor()
        self.request_count = 0
        self.error_count = 0
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        self.request_count += 1
        
        # 요청 처리
        try:
            response = await call_next(request)
            
            # 처리 시간 계산
            process_time = (time.time() - start_time) * 1000
            
            # 성능 임계값 체크
            if process_time > self.performance_monitor.performance_thresholds["api_response_time"]:
                logger.warning(f"느린 요청 감지: {request.method} {request.url.path} - {process_time:.3f}ms")
            
            # 로그 기록
            logger.info(
                f"요청 처리 완료: {request.method} {request.url.path} - "
                f"상태코드: {response.status_code}, "
                f"처리시간: {process_time:.3f}ms"
            )
            
            # 응답 헤더에 처리 시간 추가
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-Count"] = str(self.request_count)
            
            return response
            
        except Exception as e:
            self.error_count += 1
            process_time = (time.time() - start_time) * 1000
            
            logger.error(
                f"요청 처리 실패: {request.method} {request.url.path} - "
                f"오류: {e}, "
                f"처리시간: {process_time:.3f}ms"
            )
            
            # 오류 응답에도 헤더 추가
            response = Response(
                content=f"Internal Server Error: {str(e)}",
                status_code=500
            )
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-Count"] = str(self.request_count)
            response.headers["X-Error-Count"] = str(self.error_count)
            
            return response
    
    async def start_monitoring(self):
        """성능 모니터링 시작"""
        asyncio.create_task(self.performance_monitor.monitor_system_performance())
        logger.info("성능 모니터링이 시작되었습니다.")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """성능 통계 반환"""
        return {
            "metrics": self.performance_monitor.get_metrics(),
            "alerts": self.performance_monitor.get_alerts(),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        }

# 전역 성능 모니터 인스턴스
performance_monitor = PerformanceMonitor() 