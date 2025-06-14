import time
import pytest
from typing import Dict, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.labor import create_random_worker, create_random_safety_training, create_random_certification
from app.tests.utils.user import create_random_user

def test_worker_list_performance(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 목록 조회 성능 테스트
    """
    # 1. 테스트 데이터 준비
    workers = [create_random_worker(db) for _ in range(100)]
    
    # 2. 성능 측정
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/",
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
    
    # 5. 필터링 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/?department_id={workers[0].department_id}",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    
    assert response.status_code == 200
    execution_time = end_time - start_time
    assert execution_time < 0.5  # 0.5초 이내 응답

def test_safety_training_performance(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    안전교육 관리 성능 테스트
    """
    # 1. 테스트 데이터 준비
    worker = create_random_worker(db)
    
    # 2. 안전교육 기록 생성 성능 측정
    trainings = []
    for i in range(10):
        training_data = {
            "worker_id": worker.id,
            "training_type": "BASIC",
            "training_date": "2024-03-20",
            "expiry_date": "2025-03-20",
            "instructor": f"강사 {i}",
            "location": f"교육장 {i}",
            "notes": f"교육 노트 {i}"
        }
        
        start_time = time.time()
        response = client.post(
            f"{settings.API_V1_STR}/labor/safety-training",
            headers=superuser_token_headers,
            json=training_data,
        )
        end_time = time.time()
        
        assert response.status_code == 200
        trainings.append(response.json())
        
        execution_time = end_time - start_time
        assert execution_time < 0.5  # 0.5초 이내 응답
    
    # 3. 안전교육 이력 조회 성능 측정
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/safety-training",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    execution_time = end_time - start_time
    assert execution_time < 0.5  # 0.5초 이내 응답

def test_certification_performance(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    자격증 관리 성능 테스트
    """
    # 1. 테스트 데이터 준비
    worker = create_random_worker(db)
    
    # 2. 자격증 등록 성능 측정
    certifications = []
    cert_types = ["건설기계", "전기", "용접", "도장", "목공"]
    
    for cert_type in cert_types:
        cert_data = {
            "worker_id": worker.id,
            "certification_type": cert_type,
            "certification_number": f"CERT-{cert_type}-001",
            "issue_date": "2024-01-01",
            "expiry_date": "2029-01-01",
            "issuing_authority": "한국건설기술인협회",
            "notes": f"{cert_type} 자격증"
        }
        
        start_time = time.time()
        response = client.post(
            f"{settings.API_V1_STR}/labor/certifications",
            headers=superuser_token_headers,
            json=cert_data,
        )
        end_time = time.time()
        
        assert response.status_code == 200
        certifications.append(response.json())
        
        execution_time = end_time - start_time
        assert execution_time < 0.5  # 0.5초 이내 응답
    
    # 3. 자격증 목록 조회 성능 측정
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/certifications",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    execution_time = end_time - start_time
    assert execution_time < 0.5  # 0.5초 이내 응답

def test_worker_concurrent_operations(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 동시 작업 성능 테스트
    """
    import threading
    import queue
    
    # 1. 테스트 데이터 준비
    worker = create_random_worker(db)
    results = queue.Queue()
    
    # 2. 동시 작업 함수 정의
    def concurrent_operation(operation_type: str):
        try:
            if operation_type == "read":
                response = client.get(
                    f"{settings.API_V1_STR}/labor/workers/{worker.id}",
                    headers=superuser_token_headers,
                )
            elif operation_type == "update":
                update_data = {"status": "ACTIVE"}
                response = client.put(
                    f"{settings.API_V1_STR}/labor/workers/{worker.id}",
                    headers=superuser_token_headers,
                    json=update_data,
                )
            elif operation_type == "training":
                training_data = {
                    "worker_id": worker.id,
                    "training_type": "BASIC",
                    "training_date": "2024-03-20",
                    "expiry_date": "2025-03-20",
                    "instructor": "테스트 강사",
                    "location": "테스트 교육장",
                    "notes": "테스트 교육"
                }
                response = client.post(
                    f"{settings.API_V1_STR}/labor/safety-training",
                    headers=superuser_token_headers,
                    json=training_data,
                )
            
            results.put((operation_type, response.status_code))
        except Exception as e:
            results.put((operation_type, str(e)))
    
    # 3. 동시 작업 실행
    threads = []
    operations = ["read", "update", "training"] * 3  # 각 작업 3번씩
    
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