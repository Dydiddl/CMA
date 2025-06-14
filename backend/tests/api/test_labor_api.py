import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.labor import create_random_worker
from app.tests.utils.department import create_random_department
from app.tests.utils.user import create_random_user

client = TestClient(app)

def test_create_worker(
    db: Session, superuser_token_headers: dict
) -> None:
    """작업자 등록 테스트"""
    department = create_random_department(db)
    data = {
        "name": "홍길동",
        "id_number": "123456-1234567",
        "phone": "010-1234-5678",
        "address": "서울시 강남구",
        "department_id": department.id,
        "position": "기술자",
        "hire_date": datetime.now().date().isoformat(),
        "emergency_contact": {
            "name": "홍부모",
            "relationship": "부",
            "phone": "010-9876-5432"
        }
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["id_number"] == data["id_number"]
    assert content["phone"] == data["phone"]
    assert content["department_id"] == data["department_id"]
    assert content["position"] == data["position"]
    assert content["emergency_contact"] == data["emergency_contact"]
    assert "id" in content

def test_read_worker(
    db: Session, superuser_token_headers: dict
) -> None:
    """작업자 조회 테스트"""
    worker = create_random_worker(db)
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == worker.id
    assert content["name"] == worker.name
    assert content["id_number"] == worker.id_number

def test_read_workers(
    db: Session, superuser_token_headers: dict
) -> None:
    """작업자 목록 조회 테스트"""
    worker = create_random_worker(db)
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["items"]) > 0
    assert content["items"][0]["id"] == worker.id

def test_update_worker(
    db: Session, superuser_token_headers: dict
) -> None:
    """작업자 정보 수정 테스트"""
    worker = create_random_worker(db)
    data = {
        "phone": "010-9999-8888",
        "address": "서울시 서초구",
        "position": "수석기술자"
    }
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["phone"] == data["phone"]
    assert content["address"] == data["address"]
    assert content["position"] == data["position"]

def test_terminate_worker(
    db: Session, superuser_token_headers: dict
) -> None:
    """작업자 퇴사 처리 테스트"""
    worker = create_random_worker(db)
    data = {
        "termination_date": datetime.now().date().isoformat(),
        "reason": "개인사유"
    }
    response = client.put(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/terminate",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "TERMINATED"
    assert content["termination_date"] == data["termination_date"]
    assert content["reason"] == data["reason"]

def test_create_safety_training(
    db: Session, superuser_token_headers: dict
) -> None:
    """안전 교육 기록 테스트"""
    worker = create_random_worker(db)
    data = {
        "worker_id": worker.id,
        "type": "BASIC",
        "completed_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),
        "instructor": "김교육",
        "location": "본사 교육장"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/safety-trainings",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["worker_id"] == data["worker_id"]
    assert content["type"] == data["type"]
    assert content["instructor"] == data["instructor"]
    assert content["location"] == data["location"]

def test_read_safety_trainings(
    db: Session, superuser_token_headers: dict
) -> None:
    """안전 교육 이력 조회 테스트"""
    worker = create_random_worker(db)
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/safety-trainings",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content
    assert "total" in content

def test_create_certification(
    db: Session, superuser_token_headers: dict
) -> None:
    """자격증 등록 테스트"""
    worker = create_random_worker(db)
    data = {
        "worker_id": worker.id,
        "type": "건설기계조종사",
        "number": "12345",
        "issue_date": datetime.now().date().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=365*5)).date().isoformat(),
        "issuing_authority": "국토교통부"
    }
    response = client.post(
        f"{settings.API_V1_STR}/labor/certifications",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["worker_id"] == data["worker_id"]
    assert content["type"] == data["type"]
    assert content["number"] == data["number"]
    assert content["issuing_authority"] == data["issuing_authority"]

def test_read_certifications(
    db: Session, superuser_token_headers: dict
) -> None:
    """자격증 목록 조회 테스트"""
    worker = create_random_worker(db)
    response = client.get(
        f"{settings.API_V1_STR}/labor/workers/{worker.id}/certifications",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content
    assert "total" in content

def test_labor_permissions(
    db: Session, superuser_token_headers: dict
) -> None:
    """인력 관리 권한 테스트"""
    # 일반 사용자 토큰 생성
    user = create_random_user(db)
    user_token_headers = {"Authorization": f"Bearer {user.id}"}
    
    # 일반 사용자가 작업자 등록 시도
    response = client.post(
        f"{settings.API_V1_STR}/labor/workers",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403
    
    # 일반 사용자가 안전 교육 기록 시도
    response = client.post(
        f"{settings.API_V1_STR}/labor/safety-trainings",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403 