#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 최적화 테스트 스크립트
Python 기반 성능 최적화 기법들을 테스트합니다.
"""

import asyncio
import time
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.core.performance_optimizer import (
    performance_optimizer, 
    memory_optimizer, 
    cache_manager,
    measure_performance
)


# 전역 함수로 정의 (멀티프로세싱용)
def process_chunk(chunk):
    """청크 처리 함수 (멀티프로세싱용)"""
    time.sleep(0.1)  # 처리 시간 시뮬레이션
    return sum(chunk)


@measure_performance("테스트 함수")
async def test_function_sync():
    """동기 함수 테스트"""
    time.sleep(0.1)  # 100ms 시뮬레이션
    return {"status": "success", "type": "sync"}


@measure_performance("비동기 테스트 함수")
async def test_function_async():
    """비동기 함수 테스트"""
    await asyncio.sleep(0.1)  # 100ms 시뮬레이션
    return {"status": "success", "type": "async"}


@memory_optimizer.monitor_memory()
def test_memory_intensive_function():
    """메모리 집약적 함수 테스트"""
    # 대용량 데이터 생성 시뮬레이션
    large_data = [i for i in range(1000000)]  # 약 8MB
    result = sum(large_data)
    return {"result": result, "data_size": len(large_data)}


async def test_cache_performance():
    """캐시 성능 테스트"""
    print("\n=== 캐시 성능 테스트 ===")
    
    # 캐시 설정
    cache_manager.set_cache("test_key", "test_value", ttl=60)
    
    # 캐시 히트 테스트
    start_time = time.time()
    for _ in range(1000):
        cache_manager.get_cache("test_key")
    cache_time = (time.time() - start_time) * 1000
    
    print(f"캐시 접근 1000회: {cache_time:.2f}ms")
    
    # 캐시 통계 확인
    stats = cache_manager.get_cache_stats()
    print(f"캐시 히트율: {stats['hit_rate']:.2f}%")


async def test_parallel_processing():
    """병렬 처리 테스트"""
    print("\n=== 병렬 처리 테스트 ===")
    
    # 테스트 데이터 생성
    data_chunks = [[i, i+1, i+2] for i in range(0, 30, 3)]
    
    # 순차 처리
    start_time = time.time()
    sequential_results = []
    for chunk in data_chunks:
        result = process_chunk(chunk)
        sequential_results.append(result)
    sequential_time = (time.time() - start_time) * 1000
    
    # 병렬 처리 (스레드 풀 사용)
    start_time = time.time()
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(performance_optimizer.thread_pool, process_chunk, chunk)
        for chunk in data_chunks
    ]
    parallel_results = await asyncio.gather(*tasks)
    parallel_time = (time.time() - start_time) * 1000
    
    print(f"순차 처리 시간: {sequential_time:.2f}ms")
    print(f"병렬 처리 시간: {parallel_time:.2f}ms")
    print(f"성능 향상: {sequential_time/parallel_time:.2f}배")


async def test_memory_optimization():
    """메모리 최적화 테스트"""
    print("\n=== 메모리 최적화 테스트 ===")
    
    # 메모리 집약적 함수 실행
    test_memory_intensive_function()
    
    # 메모리 리포트 확인
    memory_report = memory_optimizer.get_memory_report()
    print(f"현재 메모리 사용률: {memory_report['current_usage']:.2f}%")
    
    for func_name, memory_info in memory_report['function_memory'].items():
        print(f"{func_name}: {memory_info['difference']:.2f}MB 증가")
    
    if memory_report['recommendations']:
        print("\n메모리 최적화 권장사항:")
        for rec in memory_report['recommendations']:
            print(f"- {rec}")


async def test_performance_monitoring():
    """성능 모니터링 테스트"""
    print("\n=== 성능 모니터링 테스트 ===")
    
    # 여러 함수 실행
    for i in range(5):
        await test_function_sync()
        await test_function_async()
    
    # 성능 리포트 생성
    performance_report = performance_optimizer.get_performance_report()
    
    print("성능 요약:")
    for func_name, metrics in performance_report['summary'].items():
        print(f"{func_name}:")
        print(f"  평균 시간: {metrics['average_time']:.2f}ms")
        print(f"  최대 시간: {metrics['max_time']:.2f}ms")
        print(f"  최소 시간: {metrics['min_time']:.2f}ms")
        print(f"  호출 횟수: {metrics['call_count']}")
    
    if performance_report['slow_functions']:
        print("\n느린 함수 목록:")
        for slow_func in performance_report['slow_functions']:
            print(f"- {slow_func['function']}: {slow_func['average_time']:.2f}ms")
            print(f"  권장사항: {slow_func['recommendation']}")


async def main():
    """메인 테스트 함수"""
    print("🚀 CMA 성능 최적화 테스트 시작")
    print("=" * 50)
    
    try:
        # 1. 캐시 성능 테스트
        await test_cache_performance()
        
        # 2. 병렬 처리 테스트
        await test_parallel_processing()
        
        # 3. 메모리 최적화 테스트
        await test_memory_optimization()
        
        # 4. 성능 모니터링 테스트
        await test_performance_monitoring()
        
        print("\n" + "=" * 50)
        print("✅ 모든 성능 테스트 완료")
        
        # 최종 성능 리포트
        print("\n📊 최종 성능 리포트:")
        performance_report = performance_optimizer.get_performance_report()
        memory_report = memory_optimizer.get_memory_report()
        cache_stats = cache_manager.get_cache_stats()
        
        print(f"총 함수 실행 횟수: {sum(metrics['call_count'] for metrics in performance_report['summary'].values())}")
        print(f"캐시 히트율: {cache_stats['hit_rate']:.2f}%")
        print(f"메모리 사용률: {memory_report['current_usage']:.2f}%")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 비동기 테스트 실행
    asyncio.run(main()) 