from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.labor import create_random_worker
from app.tests.utils.user import create_random_user

def test_worker_workflow(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 전체 워크플로우 테스트
    """
    # 1. 작업자 등록
    worker_data = {
        "name": random_lower_string(),
        "position": "WORKER",
        "department": "CONSTRUCTION",
        "contact": "010-1234-5678",
        "status": "ACTIVE",
        "hire_date": "2024-01-01",
        "salary": 3000000,
        "bank_account": "123-456-789012",
        "emergency_contact": "010-9876-5432"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers",
        headers=superuser_token_headers,
        json=worker_data,
    )
    assert response.status_code == 200
    worker = response.json()
    
    # 2. 안전 교육 기록
    training_data = {
        "training_type": "BASIC",
        "training_date": "2024-01-15",
        "trainer": random_lower_string(),
        "score": 95,
        "certificate_number": "SAFE-2024-001",
        "expiry_date": "2025-01-15"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers/{worker['id']}/safety-training",
        headers=superuser_token_headers,
        json=training_data,
    )
    assert response.status_code == 200
    training = response.json()
    
    # 3. 자격증 기록
    certification_data = {
        "certification_type": "HEAVY_EQUIPMENT",
        "certification_number": "HE-2024-001",
        "issue_date": "2024-01-01",
        "expiry_date": "2029-01-01",
        "issuing_authority": "MINISTRY_OF_LABOR"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers/{worker['id']}/certifications",
        headers=superuser_token_headers,
        json=certification_data,
    )
    assert response.status_code == 200
    certification = response.json()
    
    # 4. 작업자 정보 수정
    update_data = {
        "position": "SENIOR_WORKER",
        "salary": 3500000
    }
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker['id']}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    
    # 5. 작업자 퇴사 처리
    termination_data = {
        "status": "INACTIVE",
        "termination_date": "2024-12-31",
        "reason": "개인사유"
    }
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker['id']}",
        headers=superuser_token_headers,
        json=termination_data,
    )
    assert response.status_code == 200

def test_worker_certification_workflow(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 자격증 워크플로우 테스트
    """
    # 1. 작업자 등록
    worker = create_random_worker(db)
    
    # 2. 여러 자격증 등록
    certifications = []
    cert_types = ["HEAVY_EQUIPMENT", "ELECTRICAL", "WELDING"]
    
    for cert_type in cert_types:
        cert_data = {
            "certification_type": cert_type,
            "certification_number": f"{cert_type}-2024-001",
            "issue_date": "2024-01-01",
            "expiry_date": "2029-01-01",
            "issuing_authority": "MINISTRY_OF_LABOR"
        }
        response = client.post(
            f"{settings.API_V1_STR}/labor/workers/{worker.id}/certifications",
            headers=superuser_token_headers,
            json=cert_data,
        )
        assert response.status_code == 200
        certifications.append(response.json())
    
    # 3. 자격증 갱신
    renewal_data = {
        "expiry_date": "2034-01-01",
        "renewal_date": "2029-01-01"
    }
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/certifications/{certifications[0]['id']}",
        headers=superuser_token_headers,
        json=renewal_data,
    )
    assert response.status_code == 200

def test_worker_safety_training_workflow(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 안전 교육 워크플로우 테스트
    """
    # 1. 작업자 등록
    worker = create_random_worker(db)
    
    # 2. 기본 안전 교육
    basic_training_data = {
        "training_type": "BASIC",
        "training_date": "2024-01-15",
        "trainer": random_lower_string(),
        "score": 95,
        "certificate_number": "SAFE-2024-001",
        "expiry_date": "2025-01-15"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/safety-training",
        headers=superuser_token_headers,
        json=basic_training_data,
    )
    assert response.status_code == 200
    basic_training = response.json()
    
    # 3. 고급 안전 교육
    advanced_training_data = {
        "training_type": "ADVANCED",
        "training_date": "2024-02-15",
        "trainer": random_lower_string(),
        "score": 90,
        "certificate_number": "SAFE-2024-002",
        "expiry_date": "2025-02-15"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/safety-training",
        headers=superuser_token_headers,
        json=advanced_training_data,
    )
    assert response.status_code == 200
    advanced_training = response.json()
    
    # 4. 교육 이력 조회
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/safety-training",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    training_history = response.json()
    assert len(training_history) >= 2 