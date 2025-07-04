from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user, create_test_contract, create_test_vendor

client = TestClient(app)


class TestDashboardAPI:
    """대시보드 API 테스트"""
    
    def test_get_dashboard_summary_success(self, test_db: Session):
        """대시보드 요약 정보 조회 성공 테스트"""
        # Given
        user = create_test_user(test_db)
        vendor = create_test_vendor(test_db)
        contract1 = create_test_contract(test_db, vendor_id=vendor.id)
        contract2 = create_test_contract(test_db, vendor_id=vendor.id)
        
        # When
        response = client.get("/api/v1/dashboard/summary")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_contracts" in data["data"]
        assert "total_vendors" in data["data"]
        assert "total_users" in data["data"]
        assert "recent_activities" in data["data"]
    
    def test_get_dashboard_contracts_overview(self, test_db: Session):
        """계약 현황 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        vendor = create_test_vendor(test_db)
        contract1 = create_test_contract(test_db, vendor_id=vendor.id, status="진행중")
        contract2 = create_test_contract(test_db, vendor_id=vendor.id, status="완료")
        
        # When
        response = client.get("/api/v1/dashboard/contracts-overview")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "contracts_by_status" in data["data"]
        assert "monthly_contracts" in data["data"]
    
    def test_get_dashboard_financial_overview(self, test_db: Session):
        """재무 현황 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        vendor = create_test_vendor(test_db)
        contract1 = create_test_contract(test_db, vendor_id=vendor.id, contract_amount=1000000)
        contract2 = create_test_contract(test_db, vendor_id=vendor.id, contract_amount=2000000)
        
        # When
        response = client.get("/api/v1/dashboard/financial-overview")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_contract_amount" in data["data"]
        assert "monthly_revenue" in data["data"]
        assert "financial_summary" in data["data"]
    
    def test_get_dashboard_labor_overview(self, test_db: Session):
        """노무 현황 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        
        # When
        response = client.get("/api/v1/dashboard/labor-overview")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_laborers" in data["data"]
        assert "labor_cost_summary" in data["data"]
        assert "monthly_labor_hours" in data["data"]
    
    def test_get_dashboard_recent_activities(self, test_db: Session):
        """최근 활동 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        
        # When
        response = client.get("/api/v1/dashboard/recent-activities")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "activities" in data["data"]
        assert isinstance(data["data"]["activities"], list)
    
    def test_get_dashboard_performance_metrics(self, test_db: Session):
        """성능 지표 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        
        # When
        response = client.get("/api/v1/dashboard/performance-metrics")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "api_response_time" in data["data"]
        assert "database_performance" in data["data"]
        assert "system_health" in data["data"]
    
    def test_get_dashboard_charts_data(self, test_db: Session):
        """차트 데이터 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        vendor = create_test_vendor(test_db)
        contract1 = create_test_contract(test_db, vendor_id=vendor.id)
        contract2 = create_test_contract(test_db, vendor_id=vendor.id)
        
        # When
        response = client.get("/api/v1/dashboard/charts-data")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "contracts_chart" in data["data"]
        assert "financial_chart" in data["data"]
        assert "labor_chart" in data["data"]
    
    def test_get_dashboard_notifications(self, test_db: Session):
        """알림 조회 테스트"""
        # Given
        user = create_test_user(test_db)
        
        # When
        response = client.get("/api/v1/dashboard/notifications")
        
        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "notifications" in data["data"]
        assert isinstance(data["data"]["notifications"], list) 