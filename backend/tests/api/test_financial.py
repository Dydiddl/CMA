from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user_model, create_test_contract_model, create_test_vendor_model

client = TestClient(app)


class TestFinancialAPI:
    """재무 API 테스트"""
    
    def test_create_financial_record_success(self, test_db: Session):
        """재무 기록 생성 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        financial_data = {
            "contract_id": contract.id,
            "amount": 1000000,
            "type": "수입",
            "category": "계약금",
            "description": "계약금 지급",
            "payment_method": "계좌이체",
            "status": "지급완료",
            "transaction_date": "2024-01-15"
        }
        
        # When
        response = client.post("/api/v1/financial/", json=financial_data)
        
        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["amount"] == financial_data["amount"]
        assert data["data"]["type"] == financial_data["type"]
    
    def test_get_financial_records_success(self, test_db: Session):
        """재무 기록 목록 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # When
        response = client.get("/api/v1/financial/")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "total" in data
    
    def test_get_financial_record_by_id_success(self, test_db: Session):
        """재무 기록 상세 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # 재무 기록 생성
        financial_data = {
            "contract_id": contract.id,
            "amount": 1000000,
            "type": "수입",
            "category": "계약금",
            "description": "테스트 기록",
            "payment_method": "계좌이체",
            "status": "지급완료",
            "transaction_date": "2024-01-15"
        }
        create_response = client.post("/api/v1/financial/", json=financial_data)
        record_id = create_response.json()["data"]["id"]
        
        # When
        response = client.get(f"/api/v1/financial/{record_id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == record_id
    
    def test_update_financial_record_success(self, test_db: Session):
        """재무 기록 수정 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # 재무 기록 생성
        financial_data = {
            "contract_id": contract.id,
            "amount": 1000000,
            "type": "수입",
            "category": "계약금",
            "description": "테스트 기록",
            "payment_method": "계좌이체",
            "status": "지급완료",
            "transaction_date": "2024-01-15"
        }
        create_response = client.post("/api/v1/financial/", json=financial_data)
        record_id = create_response.json()["data"]["id"]
        
        update_data = {
            "amount": 1500000,
            "description": "수정된 기록",
            "status": "지급대기"
        }
        
        # When
        response = client.put(f"/api/v1/financial/{record_id}", json=update_data)
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["amount"] == update_data["amount"]
        assert data["data"]["description"] == update_data["description"]
    
    def test_delete_financial_record_success(self, test_db: Session):
        """재무 기록 삭제 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        vendor = create_test_vendor_model(test_db)
        contract = create_test_contract_model(test_db, vendor_id=vendor.id)
        
        # 재무 기록 생성
        financial_data = {
            "contract_id": contract.id,
            "amount": 1000000,
            "type": "수입",
            "category": "계약금",
            "description": "테스트 기록",
            "payment_method": "계좌이체",
            "status": "지급완료",
            "transaction_date": "2024-01-15"
        }
        create_response = client.post("/api/v1/financial/", json=financial_data)
        record_id = create_response.json()["data"]["id"]
        
        # When
        response = client.delete(f"/api/v1/financial/{record_id}")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "성공적으로 삭제되었습니다" in data["message"]
    
    def test_get_financial_summary_success(self, test_db: Session):
        """재무 요약 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.get("/api/v1/financial/summary")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_income" in data["data"]
        assert "total_expense" in data["data"]
        assert "net_profit" in data["data"]
    
    def test_get_financial_reports_success(self, test_db: Session):
        """재무 보고서 조회 성공 테스트"""
        # Given
        user = create_test_user_model(test_db)
        
        # When
        response = client.get("/api/v1/financial/reports")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "reports" in data["data"]
        assert isinstance(data["data"]["reports"], list) 