import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.contract import create_random_contract
from app.tests.utils.project import create_random_project
from app.tests.utils.user import create_random_user

client = TestClient(app)

def test_create_contract(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 생성 테스트"""
    project = create_random_project(db)
    data = {
        "title": "테스트 계약",
        "description": "테스트 계약 설명",
        "project_id": project.id,
        "contractor_id": create_random_user(db).id,
        "start_date": datetime.now().date().isoformat(),
        "end_date": (datetime.now() + timedelta(days=365)).date().isoformat(),
        "amount": 100000000,
        "status": "DRAFT"
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["project_id"] == data["project_id"]
    assert content["contractor_id"] == data["contractor_id"]
    assert content["amount"] == data["amount"]
    assert content["status"] == data["status"]
    assert "id" in content

def test_read_contract(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 조회 테스트"""
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == contract.id
    assert content["title"] == contract.title
    assert content["description"] == contract.description

def test_read_contracts(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 목록 조회 테스트"""
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["items"]) > 0
    assert content["items"][0]["id"] == contract.id

def test_update_contract(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 수정 테스트"""
    contract = create_random_contract(db)
    data = {
        "title": "수정된 계약",
        "description": "수정된 계약 설명",
        "status": "ACTIVE"
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["status"] == data["status"]

def test_delete_contract(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 삭제 테스트"""
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "계약이 성공적으로 삭제되었습니다."

def test_create_contract_version(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 버전 생성 테스트"""
    contract = create_random_contract(db)
    data = {
        "version": "1.1.0",
        "content": "수정된 계약 내용",
        "changes": "계약 금액 변경"
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/{contract.id}/versions",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["version"] == data["version"]
    assert content["content"] == data["content"]
    assert content["changes"] == data["changes"]

def test_read_contract_versions(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 버전 목록 조회 테스트"""
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/versions",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content
    assert "total" in content

def test_create_contract_approval(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 승인 요청 테스트"""
    contract = create_random_contract(db)
    data = {
        "approver_id": create_random_user(db).id,
        "comment": "계약 검토 요청"
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/{contract.id}/approvals",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["contract_id"] == contract.id
    assert content["approver_id"] == data["approver_id"]
    assert content["comment"] == data["comment"]
    assert content["status"] == "PENDING"

def test_read_contract_approvals(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 승인 목록 조회 테스트"""
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/approvals",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content
    assert "total" in content

def test_contract_permissions(
    db: Session, superuser_token_headers: dict
) -> None:
    """계약 권한 테스트"""
    # 일반 사용자 토큰 생성
    user = create_random_user(db)
    user_token_headers = {"Authorization": f"Bearer {user.id}"}
    
    # 일반 사용자가 계약 생성 시도
    response = client.post(
        f"{settings.API_V1_STR}/contracts/",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403
    
    # 일반 사용자가 계약 수정 시도
    contract = create_random_contract(db)
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403 