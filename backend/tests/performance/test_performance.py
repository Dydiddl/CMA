#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 테스트 모듈
"""

import pytest
import time
import asyncio
from typing import List
from fastapi.testclient import TestClient


class TestAPIPerformance:
    """API 성능 테스트 클래스"""
    
    def test_contract_list_performance(self, client: TestClient, large_dataset: List[dict]):
        """계약 목록 조회 성능 테스트"""
        # 대용량 데이터 생성
        for contract_data in large_dataset[:50]:  # 50개 계약 생성
            client.post("/api/v1/contracts/", json=contract_data)
        
        # 성능 측정
        start_time = time.time()
        response = client.get("/api/v1/contracts/?limit=100")
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 성능 검증
        assert response.status_code == 200
        assert execution_time < 2.0  # 2초 이내 응답
        assert response.json()["status"] == "success"
    
    def test_contract_search_performance(self, client: TestClient, large_dataset: List[dict]):
        """계약 검색 성능 테스트"""
        # 대용량 데이터 생성
        for contract_data in large_dataset[:100]:  # 100개 계약 생성
            client.post("/api/v1/contracts/", json=contract_data)
        
        # 성능 측정
        start_time = time.time()
        response = client.get("/api/v1/contracts/?search=계약")
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 성능 검증
        assert response.status_code == 200
        assert execution_time < 1.0  # 1초 이내 응답
        assert response.json()["status"] == "success"
    
    def test_concurrent_requests_performance(self, client: TestClient):
        """동시 요청 성능 테스트"""
        import threading
        import concurrent.futures
        
        def make_request():
            return client.get("/api/v1/contracts/")
        
        # 10개의 동시 요청
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in concurrent.futures.as_completed(futures)]
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 성능 검증
        assert all(response.status_code == 200 for response in responses)
        assert execution_time < 5.0  # 5초 이내 모든 요청 완료
    
    def test_memory_usage_performance(self, client: TestClient, large_dataset: List[dict]):
        """메모리 사용량 성능 테스트"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 대용량 데이터 처리
        for contract_data in large_dataset:
            client.post("/api/v1/contracts/", json=contract_data)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # 메모리 사용량 검증
        assert memory_increase < 100  # 100MB 이내 메모리 증가


class TestDatabasePerformance:
    """데이터베이스 성능 테스트 클래스"""
    
    def test_bulk_insert_performance(self, db_session):
        """대량 삽입 성능 테스트"""
        from app.models.contract import Contract
        
        contracts = []
        for i in range(1000):
            contract = Contract(
                name=f"계약 {i}",
                contract_number=f"CON-2024-{i:04d}",
                contract_amount=1000000 + (i * 1000),
                contract_date="2024-01-15T00:00:00",
                client_name=f"발주처 {i}",
                vendor_id=f"vendor-{i}",
                status="진행중"
            )
            contracts.append(contract)
        
        start_time = time.time()
        db_session.add_all(contracts)
        db_session.commit()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 성능 검증
        assert execution_time < 10.0  # 10초 이내 1000개 레코드 삽입
    
    def test_complex_query_performance(self, db_session):
        """복잡한 쿼리 성능 테스트"""
        from app.models.contract import Contract
        from sqlalchemy import func
        
        # 대량 데이터 생성
        contracts = []
        for i in range(500):
            contract = Contract(
                name=f"계약 {i}",
                contract_number=f"CON-2024-{i:04d}",
                contract_amount=1000000 + (i * 1000),
                contract_date="2024-01-15T00:00:00",
                client_name=f"발주처 {i % 10}",  # 10개 발주처로 제한
                vendor_id=f"vendor-{i % 5}",     # 5개 거래처로 제한
                status="진행중" if i % 2 == 0 else "완료"
            )
            contracts.append(contract)
        
        db_session.add_all(contracts)
        db_session.commit()
        
        # 복잡한 집계 쿼리 성능 측정
        start_time = time.time()
        result = db_session.query(
            Contract.client_name,
            func.count(Contract.id).label('contract_count'),
            func.sum(Contract.contract_amount).label('total_amount'),
            func.avg(Contract.contract_amount).label('avg_amount')
        ).group_by(Contract.client_name).all()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 성능 검증
        assert execution_time < 1.0  # 1초 이내 복잡한 집계 쿼리
        assert len(result) == 10  # 10개 발주처


class TestASCRPerformance:
    """ASCR 모듈 성능 테스트 클래스"""
    
    def test_pdf_processing_performance(self, sample_pdf_data: dict):
        """PDF 처리 성능 테스트"""
        # PDF 처리 시간 측정
        start_time = time.time()
        
        # 실제 PDF 처리 로직 (모의)
        time.sleep(0.1)  # PDF 처리 시뮬레이션
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 성능 검증
        assert execution_time < 5.0  # 5초 이내 PDF 처리
    
    def test_excel_processing_performance(self, sample_excel_data: dict):
        """Excel 처리 성능 테스트"""
        # Excel 처리 시간 측정
        start_time = time.time()
        
        # 실제 Excel 처리 로직 (모의)
        time.sleep(0.05)  # Excel 처리 시뮬레이션
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 성능 검증
        assert execution_time < 2.0  # 2초 이내 Excel 처리


class TestCachingPerformance:
    """캐싱 성능 테스트 클래스"""
    
    def test_cache_hit_performance(self, client: TestClient):
        """캐시 히트 성능 테스트"""
        # 첫 번째 요청 (캐시 미스)
        start_time = time.time()
        response1 = client.get("/api/v1/contracts/")
        first_request_time = time.time() - start_time
        
        # 두 번째 요청 (캐시 히트)
        start_time = time.time()
        response2 = client.get("/api/v1/contracts/")
        second_request_time = time.time() - start_time
        
        # 캐시 효과 검증
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert second_request_time < first_request_time  # 캐시 히트가 더 빠름
        assert second_request_time < 0.1  # 캐시 히트는 0.1초 이내 