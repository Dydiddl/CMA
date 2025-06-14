from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.labor import create_random_worker
from app.tests.utils.user import create_random_user

def test_create_worker(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 등록 API 테스트
    """
    data = {
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
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["position"] == data["position"]
    assert content["department"] == data["department"]
    assert content["status"] == data["status"]
    assert "id" in content

def test_read_worker(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 조회 API 테스트
    """
    worker = create_random_worker(db)
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == worker.name
    assert content["id"] == worker.id

def test_read_workers(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 목록 조회 API 테스트
    """
    create_random_worker(db)
    create_random_worker(db)
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 2

def test_update_worker(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    작업자 정보 수정 API 테스트
    """
    worker = create_random_worker(db)
    data = {
        "name": random_lower_string(),
        "position": "SENIOR_WORKER",
        "status": "INACTIVE"
    }
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["position"] == data["position"]
    assert content["status"] == data["status"]
    assert content["id"] == worker.id

def test_create_safety_training(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    안전 교육 기록 API 테스트
    """
    worker = create_random_worker(db)
    data = {
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
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["training_type"] == data["training_type"]
    assert content["score"] == data["score"]
    assert content["certificate_number"] == data["certificate_number"]
    assert "id" in content

def test_create_certification(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    자격증 기록 API 테스트
    """
    worker = create_random_worker(db)
    data = {
        "certification_type": "HEAVY_EQUIPMENT",
        "certification_number": "HE-2024-001",
        "issue_date": "2024-01-01",
        "expiry_date": "2029-01-01",
        "issuing_authority": "MINISTRY_OF_LABOR"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/certifications",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["certification_type"] == data["certification_type"]
    assert content["certification_number"] == data["certification_number"]
    assert content["issuing_authority"] == data["issuing_authority"]
    assert "id" in content

def test_labor_permissions(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    """
    인력 API 권한 테스트
    """
    worker = create_random_worker(db)
    
    # 조회 권한 테스트
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    
    # 수정 권한 테스트
    data = {"name": random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    
    # 안전 교육 기록 권한 테스트
    training_data = {
        "training_type": "BASIC",
        "training_date": "2024-01-15"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/safety-training",
        headers=normal_user_token_headers,
        json=training_data,
    )
    assert response.status_code == 403 