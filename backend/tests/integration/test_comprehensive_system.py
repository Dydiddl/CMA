import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user, create_test_vendor, create_test_contract

client = TestClient(app)


class TestComprehensiveSystem:
    """종합 시스템 통합 테스트"""
    
    def test_full_workflow_contract_management(self, test_db: Session):
        """전체 계약 관리 워크플로우 테스트"""
        # 1. 사용자 생성
        user_data = {
            "email": "workflow@test.com",
            "password": "testpass123",
            "name": "워크플로우 테스트 사용자",
            "role": "admin"
        }
        user_response = client.post("/api/v1/users/", json=user_data)
        assert user_response.status_code == 201
        user_id = user_response.json()["data"]["id"]
        
        # 2. 거래처 생성
        vendor_data = {
            "name": "워크플로우 테스트 거래처",
            "business_number": "123-45-67891",
            "representative": "홍길동",
            "contact": "010-1234-5678",
            "email": "vendor@test.com",
            "address": "서울시 강남구 테스트로 123",
            "vendor_type": "건설업"
        }
        vendor_response = client.post("/api/v1/vendors/", json=vendor_data)
        assert vendor_response.status_code == 201
        vendor_id = vendor_response.json()["data"]["id"]
        
        # 3. 계약 생성
        contract_data = {
            "name": "워크플로우 테스트 계약",
            "contract_number": "CON-WF-2024-001",
            "contract_amount": 50000000,
            "contract_date": "2024-01-15",
            "start_date": "2024-02-01",
            "end_date": "2024-12-31",
            "client_name": "테스트 발주처",
            "client_contact": "010-9876-5432",
            "status": "진행중",
            "description": "워크플로우 테스트용 계약",
            "vendor_id": vendor_id
        }
        contract_response = client.post("/api/v1/contracts/", json=contract_data)
        assert contract_response.status_code == 201
        contract_id = contract_response.json()["data"]["id"]
        
        # 4. 재무 기록 생성
        financial_data = {
            "contract_id": contract_id,
            "record_type": "수입",
            "amount": 10000000,
            "description": "계약금 지급",
            "record_date": "2024-01-15"
        }
        financial_response = client.post("/api/v1/financial/", json=financial_data)
        assert financial_response.status_code == 201
        
        # 5. 노무 기록 생성
        labor_data = {
            "contract_id": contract_id,
            "worker_name": "김철수",
            "position": "기술자",
            "work_date": "2024-02-01",
            "work_hours": 8,
            "hourly_rate": 20000,
            "description": "기초공사"
        }
        labor_response = client.post("/api/v1/labor/", json=labor_data)
        assert labor_response.status_code == 201
        
        # 6. 대시보드 요약 확인
        dashboard_response = client.get("/api/v1/dashboard/summary")
        assert dashboard_response.status_code == 200
        dashboard_data = dashboard_response.json()["data"]
        assert dashboard_data["total_contracts"] >= 1
        assert dashboard_data["total_vendors"] >= 1
        assert dashboard_data["total_users"] >= 1
        
        # 7. 계약 상태 업데이트
        update_data = {"status": "완료"}
        update_response = client.put(f"/api/v1/contracts/{contract_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["data"]["status"] == "완료"
        
        # 8. 데이터 삭제 (정리)
        client.delete(f"/api/v1/contracts/{contract_id}")
        client.delete(f"/api/v1/vendors/{vendor_id}")
        client.delete(f"/api/v1/users/{user_id}")
    
    def test_data_consistency_across_modules(self, test_db: Session):
        """모듈 간 데이터 일관성 테스트"""
        # 1. 기본 데이터 생성
        user = create_test_user(test_db)
        vendor = create_test_vendor(test_db)
        contract = create_test_contract(test_db, vendor_id=vendor.id)
        
        # 2. 재무 데이터 생성
        financial_data = {
            "contract_id": contract.id,
            "record_type": "수입",
            "amount": 5000000,
            "description": "테스트 수입",
            "record_date": "2024-01-15"
        }
        financial_response = client.post("/api/v1/financial/", json=financial_data)
        assert financial_response.status_code == 201
        
        # 3. 노무 데이터 생성
        labor_data = {
            "contract_id": contract.id,
            "worker_name": "이영희",
            "position": "기술자",
            "work_date": "2024-01-15",
            "work_hours": 8,
            "hourly_rate": 15000,
            "description": "테스트 작업"
        }
        labor_response = client.post("/api/v1/labor/", json=labor_data)
        assert labor_response.status_code == 201
        
        # 4. 각 모듈에서 데이터 확인
        # 계약 조회
        contract_response = client.get(f"/api/v1/contracts/{contract.id}")
        assert contract_response.status_code == 200
        
        # 재무 요약
        financial_summary = client.get("/api/v1/financial/summary")
        assert financial_summary.status_code == 200
        
        # 노무 요약
        labor_summary = client.get("/api/v1/labor/summary")
        assert labor_summary.status_code == 200
        
        # 대시보드 통합 확인
        dashboard_summary = client.get("/api/v1/dashboard/summary")
        assert dashboard_summary.status_code == 200
    
    def test_error_handling_and_validation(self, test_db: Session):
        """오류 처리 및 검증 테스트"""
        # 1. 잘못된 데이터로 계약 생성 시도
        invalid_contract_data = {
            "name": "",  # 빈 이름
            "contract_number": "INVALID",
            "contract_amount": -1000,  # 음수 금액
            "contract_date": "2024-01-15",
            "client_name": "테스트 발주처",
            "vendor_id": "non-existent-vendor-id"
        }
        
        response = client.post("/api/v1/contracts/", json=invalid_contract_data)
        assert response.status_code == 400
        
        # 2. 존재하지 않는 리소스 조회
        response = client.get("/api/v1/contracts/non-existent-id")
        assert response.status_code == 404
        
        # 3. 잘못된 재무 데이터
        invalid_financial_data = {
            "contract_id": "non-existent-contract-id",
            "record_type": "잘못된_타입",
            "amount": -5000,
            "description": "테스트",
            "record_date": "2024-01-15"
        }
        
        response = client.post("/api/v1/financial/", json=invalid_financial_data)
        assert response.status_code == 400
    
    def test_performance_under_load(self, test_db: Session):
        """부하 하에서의 성능 테스트"""
        # 1. 대량 데이터 생성
        vendor = create_test_vendor(test_db)
        
        # 여러 계약 생성
        for i in range(10):
            contract_data = {
                "name": f"성능 테스트 계약 {i}",
                "contract_number": f"PERF-2024-{i:03d}",
                "contract_amount": 1000000 + (i * 100000),
                "contract_date": "2024-01-15",
                "client_name": f"테스트 발주처 {i}",
                "vendor_id": vendor.id
            }
            response = client.post("/api/v1/contracts/", json=contract_data)
            assert response.status_code == 201
        
        # 2. 대량 데이터 조회 성능 테스트
        import time
        start_time = time.time()
        
        response = client.get("/api/v1/contracts/?limit=100")
        assert response.status_code == 200
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # 응답 시간이 1초 이내여야 함
        assert response_time < 1.0
        
        # 3. 대시보드 성능 테스트
        start_time = time.time()
        
        response = client.get("/api/v1/dashboard/summary")
        assert response.status_code == 200
        
        end_time = time.time()
        dashboard_response_time = end_time - start_time
        
        # 대시보드 응답 시간이 2초 이내여야 함
        assert dashboard_response_time < 2.0
    
    def test_concurrent_operations(self, test_db: Session):
        """동시 작업 테스트"""
        import threading
        import time
        
        vendor = create_test_vendor(test_db)
        results = []
        
        def create_contract(thread_id):
            """스레드별 계약 생성"""
            contract_data = {
                "name": f"동시 테스트 계약 {thread_id}",
                "contract_number": f"CONC-2024-{thread_id:03d}",
                "contract_amount": 1000000,
                "contract_date": "2024-01-15",
                "client_name": f"동시 테스트 발주처 {thread_id}",
                "vendor_id": vendor.id
            }
            response = client.post("/api/v1/contracts/", json=contract_data)
            results.append(response.status_code)
        
        # 5개 스레드에서 동시에 계약 생성
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_contract, args=(i,))
            threads.append(thread)
            thread.start()
        
        # 모든 스레드 완료 대기
        for thread in threads:
            thread.join()
        
        # 모든 요청이 성공했는지 확인
        assert all(status_code == 201 for status_code in results)
    
    def test_data_integrity_constraints(self, test_db: Session):
        """데이터 무결성 제약 조건 테스트"""
        # 1. 중복 계약번호 테스트
        vendor = create_test_vendor(test_db)
        
        contract_data = {
            "name": "중복 테스트 계약",
            "contract_number": "DUPL-2024-001",
            "contract_amount": 1000000,
            "contract_date": "2024-01-15",
            "client_name": "테스트 발주처",
            "vendor_id": vendor.id
        }
        
        # 첫 번째 계약 생성
        response1 = client.post("/api/v1/contracts/", json=contract_data)
        assert response1.status_code == 201
        
        # 동일한 계약번호로 두 번째 계약 생성 시도
        response2 = client.post("/api/v1/contracts/", json=contract_data)
        assert response2.status_code == 400
        assert "이미 존재하는 계약번호" in response2.json()["detail"]
        
        # 2. 외래키 제약 조건 테스트
        invalid_contract_data = {
            "name": "외래키 테스트 계약",
            "contract_number": "FK-2024-001",
            "contract_amount": 1000000,
            "contract_date": "2024-01-15",
            "client_name": "테스트 발주처",
            "vendor_id": "non-existent-vendor-id"
        }
        
        response = client.post("/api/v1/contracts/", json=invalid_contract_data)
        assert response.status_code == 400 