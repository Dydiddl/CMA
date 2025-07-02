#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 성능 최적화 스크립트
"""

import os
import sys
import time
import logging
import json
from typing import Dict, Any, List
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import engine, get_db
from app.core.cache import get_cache, clear_all_cache, get_cache_stats
from app.services.labor_service import LaborService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """성능 최적화 클래스"""
    
    def __init__(self):
        self.db = next(get_db())
        self.cache = get_cache()
        self.optimization_results = {}
    
    def optimize_database_connections(self) -> Dict[str, Any]:
        """데이터베이스 연결 최적화"""
        logger.info("데이터베이스 연결 최적화 시작")
        
        try:
            # 연결 풀 상태 확인
            pool_info = {
                "pool_size": engine.pool.size(),
                "checked_in": engine.pool.checkedin(),
                "checked_out": engine.pool.checkedout(),
                "overflow": engine.pool.overflow(),
                "invalid": engine.pool.invalid()
            }
            
            # 연결 풀 최적화 권장사항
            recommendations = []
            
            if pool_info["checked_out"] > pool_info["pool_size"] * 0.8:
                recommendations.append("연결 풀 크기 증가 권장")
            
            if pool_info["invalid"] > 0:
                recommendations.append("무효한 연결 정리 필요")
            
            result = {
                "current_pool_status": pool_info,
                "recommendations": recommendations,
                "optimization_applied": len(recommendations) == 0
            }
            
            logger.info("데이터베이스 연결 최적화 완료")
            return result
            
        except Exception as e:
            logger.error(f"데이터베이스 연결 최적화 실패: {e}")
            return {"error": str(e)}
    
    def optimize_cache_performance(self) -> Dict[str, Any]:
        """캐시 성능 최적화"""
        logger.info("캐시 성능 최적화 시작")
        
        try:
            # 캐시 통계 수집
            cache_stats = get_cache_stats()
            
            # 캐시 최적화 권장사항
            recommendations = []
            
            # 메모리 사용량 확인
            if cache_stats.get("used_memory", 0) > 100 * 1024 * 1024:  # 100MB
                recommendations.append("캐시 메모리 사용량 높음 - TTL 단축 권장")
            
            # 캐시 히트율 확인
            hits = cache_stats.get("keyspace_hits", 0)
            misses = cache_stats.get("keyspace_misses", 0)
            total_requests = hits + misses
            
            if total_requests > 0:
                hit_rate = (hits / total_requests) * 100
                if hit_rate < 50:
                    recommendations.append("캐시 히트율 낮음 - 캐시 전략 재검토 필요")
            else:
                hit_rate = 0
            
            # 캐시 정리 (필요한 경우)
            if len(recommendations) > 0:
                logger.info("캐시 정리 수행")
                clear_all_cache()
            
            result = {
                "cache_stats": cache_stats,
                "hit_rate_percent": round(hit_rate, 2),
                "recommendations": recommendations,
                "optimization_applied": len(recommendations) > 0
            }
            
            logger.info("캐시 성능 최적화 완료")
            return result
            
        except Exception as e:
            logger.error(f"캐시 성능 최적화 실패: {e}")
            return {"error": str(e)}
    
    def optimize_database_queries(self) -> Dict[str, Any]:
        """데이터베이스 쿼리 최적화"""
        logger.info("데이터베이스 쿼리 최적화 시작")
        
        try:
            # 느린 쿼리 분석
            slow_queries = self.db.execute("""
                SELECT 
                    query,
                    calls,
                    total_time,
                    mean_time,
                    rows
                FROM pg_stat_statements
                WHERE mean_time > 100  -- 100ms 이상
                ORDER BY mean_time DESC
                LIMIT 10
            """).fetchall()
            
            # 인덱스 사용 현황 분석
            index_usage = self.db.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes
                WHERE schemaname = 'public'
                ORDER BY idx_scan DESC
            """).fetchall()
            
            # 최적화 권장사항
            recommendations = []
            
            for query in slow_queries:
                if query.mean_time > 1000:  # 1초 이상
                    recommendations.append(f"매우 느린 쿼리 발견: {query.query[:100]}...")
            
            # 사용되지 않는 인덱스 확인
            unused_indexes = [idx for idx in index_usage if idx.idx_scan == 0]
            if unused_indexes:
                recommendations.append(f"사용되지 않는 인덱스 {len(unused_indexes)}개 발견")
            
            result = {
                "slow_queries": [dict(q) for q in slow_queries],
                "index_usage": [dict(idx) for idx in index_usage],
                "unused_indexes_count": len(unused_indexes),
                "recommendations": recommendations,
                "optimization_applied": len(recommendations) == 0
            }
            
            logger.info("데이터베이스 쿼리 최적화 완료")
            return result
            
        except Exception as e:
            logger.error(f"데이터베이스 쿼리 최적화 실패: {e}")
            return {"error": str(e)}
    
    def optimize_labor_service(self) -> Dict[str, Any]:
        """노무 서비스 최적화"""
        logger.info("노무 서비스 최적화 시작")
        
        try:
            labor_service = LaborService(self.db)
            
            # 성능 테스트 실행
            start_time = time.time()
            
            # 노무자 목록 조회 성능 테스트
            labor_list, total = labor_service.get_labor_records(skip=0, limit=100)
            list_query_time = (time.time() - start_time) * 1000
            
            # 요약 통계 성능 테스트
            start_time = time.time()
            summary = labor_service.get_labor_summary()
            summary_query_time = (time.time() - start_time) * 1000
            
            # 성능 분석
            recommendations = []
            
            if list_query_time > 500:  # 500ms 이상
                recommendations.append("노무자 목록 조회 성능 개선 필요")
            
            if summary_query_time > 1000:  # 1초 이상
                recommendations.append("노무 요약 통계 성능 개선 필요")
            
            result = {
                "list_query_time_ms": round(list_query_time, 2),
                "summary_query_time_ms": round(summary_query_time, 2),
                "total_labor_count": total,
                "recommendations": recommendations,
                "optimization_applied": len(recommendations) == 0
            }
            
            logger.info("노무 서비스 최적화 완료")
            return result
            
        except Exception as e:
            logger.error(f"노무 서비스 최적화 실패: {e}")
            return {"error": str(e)}
    
    def run_all_optimizations(self) -> Dict[str, Any]:
        """모든 최적화 실행"""
        logger.info("=== CMA 성능 최적화 시작 ===")
        
        all_results = {}
        
        try:
            # 1. 데이터베이스 연결 최적화
            logger.info("1. 데이터베이스 연결 최적화")
            all_results["database_connections"] = self.optimize_database_connections()
            
            # 2. 캐시 성능 최적화
            logger.info("2. 캐시 성능 최적화")
            all_results["cache_performance"] = self.optimize_cache_performance()
            
            # 3. 데이터베이스 쿼리 최적화
            logger.info("3. 데이터베이스 쿼리 최적화")
            all_results["database_queries"] = self.optimize_database_queries()
            
            # 4. 노무 서비스 최적화
            logger.info("4. 노무 서비스 최적화")
            all_results["labor_service"] = self.optimize_labor_service()
            
        except Exception as e:
            logger.error(f"성능 최적화 실행 중 오류: {e}")
            all_results["error"] = str(e)
        
        # 최적화 요약 생성
        all_results["summary"] = self._generate_optimization_summary(all_results)
        
        logger.info("=== CMA 성능 최적화 완료 ===")
        return all_results
    
    def _generate_optimization_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """최적화 요약 생성"""
        summary = {
            "optimization_timestamp": time.time(),
            "overall_status": "OPTIMIZED",
            "total_recommendations": 0,
            "optimizations_applied": 0,
            "performance_improvements": []
        }
        
        total_recommendations = 0
        optimizations_applied = 0
        
        for category, result in results.items():
            if isinstance(result, dict) and "recommendations" in result:
                recommendations = result.get("recommendations", [])
                total_recommendations += len(recommendations)
                
                if result.get("optimization_applied", False):
                    optimizations_applied += 1
                    summary["performance_improvements"].append(category)
        
        summary["total_recommendations"] = total_recommendations
        summary["optimizations_applied"] = optimizations_applied
        
        # 전체 상태 결정
        if total_recommendations > 5:
            summary["overall_status"] = "NEEDS_ATTENTION"
        elif total_recommendations > 0:
            summary["overall_status"] = "PARTIALLY_OPTIMIZED"
        
        return summary


def main():
    """메인 실행 함수"""
    logger.info("CMA 성능 최적화 스크립트 시작")
    
    try:
        # 성능 최적화 실행
        optimizer = PerformanceOptimizer()
        results = optimizer.run_all_optimizations()
        
        # 결과 출력
        print("\n" + "="*60)
        print("CMA 성능 최적화 결과")
        print("="*60)
        
        # 요약 출력
        summary = results.get("summary", {})
        print(f"전체 상태: {summary.get('overall_status', 'UNKNOWN')}")
        print(f"최적화 적용: {summary.get('optimizations_applied', 0)}개")
        print(f"권장사항: {summary.get('total_recommendations', 0)}개")
        
        # 성능 개선 사항 출력
        improvements = summary.get("performance_improvements", [])
        if improvements:
            print(f"성능 개선 적용 영역: {', '.join(improvements)}")
        
        # 상세 결과 출력
        for category, result in results.items():
            if category != "summary" and isinstance(result, dict):
                print(f"\n{category.upper()}:")
                if "recommendations" in result:
                    recommendations = result.get("recommendations", [])
                    if recommendations:
                        print("  권장사항:")
                        for rec in recommendations:
                            print(f"    - {rec}")
                    else:
                        print("  최적화 완료")
        
        print("="*60)
        
        # 결과를 파일로 저장
        output_file = "performance_optimization_results.json"
        with open(output_file, "w", encoding="utf-8", newline='', encoding='utf-8', newline='') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"성능 최적화 결과가 {output_file}에 저장되었습니다.")
        
        return results
        
    except Exception as e:
        logger.error(f"성능 최적화 스크립트 실행 실패: {e}")
        raise


if __name__ == "__main__":
    main() 