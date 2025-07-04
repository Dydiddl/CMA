import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user_model

client = TestClient(app)


class TestUserAPI:
    """사용자 API 테스트"""
    
    def test_create_user_success(self, test_db: Session):
        """사용자 생성 성공 테스트"""
        # Given
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "테스트 사용자",
            "role": "user",
            "department": "개발팀",
            "phone": "010-1234-5678",
            "is_active": True
        }
        
        # When
        response = client.post("/api/v1/users/", json=user_data)
        
        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["email"] == user_data["email"]
        assert data["data"]["full_name"] == user_data["full_name"]
        assert "password" not in data["data"]
    
    def test_create_user_duplicate_email(self, test_db: Session):
        """중복 이메일 테스트"""
        # Given
        existing_user = create_test_user_model(test_db, email="test@example.com")
        
        user_data = {
            "email": "test@example.com",  # 중복
            "password": "testpassword123",
            "full_name": "다른 사용자",
            "role": "user",
            "department": "개발팀",
            "phone": "010-9876-5432",
            "is_active": True
        }
        
        # When
        response = client.post("/api/v1/users/", json=user_data)
        
        # Then
        assert response.status_code == 400
        data = response.json()
        assert "이미 존재하는 이메일" in data["detail"]
    
    def test_get_users_success(self, test_db: Session):
        """사용자 목록 조회 성공 테스트"""
        # Given
        user1 = create_test_user_model(test_db, email="user1@example.com")
        user2 = create_test_user_model(test_db, email="user2@example.com")
        
        # When
        response = client.get("/api/v1/users/")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) >= 2
        assert data["total"] >= 2
    
    def test_get_user_by_id_success(self, test_db: Session):
        """사용자 상세 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.get(f"/api/v1/users/{user.id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == user.id
        assert data["data"]["email"] == user.email
    
    def test_get_user_by_id_not_found(self, test_db: Session):
        """존재하지 않는 사용자 조회 테스트"""
        # When
        response = client.get("/api/v1/users/non-existent-id")
        
        # Then
        assert response.status_code == 404
        data = response.json()
        assert "사용자를 찾을 수 없습니다" in data["detail"]
    
    def test_update_user_success(self, test_db: Session):
        """사용자 수정 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        update_data = {
            "full_name": "수정된 사용자명",
            "role": "admin",
            "department": "관리팀",
            "phone": "010-9999-8888"
        }
        
        # When
        response = client.put(f"/api/v1/users/{user.id}", json=update_data)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["full_name"] == update_data["full_name"]
        assert data["data"]["role"] == update_data["role"]
    
    def test_delete_user_success(self, test_db: Session):
        """사용자 삭제 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.delete(f"/api/v1/users/{user.id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "성공적으로 삭제되었습니다" in data["message"]
    
    def test_search_users_by_name(self, test_db: Session):
        """사용자명으로 검색 테스트"""
        # Given
        user1 = create_test_user_model(test_db, full_name="홍길동")
        user2 = create_test_user_model(test_db, full_name="김철수")
        user3 = create_test_user_model(test_db, full_name="이영희")
        
        # When
        response = client.get("/api/v1/users/?search=홍")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) >= 1
        for user in data["data"]:
            assert "홍" in user["full_name"]
    
    def test_filter_users_by_role(self, test_db: Session):
        """사용자 역할로 필터링 테스트"""
        # Given
        user1 = create_test_user_model(test_db, role="admin")
        user2 = create_test_user_model(test_db, role="user")
        
        # When
        response = client.get("/api/v1/users/?role=admin")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        for user in data["data"]:
            assert user["role"] == "admin" 