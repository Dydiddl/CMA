#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 노무 관리 성능 테스트
"""

import time
import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.labor_service import LaborService
from app.schemas.labor import LaborCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LaborPerformanceTest:
    """노무 관리 성능 테스트 클래스"""
    
    def __init__(self):
        self.db = next(get_db())
        self.labor_service = LaborService(self.db)
        self.test_results = {}
    
    def generate_test_data(self, count: int = 100) -> List[LaborCreate]:
        """테스트 데이터 생성"""
        job_types = ["기술자", "일반노무자", "관리자", "안전관리자", "품질관리자"]
        statuses = ["재직", "퇴직", "휴직"]
        names = ["김철수", "이영희", "박민수", "정수진", "최동욱", "한미영", "송태호", "윤지영"]
        
        test_data = []
        for i in range(count):
            labor_data = LaborCreate(
                worker_name=f"{random.choice(names)}{i+1}",
                ssn=f"90{random.randint(1, 12):02d}{random.randint(1, 28):02d}-{random.randint(1000000, 9999999)}",
                birth_date=f"1990-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                gender=random.choice(["남성", "여성"]),
                job_type=random.choice(job_types),
                hire_date=f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                hourly_wage=random.randint(15000, 30000),
                work_hours=random.randint(6, 10),
                status=random.choice(statuses),
                contact=f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                address=f"서울시 {random.choice(['강남구', '서초구', '마포구', '종로구'])}",
                emergency_contact=f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                memo=f"성능 테스트용 노무자 {i+1}"
            )
            test_data.append(labor_data)
        
        return test_data
    
    def test_create_performance(self, count: int = 100) -> Dict[str, Any]:
        """노무자 생성 성능 테스트"""
        logger.info(f"노무자 생성 성능 테스트 시작: {count}개")
        
        test_data = self.generate_test_data(count)
        created_labors = []
        
        start_time = time.time()
        
        try:
            for i, labor_data in enumerate(test_data):
                start_create = time.time()
                created_labor = self.labor_service.create_labor(labor_data)
                end_create = time.time()
                
                created_labors.append(created_labor)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"생성 진행률: {i + 1}/{count}")
        
        except Exception as e:
            logger.error(f"노무자 생성 중 오류: {e}")
            # 생성된 노무자들 정리
            for labor in created_labors:
                try:
                    self.labor_service.delete_labor(labor.id)
                except:
                    pass
            raise
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / count
        
        result = {
            "test_name": "노무자 생성 성능",
            "total_count": count,
            "total_time": total_time,
            "average_time": avg_time,
            "operations_per_second": count / total_time,
            "created_labors": created_labors
        }
        
        logger.info(f"노무자 생성 성능 테스트 완료: {total_time:.2f}초 ({avg_time:.3f}초/개)")
        return result
    
    def test_query_performance(self, search_terms: List[str] = None) -> Dict[str, Any]:
        """노무자 조회 성능 테스트"""
        logger.info("노무자 조회 성능 테스트 시작")
        
        if search_terms is None:
            search_terms = ["기술자", "재직", "김", "010"]
        
        results = {}
        
        for term in search_terms:
            start_time = time.time()
            
            # 검색 실행
            labor_list, total = self.labor_service.get_labor_records(
                skip=0, 
                limit=100, 
                search=term
            )
            
            end_time = time.time()
            query_time = end_time - start_time
            
            results[term] = {
                "search_term": term,
                "query_time": query_time,
                "result_count": len(labor_list),
                "total_count": total
            }
            
            logger.info(f"검색 '{term}': {query_time:.3f}초, 결과 {len(labor_list)}개")
        
        # 페이징 성능 테스트
        start_time = time.time()
        labor_list, total = self.labor_service.get_labor_records(skip=0, limit=10)
        end_time = time.time()
        paging_time = end_time - start_time
        
        results["paging"] = {
            "test_type": "페이징",
            "query_time": paging_time,
            "result_count": len(labor_list),
            "total_count": total
        }
        
        logger.info(f"페이징 성능: {paging_time:.3f}초")
        
        return results
    
    def test_summary_performance(self, iterations: int = 10) -> Dict[str, Any]:
        """노무 요약 통계 성능 테스트"""
        logger.info(f"노무 요약 통계 성능 테스트 시작: {iterations}회")
        
        times = []
        
        for i in range(iterations):
            start_time = time.time()
            
            summary = self.labor_service.get_labor_summary()
            
            end_time = time.time()
            query_time = end_time - start_time
            times.append(query_time)
            
            logger.info(f"요약 통계 {i+1}: {query_time:.3f}초")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        result = {
            "test_name": "노무 요약 통계 성능",
            "iterations": iterations,
            "average_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "total_time": sum(times)
        }
        
        logger.info(f"요약 통계 성능 테스트 완료: 평균 {avg_time:.3f}초")
        return result
    
    def test_batch_operations_performance(self, batch_size: int = 50) -> Dict[str, Any]:
        """배치 작업 성능 테스트"""
        logger.info(f"배치 작업 성능 테스트 시작: 배치 크기 {batch_size}")
        
        # 배치용 테스트 데이터 생성
        test_records = []
        for i in range(batch_size):
            record = {
                "worker_id": f"test-worker-{i}",
                "work_date": datetime.now().strftime("%Y-%m-%d"),
                "hours_worked": random.randint(6, 10),
                "project_id": f"test-project-{random.randint(1, 5)}"
            }
            test_records.append(record)
        
        start_time = time.time()
        
        try:
            result = self.labor_service.batch_create_labor_records(test_records)
            end_time = time.time()
            
            batch_time = end_time - start_time
            
            result_data = {
                "test_name": "배치 작업 성능",
                "batch_size": batch_size,
                "total_time": batch_time,
                "average_time_per_record": batch_time / batch_size,
                "records_per_second": batch_size / batch_time
            }
            
            logger.info(f"배치 작업 성능 테스트 완료: {batch_time:.3f}초")
            return result_data
            
        except Exception as e:
            logger.error(f"배치 작업 성능 테스트 실패: {e}")
            raise
    
    def test_cache_performance(self) -> Dict[str, Any]:
        """캐시 성능 테스트"""
        logger.info("캐시 성능 테스트 시작")
        
        # 첫 번째 조회 (캐시 미스)
        start_time = time.time()
        summary1 = self.labor_service.get_labor_summary()
        first_query_time = time.time() - start_time
        
        # 두 번째 조회 (캐시 히트)
        start_time = time.time()
        summary2 = self.labor_service.get_labor_summary()
        second_query_time = time.time() - start_time
        
        # 캐시 효과 계산
        cache_improvement = (first_query_time - second_query_time) / first_query_time * 100
        
        result = {
            "test_name": "캐시 성능",
            "first_query_time": first_query_time,
            "second_query_time": second_query_time,
            "cache_improvement_percent": cache_improvement,
            "cache_effectiveness": "효과적" if cache_improvement > 50 else "보통"
        }
        
        logger.info(f"캐시 성능 테스트 완료: 개선율 {cache_improvement:.1f}%")
        return result
    
    def run_all_performance_tests(self) -> Dict[str, Any]:
        """모든 성능 테스트 실행"""
        logger.info("=== 노무 관리 성능 테스트 시작 ===")
        
        all_results = {}
        
        try:
            # 1. 생성 성능 테스트
            logger.info("1. 노무자 생성 성능 테스트")
            all_results["create_performance"] = self.test_create_performance(count=50)
            
            # 2. 조회 성능 테스트
            logger.info("2. 노무자 조회 성능 테스트")
            all_results["query_performance"] = self.test_query_performance()
            
            # 3. 요약 통계 성능 테스트
            logger.info("3. 노무 요약 통계 성능 테스트")
            all_results["summary_performance"] = self.test_summary_performance()
            
            # 4. 캐시 성능 테스트
            logger.info("4. 캐시 성능 테스트")
            all_results["cache_performance"] = self.test_cache_performance()
            
            # 5. 배치 작업 성능 테스트
            logger.info("5. 배치 작업 성능 테스트")
            all_results["batch_performance"] = self.test_batch_operations_performance()
            
            # 6. 데이터베이스 최적화 분석
            logger.info("6. 데이터베이스 최적화 분석")
            all_results["db_optimization"] = self.labor_service.optimize_database_queries()
            
        except Exception as e:
            logger.error(f"성능 테스트 실행 중 오류: {e}")
            raise
        finally:
            # 테스트 데이터 정리
            self._cleanup_test_data()
        
        # 성능 요약 생성
        all_results["summary"] = self._generate_performance_summary(all_results)
        
        logger.info("=== 노무 관리 성능 테스트 완료 ===")
        return all_results
    
    def _cleanup_test_data(self):
        """테스트 데이터 정리"""
        logger.info("테스트 데이터 정리 시작")
        
        try:
            # 테스트용 노무자들 삭제
            test_labors, _ = self.labor_service.get_labor_records(search="성능 테스트용")
            
            for labor in test_labors:
                try:
                    self.labor_service.delete_labor(labor.id)
                except:
                    pass
            
            logger.info(f"테스트 데이터 정리 완료: {len(test_labors)}개 삭제")
            
        except Exception as e:
            logger.error(f"테스트 데이터 정리 실패: {e}")
    
    def _generate_performance_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """성능 요약 생성"""
        summary = {
            "test_timestamp": datetime.now().isoformat(),
            "overall_status": "PASS",
            "performance_metrics": {},
            "recommendations": []
        }
        
        # 생성 성능 분석
        if "create_performance" in results:
            create_perf = results["create_performance"]
            summary["performance_metrics"]["create_ops_per_second"] = create_perf["operations_per_second"]
            
            if create_perf["operations_per_second"] < 1:
                summary["recommendations"].append("노무자 생성 성능 개선 필요")
        
        # 조회 성능 분석
        if "query_performance" in results:
            query_perf = results["query_performance"]
            avg_query_time = sum(
                result["query_time"] for result in query_perf.values() 
                if isinstance(result, dict) and "query_time" in result
            ) / len([k for k, v in query_perf.items() if isinstance(v, dict) and "query_time" in v])
            
            summary["performance_metrics"]["average_query_time"] = avg_query_time
            
            if avg_query_time > 1.0:
                summary["recommendations"].append("노무자 조회 성능 개선 필요")
        
        # 캐시 성능 분석
        if "cache_performance" in results:
            cache_perf = results["cache_performance"]
            summary["performance_metrics"]["cache_improvement"] = cache_perf["cache_improvement_percent"]
            
            if cache_perf["cache_improvement_percent"] < 50:
                summary["recommendations"].append("캐시 효과 개선 필요")
        
        # 전체 상태 결정
        if len(summary["recommendations"]) > 2:
            summary["overall_status"] = "NEEDS_IMPROVEMENT"
        elif len(summary["recommendations"]) > 0:
            summary["overall_status"] = "WARNING"
        
        return summary


def main():
    """메인 실행 함수"""
    logger.info("노무 관리 성능 테스트 시작")
    
    try:
        # 성능 테스트 실행
        performance_test = LaborPerformanceTest()
        results = performance_test.run_all_performance_tests()
        
        # 결과 출력
        print("\n" + "="*60)
        print("노무 관리 성능 테스트 결과")
        print("="*60)
        
        # 요약 출력
        summary = results.get("summary", {})
        print(f"전체 상태: {summary.get('overall_status', 'UNKNOWN')}")
        print(f"테스트 시간: {summary.get('test_timestamp', 'UNKNOWN')}")
        
        # 성능 지표 출력
        metrics = summary.get("performance_metrics", {})
        if metrics:
            print("\n성능 지표:")
            for key, value in metrics.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.3f}")
                else:
                    print(f"  {key}: {value}")
        
        # 권장사항 출력
        recommendations = summary.get("recommendations", [])
        if recommendations:
            print("\n권장사항:")
            for rec in recommendations:
                print(f"  - {rec}")
        
        print("="*60)
        
        # 상세 결과를 파일로 저장
        import json
        with open("labor_performance_test_results.json", "w", encoding="utf-8", newline='', encoding='utf-8', newline='') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info("성능 테스트 결과가 labor_performance_test_results.json에 저장되었습니다.")
        
    except Exception as e:
        logger.error(f"성능 테스트 실행 실패: {e}")
        raise


if __name__ == "__main__":
    main() 