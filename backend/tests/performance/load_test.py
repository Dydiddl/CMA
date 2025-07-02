#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 성능 부하 테스트
"""

import time
import json
import logging
import asyncio
import aiohttp
from typing import Dict, Any, List
from datetime import datetime
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoadTest:
    """성능 부하 테스트 클래스"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}
        self.start_time = time.time()
    
    async def test_endpoint(self, endpoint: str, concurrent_users: int, duration_seconds: int) -> Dict[str, Any]:
        """특정 엔드포인트 부하 테스트"""
        logger.info(f"부하 테스트 시작: {endpoint} - {concurrent_users}명 동시 사용자, {duration_seconds}초")
        
        response_times = []
        success_count = 0
        error_count = 0
        start_time = time.time()
        
        async def make_request():
            """단일 요청 수행"""
            try:
                async with aiohttp.ClientSession() as session:
                    request_start = time.time()
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        request_time = (time.time() - request_start) * 1000
                        response_times.append(request_time)
                        
                        if response.status == 200:
                            return "SUCCESS"
                        else:
                            return f"HTTP_{response.status}"
            except Exception as e:
                return f"ERROR_{str(e)}"
        
        # 동시 요청 생성
        tasks = []
        for _ in range(concurrent_users):
            task = asyncio.create_task(make_request())
            tasks.append(task)
        
        # 요청 실행
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 결과 분석
        for result in results:
            if result == "SUCCESS":
                success_count += 1
            else:
                error_count += 1
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        # 통계 계산
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            median_response_time = statistics.median(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else max_response_time
        else:
            avg_response_time = min_response_time = max_response_time = median_response_time = p95_response_time = 0
        
        # 성능 등급 결정
        if avg_response_time < 100:
            performance_grade = "EXCELLENT"
        elif avg_response_time < 500:
            performance_grade = "GOOD"
        elif avg_response_time < 1000:
            performance_grade = "FAIR"
        else:
            performance_grade = "POOR"
        
        return {
            "endpoint": endpoint,
            "concurrent_users": concurrent_users,
            "duration_seconds": actual_duration,
            "total_requests": len(response_times),
            "success_count": success_count,
            "error_count": error_count,
            "success_rate": (success_count / len(response_times)) * 100 if response_times else 0,
            "avg_response_time_ms": round(avg_response_time, 2),
            "min_response_time_ms": round(min_response_time, 2),
            "max_response_time_ms": round(max_response_time, 2),
            "median_response_time_ms": round(median_response_time, 2),
            "p95_response_time_ms": round(p95_response_time, 2),
            "requests_per_second": len(response_times) / actual_duration if actual_duration > 0 else 0,
            "performance_grade": performance_grade
        }
    
    async def run_load_tests(self) -> Dict[str, Any]:
        """모든 부하 테스트 실행"""
        logger.info("=== CMA 성능 부하 테스트 시작 ===")
        
        test_scenarios = [
            # (엔드포인트, 동시 사용자 수, 테스트 시간)
            ("/", 10, 30),
            ("/health", 20, 30),
            ("/performance/stats", 5, 30),
            ("/api/v1/contracts/", 15, 30),
            ("/api/v1/financial/", 15, 30),
            ("/api/v1/labor/", 15, 30)
        ]
        
        all_results = {
            "test_timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "scenarios": {}
        }
        
        for endpoint, concurrent_users, duration in test_scenarios:
            try:
                result = await self.test_endpoint(endpoint, concurrent_users, duration)
                all_results["scenarios"][f"{endpoint}_{concurrent_users}users"] = result
                
                # 결과 출력
                print(f"\n{endpoint} - {concurrent_users}명 동시 사용자:")
                print(f"  성공률: {result['success_rate']:.1f}%")
                print(f"  평균 응답시간: {result['avg_response_time_ms']:.2f}ms")
                print(f"  초당 요청수: {result['requests_per_second']:.1f}")
                print(f"  성능 등급: {result['performance_grade']}")
                
            except Exception as e:
                logger.error(f"부하 테스트 실패 {endpoint}: {e}")
                all_results["scenarios"][f"{endpoint}_{concurrent_users}users"] = {
                    "error": str(e),
                    "status": "FAILED"
                }
        
        # 전체 요약 생성
        all_results["summary"] = self._generate_load_test_summary(all_results)
        all_results["test_duration_seconds"] = round(time.time() - self.start_time, 2)
        
        logger.info("=== CMA 성능 부하 테스트 완료 ===")
        return all_results
    
    def _generate_load_test_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """부하 테스트 요약 생성"""
        summary = {
            "overall_performance": "EXCELLENT",
            "total_scenarios": 0,
            "passed_scenarios": 0,
            "failed_scenarios": 0,
            "performance_issues": [],
            "recommendations": []
        }
        
        scenarios = results.get("scenarios", {})
        summary["total_scenarios"] = len(scenarios)
        
        performance_grades = []
        
        for scenario_name, scenario_result in scenarios.items():
            if "error" in scenario_result:
                summary["failed_scenarios"] += 1
                continue
            
            summary["passed_scenarios"] += 1
            performance_grade = scenario_result.get("performance_grade", "UNKNOWN")
            performance_grades.append(performance_grade)
            
            # 성능 이슈 확인
            if performance_grade in ["FAIR", "POOR"]:
                summary["performance_issues"].append({
                    "scenario": scenario_name,
                    "grade": performance_grade,
                    "avg_response_time": scenario_result.get("avg_response_time_ms", 0),
                    "success_rate": scenario_result.get("success_rate", 0)
                })
        
        # 전체 성능 등급 결정
        if performance_grades:
            if all(grade == "EXCELLENT" for grade in performance_grades):
                summary["overall_performance"] = "EXCELLENT"
            elif all(grade in ["EXCELLENT", "GOOD"] for grade in performance_grades):
                summary["overall_performance"] = "GOOD"
            elif any(grade == "POOR" for grade in performance_grades):
                summary["overall_performance"] = "POOR"
            else:
                summary["overall_performance"] = "FAIR"
        
        # 권장사항 생성
        if summary["performance_issues"]:
            summary["recommendations"].append("성능 최적화가 필요한 엔드포인트가 있습니다")
        
        if summary["failed_scenarios"] > 0:
            summary["recommendations"].append("실패한 시나리오가 있습니다 - 시스템 안정성 확인 필요")
        
        if summary["overall_performance"] == "EXCELLENT":
            summary["recommendations"].append("시스템이 우수한 성능을 보이고 있습니다")
        
        return summary


async def main():
    """메인 실행 함수"""
    logger.info("CMA 성능 부하 테스트 시작")
    
    try:
        # 부하 테스트 실행
        load_test = LoadTest()
        results = await load_test.run_load_tests()
        
        # 결과 출력
        print("\n" + "="*60)
        print("CMA 성능 부하 테스트 결과")
        print("="*60)
        
        # 요약 출력
        summary = results.get("summary", {})
        print(f"전체 성능: {summary.get('overall_performance', 'UNKNOWN')}")
        print(f"테스트 실행 시간: {results.get('test_duration_seconds', 0)}초")
        print(f"총 시나리오: {summary.get('total_scenarios', 0)}개")
        print(f"성공: {summary.get('passed_scenarios', 0)}개")
        print(f"실패: {summary.get('failed_scenarios', 0)}개")
        
        # 성능 이슈 출력
        performance_issues = summary.get("performance_issues", [])
        if performance_issues:
            print(f"\n성능 이슈 ({len(performance_issues)}개):")
            for issue in performance_issues:
                print(f"  - {issue['scenario']}: {issue['grade']} (평균 {issue['avg_response_time']:.2f}ms)")
        
        # 권장사항 출력
        recommendations = summary.get("recommendations", [])
        if recommendations:
            print(f"\n권장사항:")
            for rec in recommendations:
                print(f"  - {rec}")
        
        print("="*60)
        
        # 결과를 파일로 저장
        output_file = "load_test_results.json"
        with open(output_file, "w", encoding="utf-8", newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"부하 테스트 결과가 {output_file}에 저장되었습니다.")
        
        return results
        
    except Exception as e:
        logger.error(f"부하 테스트 실행 실패: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main()) 