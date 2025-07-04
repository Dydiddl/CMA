from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user_model, create_test_contract_model, create_test_vendor_model

client = TestClient(app)


class TestLaborAPI:
    """노무 API 테스트"""
    
    def test_create_labor_record_success(self, test_db: Session):
        """노무 기록 생성 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        labor_data = {
            "contract_id": contract.id,
            "name": "홍길동",
            "phone": "010-1234-5678",
            "id_number": "900101-1234567",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "daily_wage": 20000,
            "status": "재직"
        }
        
        # When
        response = client.post("/api/v1/labor/", json=labor_data)
        
        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == labor_data["name"]
        assert data["data"]["daily_wage"] == labor_data["daily_wage"]
    
    def test_get_labor_records_success(self, test_db: Session):
        """노무 기록 목록 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # When
        response = client.get("/api/v1/labor/")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "total" in data
    
    def test_get_labor_record_by_id_success(self, test_db: Session):
        """노무 기록 상세 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # 노무 기록 생성
        labor_data = {
            "contract_id": contract.id,
            "name": "홍길동",
            "phone": "010-1234-5678",
            "id_number": "900101-1234567",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "daily_wage": 20000,
            "status": "재직"
        }
        create_response = client.post("/api/v1/labor/", json=labor_data)
        record_id = create_response.json()["data"]["id"]
        
        # When
        response = client.get(f"/api/v1/labor/{record_id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == record_id
    
    def test_update_labor_record_success(self, test_db: Session):
        """노무 기록 수정 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # 노무 기록 생성
        labor_data = {
            "contract_id": contract.id,
            "name": "홍길동",
            "phone": "010-1234-5678",
            "id_number": "900101-1234567",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "daily_wage": 20000,
            "status": "재직"
        }
        create_response = client.post("/api/v1/labor/", json=labor_data)
        record_id = create_response.json()["data"]["id"]
        
        update_data = {
            "daily_wage": 25000,
            "status": "퇴직"
        }
        
        # When
        response = client.put(f"/api/v1/labor/{record_id}", json=update_data)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["daily_wage"] == update_data["daily_wage"]
        assert data["data"]["status"] == update_data["status"]
    
    def test_delete_labor_record_success(self, test_db: Session):
        """노무 기록 삭제 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # 노무 기록 생성
        labor_data = {
            "contract_id": contract.id,
            "name": "홍길동",
            "phone": "010-1234-5678",
            "id_number": "900101-1234567",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "daily_wage": 20000,
            "status": "재직"
        }
        create_response = client.post("/api/v1/labor/", json=labor_data)
        record_id = create_response.json()["data"]["id"]
        
        # When
        response = client.delete(f"/api/v1/labor/{record_id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "성공적으로 삭제되었습니다" in data["message"]
    
    def test_get_labor_summary_success(self, test_db: Session):
        """노무 요약 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.get("/api/v1/labor/summary")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_workers" in data["data"]
        assert "total_cost" in data["data"]
        assert "active_workers" in data["data"]
    
    def test_get_labor_reports_success(self, test_db: Session):
        """노무 보고서 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.get("/api/v1/labor/reports")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "reports" in data["data"]
        assert isinstance(data["data"]["reports"], list) 