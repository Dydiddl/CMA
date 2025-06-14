import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from backend.app.main import app
from backend.app.models import User, Project, Contract
from backend.app.core.security import create_access_token

client = TestClient(app)

@pytest.fixture
def test_user(db_session):
    """테스트용 사용자 생성"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_token(test_user):
    """테스트용 JWT 토큰 생성"""
    return create_access_token({"sub": test_user.email})

@pytest.fixture
def auth_headers(test_token):
    """인증 헤더 생성"""
    return {"Authorization": f"Bearer {test_token}"}

def test_create_project(auth_headers, db_session):
    """프로젝트 생성 API 테스트"""
    project_data = {
        "name": "테스트 프로젝트",
        "code": "TEST-001",
        "description": "테스트용 프로젝트입니다.",
        "status": "active"
    }
    
    response = client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["code"] == project_data["code"]

def test_get_project(auth_headers, db_session):
    """프로젝트 조회 API 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    response = client.get(
        f"/api/v1/projects/{project.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project.name
    assert data["code"] == project.code

def test_update_project(auth_headers, db_session):
    """프로젝트 수정 API 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    update_data = {
        "name": "수정된 프로젝트",
        "status": "completed"
    }
    
    response = client.put(
        f"/api/v1/projects/{project.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["status"] == update_data["status"]

def test_delete_project(auth_headers, db_session):
    """프로젝트 삭제 API 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    response = client.delete(
        f"/api/v1/projects/{project.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # 삭제 확인
    deleted_project = db_session.query(Project).filter_by(id=project.id).first()
    assert deleted_project is None

def test_create_contract(auth_headers, db_session):
    """계약 생성 API 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    contract_data = {
        "project_id": project.id,
        "contract_number": "CONT-001",
        "client_id": "test-client-id",
        "contract_amount": 1000000,
        "start_date": datetime.now().isoformat(),
        "status": "active",
        "contract_type": "construction"
    }
    
    response = client.post(
        "/api/v1/contracts/",
        json=contract_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["contract_number"] == contract_data["contract_number"]
    assert data["project_id"] == project.id

def test_unauthorized_access():
    """인증되지 않은 접근 테스트"""
    response = client.get("/api/v1/projects/")
    assert response.status_code == 401

def test_invalid_token():
    """잘못된 토큰 테스트"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/projects/", headers=headers)
    assert response.status_code == 401

def test_project_not_found(auth_headers):
    """존재하지 않는 프로젝트 조회 테스트"""
    response = client.get(
        "/api/v1/projects/999999",
        headers=auth_headers
    )
    assert response.status_code == 404 