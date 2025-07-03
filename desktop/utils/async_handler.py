#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 비동기 처리 유틸리티
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Any, Optional, Dict
from functools import wraps

logger = logging.getLogger(__name__)


class AsyncHandler:
    """비동기 처리 핸들러"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=max_workers)
        self.loop = None
    
    def __del__(self):
        """소멸자 - 리소스 정리"""
        self.cleanup()
    
    def cleanup(self):
        """리소스 정리"""
        try:
            if self.thread_pool:
                self.thread_pool.shutdown(wait=True)
            if self.process_pool:
                self.process_pool.shutdown(wait=True)
        except Exception as e:
            logger.error(f"리소스 정리 실패: {e}")
    
    async def run_in_thread(self, func: Callable, *args, **kwargs) -> Any:
        """스레드 풀에서 함수 실행"""
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        
        try:
            result = await self.loop.run_in_executor(
                self.thread_pool, 
                self._run_with_logging, 
                func, 
                *args, 
                **kwargs
            )
            return result
        except Exception as e:
            logger.error(f"스레드 실행 실패: {e}")
            raise
    
    async def run_in_process(self, func: Callable, *args, **kwargs) -> Any:
        """프로세스 풀에서 함수 실행"""
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        
        try:
            result = await self.loop.run_in_executor(
                self.process_pool, 
                self._run_with_logging, 
                func, 
                *args, 
                **kwargs
            )
            return result
        except Exception as e:
            logger.error(f"프로세스 실행 실패: {e}")
            raise
    
    def _run_with_logging(self, func: Callable, *args, **kwargs) -> Any:
        """로깅과 함께 함수 실행"""
        try:
            logger.debug(f"함수 실행 시작: {func.__name__}")
            result = func(*args, **kwargs)
            logger.debug(f"함수 실행 완료: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"함수 실행 실패: {func.__name__} - {e}")
            raise


class PerformanceMonitor:
    """성능 모니터링 클래스"""
    
    def __init__(self):
        self.metrics: Dict[str, float] = {}
    
    async def monitor_performance(self, func_name: str, func: Callable, 
                                *args, **kwargs) -> Any:
        """성능 모니터링과 함께 함수 실행"""
        import time
        
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            # 성능 지표 저장
            self.metrics[func_name] = duration
            
            # 성능 임계값 체크 (1초 이상)
            if duration > 1.0:
                logger.warning(f"느린 함수 실행: {func_name} - {duration:.3f}초")
            else:
                logger.debug(f"함수 실행 완료: {func_name} - {duration:.3f}초")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"함수 실행 실패: {func_name} - {duration:.3f}초 - {e}")
            raise
    
    def get_performance_report(self) -> Dict[str, float]:
        """성능 보고서 반환"""
        return self.metrics.copy()
    
    def clear_metrics(self):
        """성능 지표 초기화"""
        self.metrics.clear()


def async_task(func: Callable) -> Callable:
    """비동기 작업 데코레이터"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        handler = AsyncHandler()
        try:
            return await handler.run_in_thread(func, *args, **kwargs)
        finally:
            handler.cleanup()
    return wrapper


def cpu_intensive_task(func: Callable) -> Callable:
    """CPU 집약적 작업 데코레이터"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        handler = AsyncHandler()
        try:
            return await handler.run_in_process(func, *args, **kwargs)
        finally:
            handler.cleanup()
    return wrapper


# 전역 인스턴스
async_handler = AsyncHandler()
performance_monitor = PerformanceMonitor() 