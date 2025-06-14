import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.main import app
from app.models.user import User
from app.models.project import Project
from app.models.contract import Contract
from app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def test_user(db_session: Session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=True
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.mark.integration
def test_project_creation_flow(db_session: Session, auth_headers):
    """프로젝트 생성부터 계약 추가까지의 전체 흐름 테스트"""
    
    # 1. 프로젝트 생성
    project_data = {
        "name": "통합 테스트 프로젝트",
        "code": "INT-TEST-001",
        "description": "통합 테스트를 위한 프로젝트입니다.",
        "status": "active",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "budget": 1000000
    }
    
    response = client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    project = response.json()
    project_id = project["id"]
    
    # 2. 프로젝트 조회
    response = client.get(
        f"/api/v1/projects/{project_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == project_data["name"]
    
    # 3. 계약 생성
    contract_data = {
        "project_id": project_id,
        "contract_number": "CONT-001",
        "client_id": "test-client-id",
        "contract_amount": 1000000,
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "status": "active",
        "contract_type": "construction"
    }
    
    response = client.post(
        "/api/v1/contracts/",
        json=contract_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    contract = response.json()
    contract_id = contract["id"]
    
    # 4. 계약 조회
    response = client.get(
        f"/api/v1/contracts/{contract_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["contract_number"] == contract_data["contract_number"]
    
    # 5. 프로젝트의 계약 목록 조회
    response = client.get(
        f"/api/v1/projects/{project_id}/contracts",
        headers=auth_headers
    )
    assert response.status_code == 200
    contracts = response.json()
    assert len(contracts) == 1
    assert contracts[0]["contract_number"] == contract_data["contract_number"]

@pytest.mark.integration
def test_project_flow_error_cases(db_session: Session, auth_headers):
    """프로젝트 생성 흐름의 에러 케이스 테스트"""
    
    # 1. 잘못된 데이터로 프로젝트 생성 시도
    invalid_project_data = {
        "name": "",  # 빈 이름
        "code": "INVALID",  # 잘못된 코드 형식
        "status": "invalid_status"  # 잘못된 상태값
    }
    
    response = client.post(
        "/api/v1/projects/",
        json=invalid_project_data,
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation Error
    
    # 2. 존재하지 않는 프로젝트에 계약 생성 시도
    non_existent_project_id = 99999
    contract_data = {
        "project_id": non_existent_project_id,
        "contract_number": "CONT-001",
        "contract_amount": 1000000,
        "start_date": datetime.now().isoformat(),
        "status": "active"
    }
    
    response = client.post(
        "/api/v1/contracts/",
        json=contract_data,
        headers=auth_headers
    )
    assert response.status_code == 404  # Not Found
    
    # 3. 권한 없는 사용자로 접근 시도
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = client.get(
        "/api/v1/projects/",
        headers=invalid_headers
    )
    assert response.status_code == 401  # Unauthorized

@pytest.mark.integration
def test_project_update_flow(db_session: Session, auth_headers):
    """프로젝트 수정 흐름 테스트"""
    
    # 1. 프로젝트 생성
    project_data = {
        "name": "수정 테스트 프로젝트",
        "code": "UPDATE-TEST-001",
        "description": "수정 테스트를 위한 프로젝트입니다.",
        "status": "active",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=365)).isoformat(),
        "budget": 1000000
    }
    
    response = client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    project = response.json()
    project_id = project["id"]
    
    # 2. 프로젝트 수정
    update_data = {
        "name": "수정된 프로젝트",
        "description": "수정된 설명입니다.",
        "status": "completed",
        "budget": 2000000
    }
    
    response = client.put(
        f"/api/v1/projects/{project_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    updated_project = response.json()
    assert updated_project["name"] == update_data["name"]
    assert updated_project["description"] == update_data["description"]
    assert updated_project["status"] == update_data["status"]
    assert updated_project["budget"] == update_data["budget"]
    
    # 3. 수정된 프로젝트 조회
    response = client.get(
        f"/api/v1/projects/{project_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"] 