import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user_model, create_test_vendor_model

client = TestClient(app)

class TestVendorAPI:
    """거래처 API 테스트"""
    
    def test_create_vendor_success(self, test_db: Session):
        """거래처 생성 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor_data = {
            "name": "테스트 거래처",
            "business_number": "1234567890",
            "representative": "홍길동",
            "address": "서울시 강남구 테스트로 123",
            "phone": "02-1234-5678",
            "email": "test@vendor.com",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "status": "활성",
            "description": "테스트용 거래처입니다."
        }
        
        # When
        response = client.post("/api/v1/vendors/", json=vendor_data)
        
        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == vendor_data["name"]
        assert data["data"]["business_number"] == vendor_data["business_number"]
    
    def test_create_vendor_duplicate_business_number(self, test_db: Session):
        """중복 사업자번호 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor1 = create_test_vendor_model(test_db, business_number="1234567890")
        
        vendor_data = {
            "name": "다른 거래처",
            "business_number": "1234567890",  # 중복
            "representative": "김철수",
            "address": "서울시 서초구 다른로 456",
            "phone": "02-9876-5432",
            "email": "other@vendor.com",
            "bank_name": "국민은행",
            "bank_account": "123-456-789012",
            "status": "활성",
            "description": "다른 거래처입니다."
        }
        
        # When
        response = client.post("/api/v1/vendors/", json=vendor_data)
        
        # Then
        assert response.status_code == 400
        data = response.json()
        assert "이미 존재하는 사업자번호" in data["detail"]
    
    def test_get_vendors_success(self, test_db: Session):
        """거래처 목록 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor1 = create_test_vendor_model(test_db, name="거래처1")
        vendor2 = create_test_vendor_model(test_db, name="거래처2")
        
        # When
        response = client.get("/api/v1/vendors/")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) >= 2
        assert data["total"] >= 2
    
    def test_get_vendor_by_id_success(self, test_db: Session):
        """거래처 상세 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        
        # When
        response = client.get(f"/api/v1/vendors/{vendor.id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == vendor.id
        assert data["data"]["name"] == vendor.name
    
    def test_get_vendor_by_id_not_found(self, test_db: Session):
        """존재하지 않는 거래처 조회 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.get("/api/v1/vendors/non-existent-id")
        
        # Then
        assert response.status_code == 404
        data = response.json()
        assert "거래처를 찾을 수 없습니다" in data["detail"]
    
    def test_update_vendor_success(self, test_db: Session):
        """거래처 수정 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        
        update_data = {
            "name": "수정된 거래처명",
            "phone": "02-9999-8888",
            "status": "비활성"
        }
        
        # When
        response = client.put(f"/api/v1/vendors/{vendor.id}", json=update_data)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == update_data["name"]
        assert data["data"]["phone"] == update_data["phone"]
    
    def test_delete_vendor_success(self, test_db: Session):
        """거래처 삭제 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        
        # When
        response = client.delete(f"/api/v1/vendors/{vendor.id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "성공적으로 삭제되었습니다" in data["message"]
    
    def test_search_vendors_by_name(self, test_db: Session):
        """거래처명으로 검색 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor1 = create_test_vendor_model(test_db, name="건설업체 A")
        vendor2 = create_test_vendor_model(test_db, name="건설업체 B")
        vendor3 = create_test_vendor_model(test_db, name="자재업체 C")
        
        # When
        response = client.get("/api/v1/vendors/?search=건설업체")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) >= 2
        for vendor in data["data"]:
            assert "건설업체" in vendor["name"]
    
    def test_filter_vendors_by_status(self, test_db: Session):
        """거래처 상태로 필터링 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor1 = create_test_vendor_model(test_db, status="활성")
        vendor2 = create_test_vendor_model(test_db, status="비활성")
        
        # When
        response = client.get("/api/v1/vendors/?status=활성")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        for vendor in data["data"]:
            assert vendor["status"] == "활성" 