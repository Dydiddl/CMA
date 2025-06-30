#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 최적화 핵심 모듈
Python 기반 성능 최적화를 위한 다양한 기법들을 제공합니다.
"""

import asyncio
import time
import functools
import logging
from typing import Any, Dict, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count
from functools import lru_cache
import psutil
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """성능 최적화 관리자"""
    
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=cpu_count())
        self.process_pool = ProcessPoolExecutor(max_workers=cpu_count())
        self.performance_metrics = {}
        self.optimization_history = []
    
    async def optimize_function(self, func: Callable, *args, **kwargs) -> Any:
        """함수 성능 최적화"""
        start_time = time.time()
        
        try:
            # 비동기 함수인 경우
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                # 동기 함수를 비동기로 실행
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(self.thread_pool, func, *args, **kwargs)
            
            execution_time = (time.time() - start_time) * 1000
            self._record_metric(func.__name__, execution_time)
            
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"함수 실행 실패: {func.__name__} - {execution_time:.2f}ms - {e}")
            raise
    
    def _record_metric(self, function_name: str, execution_time: float):
        """성능 메트릭 기록"""
        if function_name not in self.performance_metrics:
            self.performance_metrics[function_name] = []
        
        self.performance_metrics[function_name].append(execution_time)
        
        # 성능 임계값 체크
        if execution_time > 1000:  # 1초 이상
            logger.warning(f"느린 함수 감지: {function_name} - {execution_time:.2f}ms")
    
    async def process_large_data_parallel(self, data_chunks: List[Any], 
                                        processor_func: Callable) -> List[Any]:
        """대용량 데이터 병렬 처리"""
        loop = asyncio.get_event_loop()
        
        # CPU 집약적 작업을 프로세스 풀에서 실행
        tasks = [
            loop.run_in_executor(self.process_pool, processor_func, chunk)
            for chunk in data_chunks
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    def get_performance_report(self) -> Dict[str, Any]:
        """성능 리포트 생성"""
        report = {
            "summary": {},
            "slow_functions": [],
            "recommendations": []
        }
        
        for func_name, times in self.performance_metrics.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            
            report["summary"][func_name] = {
                "average_time": avg_time,
                "max_time": max_time,
                "min_time": min_time,
                "call_count": len(times)
            }
            
            # 느린 함수 식별
            if avg_time > 500:  # 500ms 이상
                report["slow_functions"].append({
                    "function": func_name,
                    "average_time": avg_time,
                    "recommendation": self._get_optimization_recommendation(func_name, avg_time)
                })
        
        return report
    
    def _get_optimization_recommendation(self, func_name: str, avg_time: float) -> str:
        """최적화 권장사항 생성"""
        if avg_time > 2000:
            return "Rust 전환 고려"
        elif avg_time > 1000:
            return "멀티프로세싱 도입"
        elif avg_time > 500:
            return "비동기 처리 도입"
        else:
            return "현재 성능 적절"


def measure_performance(func_name: Optional[str] = None):
    """성능 측정 데코레이터"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                logger.info(f"함수 실행: {func_name or func.__name__} - {duration:.2f}ms")
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                logger.error(f"함수 오류: {func_name or func.__name__} - {duration:.2f}ms - {e}")
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                logger.info(f"함수 실행: {func_name or func.__name__} - {duration:.2f}ms")
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                logger.error(f"함수 오류: {func_name or func.__name__} - {duration:.2f}ms - {e}")
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class MemoryOptimizer:
    """메모리 최적화 관리자"""
    
    def __init__(self):
        self.memory_usage = {}
    
    def monitor_memory(self, process_name: Optional[str] = None):
        """메모리 사용량 모니터링 데코레이터"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                process = psutil.Process()
                initial_memory = process.memory_info().rss / 1024 / 1024  # MB
                
                try:
                    result = func(*args, **kwargs)
                    final_memory = process.memory_info().rss / 1024 / 1024  # MB
                    memory_diff = final_memory - initial_memory
                    
                    self.memory_usage[func.__name__] = {
                        "initial": initial_memory,
                        "final": final_memory,
                        "difference": memory_diff
                    }
                    
                    if memory_diff > 100:  # 100MB 이상 증가
                        logger.warning(f"높은 메모리 사용: {func.__name__} - {memory_diff:.2f}MB 증가")
                    
                    return result
                except Exception as e:
                    logger.error(f"메모리 모니터링 중 오류: {func.__name__} - {e}")
                    raise
            
            return wrapper
        return decorator
    
    def get_memory_report(self) -> Dict[str, Any]:
        """메모리 사용량 리포트"""
        return {
            "current_usage": psutil.virtual_memory().percent,
            "function_memory": self.memory_usage,
            "recommendations": self._get_memory_recommendations()
        }
    
    def _get_memory_recommendations(self) -> List[str]:
        """메모리 최적화 권장사항"""
        recommendations = []
        
        for func_name, memory_info in self.memory_usage.items():
            if memory_info["difference"] > 200:  # 200MB 이상
                recommendations.append(f"{func_name}: 메모리 누수 가능성, 가비지 컬렉션 확인 필요")
            elif memory_info["difference"] > 100:  # 100MB 이상
                recommendations.append(f"{func_name}: 메모리 사용량 최적화 고려")
        
        return recommendations


class CacheManager:
    """캐싱 관리자"""
    
    def __init__(self):
        self.memory_cache = {}
        self.cache_stats = {}
    
    @lru_cache(maxsize=1000)
    def get_cached_result(self, key: str) -> Optional[Any]:
        """메모리 캐시에서 결과 가져오기"""
        return self.memory_cache.get(key)
    
    def set_cache(self, key: str, value: Any, ttl: int = 3600):
        """캐시 설정"""
        self.memory_cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }
        
        # 캐시 통계 업데이트
        if key not in self.cache_stats:
            self.cache_stats[key] = {"hits": 0, "misses": 0}
    
    def get_cache(self, key: str) -> Optional[Any]:
        """캐시에서 값 가져오기"""
        cached = self.memory_cache.get(key)
        
        if cached and time.time() < cached["expires_at"]:
            self.cache_stats[key]["hits"] += 1
            return cached["value"]
        else:
            if key in self.cache_stats:
                self.cache_stats[key]["misses"] += 1
            return None
    
    def clear_expired_cache(self):
        """만료된 캐시 정리"""
        current_time = time.time()
        expired_keys = [
            key for key, cached in self.memory_cache.items()
            if current_time >= cached["expires_at"]
        ]
        
        for key in expired_keys:
            del self.memory_cache[key]
        
        if expired_keys:
            logger.info(f"만료된 캐시 정리: {len(expired_keys)}개 항목")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계 반환"""
        return {
            "total_items": len(self.memory_cache),
            "stats": self.cache_stats,
            "hit_rate": self._calculate_hit_rate()
        }
    
    def _calculate_hit_rate(self) -> float:
        """캐시 히트율 계산"""
        total_hits = sum(stats["hits"] for stats in self.cache_stats.values())
        total_misses = sum(stats["misses"] for stats in self.cache_stats.values())
        total_requests = total_hits + total_misses
        
        if total_requests == 0:
            return 0.0
        
        return (total_hits / total_requests) * 100


# 전역 성능 최적화 인스턴스
performance_optimizer = PerformanceOptimizer()
memory_optimizer = MemoryOptimizer()
cache_manager = CacheManager()


# 사용 예시
@measure_performance("PDF 처리")
@memory_optimizer.monitor_memory()
async def process_pdf_optimized(pdf_path: str) -> Dict[str, Any]:
    """최적화된 PDF 처리 예시"""
    
    # 캐시 확인
    cache_key = f"pdf_processed:{pdf_path}"
    cached_result = cache_manager.get_cache(cache_key)
    if cached_result:
        return cached_result
    
    # 실제 처리 로직
    result = await performance_optimizer.optimize_function(
        _process_pdf_internal, pdf_path
    )
    
    # 결과 캐싱
    cache_manager.set_cache(cache_key, result, ttl=3600)
    
    return result


def _process_pdf_internal(pdf_path: str) -> Dict[str, Any]:
    """PDF 내부 처리 로직 (CPU 집약적 작업 시뮬레이션)"""
    # 실제 PDF 처리 로직이 여기에 들어갑니다
    time.sleep(0.1)  # 처리 시간 시뮬레이션
    return {"status": "success", "file": pdf_path} 