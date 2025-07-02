#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 전체 시스템 통합 테스트 스위트
"""

import os
import sys
import time
import json
import logging
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.database import get_db, create_tables
from app.core.cache import get_cache, clear_all_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegrationTestSuite:
    """통합 테스트 스위트"""
    
    def __init__(self):
        self.client = TestClient(app)
        self.db = next(get_db())
        self.cache = get_cache()
        self.test_results = {}
        self.start_time = time.time()
    
    def setup_test_environment(self):
        """테스트 환경 설정"""
        logger.info("테스트 환경 설정 시작")
        
        try:
            # 데이터베이스 테이블 생성
            create_tables()
            logger.info("데이터베이스 테이블 생성 완료")
            
            # 캐시 정리
            clear_all_cache()
            logger.info("캐시 정리 완료")
            
        except Exception as e:
            logger.error(f"테스트 환경 설정 실패: {e}")
            raise
    
    def test_database_connectivity(self) -> Dict[str, Any]:
        """데이터베이스 연결 테스트"""
        logger.info("데이터베이스 연결 테스트 시작")
        
        try:
            # 연결 테스트
            result = self.db.execute("SELECT 1").fetchone()
            
            if result and result[0] == 1:
                return {
                    "status": "SUCCESS",
                    "message": "데이터베이스 연결 성공"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": "데이터베이스 연결 실패"
                }
                
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "데이터베이스 연결 실패",
                "error": str(e)
            }
    
    def test_cache_functionality(self) -> Dict[str, Any]:
        """캐시 기능 테스트"""
        logger.info("캐시 기능 테스트 시작")
        
        try:
            # 캐시 설정 테스트
            test_key = "test:cache:key"
            test_value = {"test": "data", "timestamp": time.time()}
            
            # 캐시 설정
            self.cache.setex(test_key, 60, json.dumps(test_value))
            
            # 캐시 조회
            cached_value = self.cache.get(test_key)
            
            if cached_value:
                parsed_value = json.loads(cached_value)
                if parsed_value["test"] == test_value["test"]:
                    return {
                        "status": "SUCCESS",
                        "message": "캐시 기능 정상"
                    }
            
            return {
                "status": "FAILED",
                "message": "캐시 기능 테스트 실패"
            }
            
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "캐시 기능 테스트 실패",
                "error": str(e)
            }
    
    def test_api_endpoints(self) -> Dict[str, Any]:
        """API 엔드포인트 테스트"""
        logger.info("API 엔드포인트 테스트 시작")
        
        test_results = {}
        
        # 1. 루트 엔드포인트 테스트
        try:
            response = self.client.get("/")
            test_results["root_endpoint"] = {
                "status": "SUCCESS" if response.status_code == 200 else "FAILED",
                "status_code": response.status_code
            }
        except Exception as e:
            test_results["root_endpoint"] = {
                "status": "FAILED",
                "error": str(e)
            }
        
        # 2. 헬스 체크 엔드포인트 테스트
        try:
            response = self.client.get("/health")
            test_results["health_check"] = {
                "status": "SUCCESS" if response.status_code == 200 else "FAILED",
                "status_code": response.status_code
            }
        except Exception as e:
            test_results["health_check"] = {
                "status": "FAILED",
                "error": str(e)
            }
        
        # 3. 성능 통계 엔드포인트 테스트
        try:
            response = self.client.get("/performance/stats")
            test_results["performance_stats"] = {
                "status": "SUCCESS" if response.status_code == 200 else "FAILED",
                "status_code": response.status_code
            }
        except Exception as e:
            test_results["performance_stats"] = {
                "status": "FAILED",
                "error": str(e)
            }
        
        return test_results
    
    def test_performance_benchmarks(self) -> Dict[str, Any]:
        """성능 벤치마크 테스트"""
        logger.info("성능 벤치마크 테스트 시작")
        
        benchmarks = {}
        
        # API 응답 시간 벤치마크
        api_endpoints = ["/", "/health", "/performance/stats"]
        
        for endpoint in api_endpoints:
            response_times = []
            
            for _ in range(3):  # 3회 테스트
                start_time = time.time()
                try:
                    response = self.client.get(endpoint)
                    response_time = (time.time() - start_time) * 1000
                    response_times.append(response_time)
                except Exception:
                    response_times.append(9999)
            
            avg_response_time = sum(response_times) / len(response_times)
            benchmarks[f"api_{endpoint.replace('/', '_')}"] = {
                "average_response_time_ms": round(avg_response_time, 2),
                "performance_grade": "EXCELLENT" if avg_response_time < 100 else "GOOD" if avg_response_time < 500 else "POOR"
            }
        
        return benchmarks
    
    def run_all_tests(self) -> Dict[str, Any]:
        """모든 테스트 실행"""
        logger.info("=== CMA 통합 테스트 시작 ===")
        
        all_results = {
            "test_timestamp": datetime.now().isoformat(),
            "test_duration_seconds": 0
        }
        
        try:
            # 테스트 환경 설정
            self.setup_test_environment()
            
            # 1. 데이터베이스 연결 테스트
            logger.info("1. 데이터베이스 연결 테스트")
            all_results["database_connectivity"] = self.test_database_connectivity()
            
            # 2. 캐시 기능 테스트
            logger.info("2. 캐시 기능 테스트")
            all_results["cache_functionality"] = self.test_cache_functionality()
            
            # 3. API 엔드포인트 테스트
            logger.info("3. API 엔드포인트 테스트")
            all_results["api_endpoints"] = self.test_api_endpoints()
            
            # 4. 성능 벤치마크 테스트
            logger.info("4. 성능 벤치마크 테스트")
            all_results["performance_benchmarks"] = self.test_performance_benchmarks()
            
        except Exception as e:
            logger.error(f"통합 테스트 실행 중 오류: {e}")
            all_results["error"] = str(e)
        
        # 테스트 요약 생성
        all_results["test_duration_seconds"] = round(time.time() - self.start_time, 2)
        all_results["summary"] = self._generate_test_summary(all_results)
        
        logger.info("=== CMA 통합 테스트 완료 ===")
        return all_results
    
    def _generate_test_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """테스트 요약 생성"""
        summary = {
            "overall_status": "PASSED",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "performance_issues": []
        }
        
        # 각 테스트 카테고리별 결과 분석
        test_categories = [
            "database_connectivity",
            "cache_functionality",
            "api_endpoints",
            "performance_benchmarks"
        ]
        
        for category in test_categories:
            if category in results:
                category_result = results[category]
                
                if isinstance(category_result, dict):
                    if "status" in category_result:
                        summary["total_tests"] += 1
                        if category_result["status"] == "SUCCESS":
                            summary["passed_tests"] += 1
                        else:
                            summary["failed_tests"] += 1
                    
                    elif isinstance(category_result, dict):
                        # 하위 테스트가 있는 경우
                        for test_name, test_result in category_result.items():
                            summary["total_tests"] += 1
                            if test_result.get("status") == "SUCCESS":
                                summary["passed_tests"] += 1
                            else:
                                summary["failed_tests"] += 1
        
        # 성능 이슈 확인
        if "performance_benchmarks" in results:
            benchmarks = results["performance_benchmarks"]
            for benchmark_name, benchmark_result in benchmarks.items():
                if benchmark_result.get("performance_grade") == "POOR":
                    summary["performance_issues"].append(f"{benchmark_name}: {benchmark_result.get('average_response_time_ms', 'N/A')}ms")
        
        # 전체 상태 결정
        if summary["failed_tests"] > 0:
            summary["overall_status"] = "FAILED"
        elif len(summary["performance_issues"]) > 2:
            summary["overall_status"] = "PERFORMANCE_ISSUES"
        
        return summary


def main():
    """메인 실행 함수"""
    logger.info("CMA 통합 테스트 스위트 시작")
    
    try:
        # 통합 테스트 실행
        test_suite = IntegrationTestSuite()
        results = test_suite.run_all_tests()
        
        # 결과 출력
        print("\n" + "="*60)
        print("CMA 통합 테스트 결과")
        print("="*60)
        
        # 요약 출력
        summary = results.get("summary", {})
        print(f"전체 상태: {summary.get('overall_status', 'UNKNOWN')}")
        print(f"테스트 실행 시간: {results.get('test_duration_seconds', 0)}초")
        print(f"총 테스트: {summary.get('total_tests', 0)}개")
        print(f"성공: {summary.get('passed_tests', 0)}개")
        print(f"실패: {summary.get('failed_tests', 0)}개")
        
        # 성능 이슈 출력
        performance_issues = summary.get("performance_issues", [])
        if performance_issues:
            print(f"\n성능 이슈 ({len(performance_issues)}개):")
            for issue in performance_issues:
                print(f"  - {issue}")
        
        print("="*60)
        
        # 결과를 파일로 저장
        output_file = "integration_test_results.json"
        with open(output_file, "w", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"통합 테스트 결과가 {output_file}에 저장되었습니다.")
        
        # 테스트 결과에 따른 종료 코드
        if summary.get("overall_status") == "PASSED":
            sys.exit(0)
        else:
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"통합 테스트 스위트 실행 실패: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 