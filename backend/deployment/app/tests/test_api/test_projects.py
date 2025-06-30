"""
프로젝트 API 테스트
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User
from app.models.project import Project

def test_create_project(client: TestClient, db: Session):
    """
    프로젝트 생성 테스트
    """
    # 테스트용 사용자 생성
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 테스트용 토큰 생성
    access_token = create_access_token({"sub": user.email})

    # 프로젝트 생성 요청
    response = client.post(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "Test Project",
            "description": "Test Description",
            "status": "active",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-12-31T23:59:59"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Test Description"
    assert data["status"] == "active"

def test_get_projects(client: TestClient, db: Session):
    """
    프로젝트 목록 조회 테스트
    """
    # 테스트용 사용자 생성
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 테스트용 프로젝트 생성
    project = Project(
        name="Test Project",
        description="Test Description",
        status="active",
        owner_id=user.id
    )
    db.add(project)
    db.commit()

    # 테스트용 토큰 생성
    access_token = create_access_token({"sub": user.email})

    # 프로젝트 목록 조회 요청
    response = client.get(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Project" 