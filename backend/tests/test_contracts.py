from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.contract import create_random_contract
from app.tests.utils.user import create_random_user
from app.tests.utils.project import create_random_project

def test_create_contract(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 생성 API 테스트
    """
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
        "contract_type": "CONSTRUCTION",
        "status": "DRAFT",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "amount": 1000000,
        "currency": "KRW",
        "payment_terms": random_lower_string(),
        "project_id": create_random_project(db).id
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["contract_type"] == data["contract_type"]
    assert content["status"] == data["status"]
    assert "id" in content

def test_read_contract(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 조회 API 테스트
    """
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == contract.name
    assert content["id"] == contract.id

def test_read_contracts(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 목록 조회 API 테스트
    """
    create_random_contract(db)
    create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 2

def test_update_contract(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 수정 API 테스트
    """
    contract = create_random_contract(db)
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
        "status": "ACTIVE"
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["status"] == data["status"]
    assert content["id"] == contract.id

def test_delete_contract(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 삭제 API 테스트
    """
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "success"

def test_create_contract_approval(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 승인 요청 API 테스트
    """
    contract = create_random_contract(db)
    data = {
        "approval_type": "CONTRACT",
        "status": "PENDING",
        "comments": random_lower_string()
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/{contract.id}/approvals",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["approval_type"] == data["approval_type"]
    assert content["status"] == data["status"]
    assert content["comments"] == data["comments"]
    assert "id" in content

def test_create_contract_payment(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 지불 API 테스트
    """
    contract = create_random_contract(db)
    data = {
        "amount": 500000,
        "payment_date": "2024-01-15",
        "payment_type": "PROGRESS",
        "status": "PENDING",
        "description": random_lower_string()
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/{contract.id}/payments",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["amount"] == data["amount"]
    assert content["payment_type"] == data["payment_type"]
    assert content["status"] == data["status"]
    assert "id" in content

def test_create_contract_document(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 문서 API 테스트
    """
    contract = create_random_contract(db)
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "document_type": "CONTRACT",
        "status": "DRAFT"
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/{contract.id}/documents",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["document_type"] == data["document_type"]
    assert content["status"] == data["status"]
    assert "id" in content

def test_contract_permissions(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    """
    계약 API 권한 테스트
    """
    contract = create_random_contract(db)
    
    # 조회 권한 테스트
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    
    # 수정 권한 테스트
    data = {"name": random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    
    # 삭제 권한 테스트
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403 