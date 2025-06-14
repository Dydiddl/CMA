import time
import pytest
from typing import Dict, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.contract import create_random_contract
from app.tests.utils.user import create_random_user

def test_contract_list_performance(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 목록 조회 성능 테스트
    """
    # 1. 테스트 데이터 준비
    contracts = [create_random_contract(db) for _ in range(100)]
    
    # 2. 성능 측정
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/contracts/",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    
    # 3. 결과 검증
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 100
    
    # 4. 성능 기준 검증
    execution_time = end_time - start_time
    assert execution_time < 1.0  # 1초 이내 응답
    
    # 5. 페이지네이션 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/contracts/?skip=0&limit=10",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    execution_time = end_time - start_time
    assert execution_time < 0.5  # 0.5초 이내 응답

def test_contract_search_performance(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 검색 성능 테스트
    """
    # 1. 테스트 데이터 준비
    contracts = [create_random_contract(db) for _ in range(100)]
    
    # 2. 검색 성능 측정
    search_terms = ["계약", "프로젝트", "시공", "유지보수"]
    
    for term in search_terms:
        start_time = time.time()
        response = client.get(
            f"{settings.API_V1_STR}/contracts/search?q={term}",
            headers=superuser_token_headers,
        )
        end_time = time.time()
        
        assert response.status_code == 200
        execution_time = end_time - start_time
        assert execution_time < 0.5  # 0.5초 이내 응답

def test_contract_version_performance(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 버전 관리 성능 테스트
    """
    # 1. 테스트 데이터 준비
    contract = create_random_contract(db)
    
    # 2. 버전 생성 성능 측정
    versions = []
    for i in range(10):
        version_data = {
            "version": f"1.{i}.0",
            "content": f"버전 {i} 내용",
            "changes": f"버전 {i} 변경사항",
            "status": "DRAFT"
        }
        
        start_time = time.time()
        response = client.post(
            f"{settings.API_V1_STR}/contracts/{contract.id}/versions",
            headers=superuser_token_headers,
            json=version_data,
        )
        end_time = time.time()
        
        assert response.status_code == 200
        versions.append(response.json())
        
        execution_time = end_time - start_time
        assert execution_time < 0.5  # 0.5초 이내 응답
    
    # 3. 버전 목록 조회 성능 측정
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/versions",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    execution_time = end_time - start_time
    assert execution_time < 0.5  # 0.5초 이내 응답

def test_contract_concurrent_operations(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 동시 작업 성능 테스트
    """
    import threading
    import queue
    
    # 1. 테스트 데이터 준비
    contract = create_random_contract(db)
    results = queue.Queue()
    
    # 2. 동시 작업 함수 정의
    def concurrent_operation(operation_type: str):
        try:
            if operation_type == "read":
                response = client.get(
                    f"{settings.API_V1_STR}/contracts/{contract.id}",
                    headers=superuser_token_headers,
                )
            elif operation_type == "update":
                update_data = {"status": "IN_PROGRESS"}
                response = client.put(
                    f"{settings.API_V1_STR}/contracts/{contract.id}",
                    headers=superuser_token_headers,
                    json=update_data,
                )
            elif operation_type == "version":
                version_data = {
                    "version": "1.0.0",
                    "content": "동시 작업 테스트",
                    "changes": "테스트",
                    "status": "DRAFT"
                }
                response = client.post(
                    f"{settings.API_V1_STR}/contracts/{contract.id}/versions",
                    headers=superuser_token_headers,
                    json=version_data,
                )
            
            results.put((operation_type, response.status_code))
        except Exception as e:
            results.put((operation_type, str(e)))
    
    # 3. 동시 작업 실행
    threads = []
    operations = ["read", "update", "version"] * 3  # 각 작업 3번씩
    
    start_time = time.time()
    for op in operations:
        thread = threading.Thread(target=concurrent_operation, args=(op,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    end_time = time.time()
    
    # 4. 결과 검증
    execution_time = end_time - start_time
    assert execution_time < 3.0  # 3초 이내 완료
    
    success_count = 0
    while not results.empty():
        op_type, status = results.get()
        if status == 200:
            success_count += 1
    
    assert success_count >= 7  # 최소 7개 이상의 작업이 성공해야 함 