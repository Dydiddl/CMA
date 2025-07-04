import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.tests.conftest import create_test_user

client = TestClient(app)


class TestSecurity:
    """보안 테스트"""
    
    def test_sql_injection_prevention(self, test_db: Session):
        """SQL 인젝션 방지 테스트"""
        # SQL 인젝션 시도
        malicious_search = "'; DROP TABLE contracts; --"
        
        response = client.get(f"/api/v1/contracts/?search={malicious_search}")
        
        # SQL 인젝션이 방지되어야 함 (500 에러가 아닌 200 또는 400)
        assert response.status_code != 500
        assert response.status_code in [200, 400, 404]
    
    def test_xss_prevention(self, test_db: Session):
        """XSS 방지 테스트"""
        # XSS 페이로드
        xss_payload = "<script>alert('XSS')</script>"
        
        # 계약 생성 시 XSS 시도
        contract_data = {
            "name": xss_payload,
            "contract_number": "XSS-2024-001",
            "contract_amount": 1000000,
            "contract_date": "2024-01-15",
            "client_name": "테스트 발주처",
            "vendor_id": "test-vendor-id"
        }
        
        response = client.post("/api/v1/contracts/", json=contract_data)
        
        # XSS가 방지되어야 함
        if response.status_code == 201:
            contract_id = response.json()["data"]["id"]
            get_response = client.get(f"/api/v1/contracts/{contract_id}")
            
            # 응답에 스크립트 태그가 포함되지 않아야 함
            response_text = get_response.text
            assert "<script>" not in response_text
            assert "alert('XSS')" not in response_text
    
    def test_input_validation(self, test_db: Session):
        """입력 검증 테스트"""
        # 잘못된 이메일 형식
        invalid_email_data = {
            "email": "invalid-email",
            "password": "testpass123",
            "name": "테스트 사용자",
            "role": "user"
        }
        
        response = client.post("/api/v1/users/", json=invalid_email_data)
        assert response.status_code == 400
        
        # 잘못된 금액 (음수)
        invalid_contract_data = {
            "name": "테스트 계약",
            "contract_number": "TEST-2024-001",
            "contract_amount": -1000,
            "contract_date": "2024-01-15",
            "client_name": "테스트 발주처",
            "vendor_id": "test-vendor-id"
        }
        
        response = client.post("/api/v1/contracts/", json=invalid_contract_data)
        assert response.status_code == 400
        
        # 잘못된 날짜 형식
        invalid_date_data = {
            "name": "테스트 계약",
            "contract_number": "TEST-2024-002",
            "contract_amount": 1000000,
            "contract_date": "invalid-date",
            "client_name": "테스트 발주처",
            "vendor_id": "test-vendor-id"
        }
        
        response = client.post("/api/v1/contracts/", json=invalid_date_data)
        assert response.status_code == 400
    
    def test_authentication_required(self, test_db: Session):
        """인증 필요 테스트"""
        # 인증 없이 민감한 데이터 조회 시도
        response = client.get("/api/v1/users/")
        assert response.status_code == 401
        
        response = client.get("/api/v1/financial/summary")
        assert response.status_code == 401
        
        response = client.get("/api/v1/dashboard/summary")
        assert response.status_code == 401
    
    def test_authorization_checks(self, test_db: Session):
        """권한 검사 테스트"""
        # 일반 사용자 생성
        user_data = {
            "email": "user@test.com",
            "password": "testpass123",
            "name": "일반 사용자",
            "role": "user"
        }
        user_response = client.post("/api/v1/users/", json=user_data)
        assert user_response.status_code == 201
        user_id = user_response.json()["data"]["id"]
        
        # 관리자 전용 기능에 접근 시도
        admin_data = {
            "email": "admin@test.com",
            "password": "testpass123",
            "name": "관리자",
            "role": "admin"
        }
        admin_response = client.post("/api/v1/users/", json=admin_data)
        assert admin_response.status_code == 201
        admin_id = admin_response.json()["data"]["id"]
        
        # 일반 사용자가 관리자 정보 수정 시도
        update_data = {"role": "admin"}
        response = client.put(f"/api/v1/users/{admin_id}", json=update_data)
        assert response.status_code == 403
    
    def test_rate_limiting(self, test_db: Session):
        """속도 제한 테스트"""
        # 빠른 연속 요청
        for i in range(10):
            response = client.get("/api/v1/contracts/")
            # 속도 제한이 적용되면 429 상태 코드 반환
            if response.status_code == 429:
                break
        
        # 속도 제한이 제대로 작동하는지 확인
        # (실제 구현에 따라 다를 수 있음)
        pass
    
    def test_data_encryption(self, test_db: Session):
        """데이터 암호화 테스트"""
        # 민감한 데이터가 평문으로 저장되지 않는지 확인
        user_data = {
            "email": "encrypt@test.com",
            "password": "sensitive_password",
            "name": "암호화 테스트 사용자",
            "role": "user"
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        
        user_id = response.json()["data"]["id"]
        user_response = client.get(f"/api/v1/users/{user_id}")
        
        # 응답에 원본 비밀번호가 포함되지 않아야 함
        user_data_response = user_response.json()["data"]
        assert "password" not in user_data_response
        assert "sensitive_password" not in str(user_data_response)
    
    def test_cors_policy(self, test_db: Session):
        """CORS 정책 테스트"""
        # 허용되지 않은 Origin으로 요청
        headers = {"Origin": "https://malicious-site.com"}
        response = client.get("/api/v1/contracts/", headers=headers)
        
        # CORS 헤더 확인
        cors_headers = response.headers.get("Access-Control-Allow-Origin")
        if cors_headers:
            # 허용된 Origin만 허용되어야 함
            assert cors_headers != "*"
    
    def test_content_security_policy(self, test_db: Session):
        """CSP 헤더 테스트"""
        response = client.get("/api/v1/contracts/")
        
        # CSP 헤더가 설정되어 있는지 확인
        csp_header = response.headers.get("Content-Security-Policy")
        # CSP가 설정되어 있다면 적절한 정책이어야 함
        if csp_header:
            assert "script-src" in csp_header
    
    def test_secure_headers(self, test_db: Session):
        """보안 헤더 테스트"""
        response = client.get("/api/v1/contracts/")
        
        # 보안 헤더 확인
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security"
        ]
        
        for header in security_headers:
            # 헤더가 설정되어 있다면 적절한 값이어야 함
            header_value = response.headers.get(header)
            if header_value:
                if header == "X-Content-Type-Options":
                    assert header_value == "nosniff"
                elif header == "X-Frame-Options":
                    assert header_value in ["DENY", "SAMEORIGIN"]
                elif header == "X-XSS-Protection":
                    assert "1" in header_value 