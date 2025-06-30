#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
계약 API 통합 테스트
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.contract import Contract
from app.tests.conftest import get_test_db

client = TestClient(app)


class TestContractAPI:
    """계약 API 테스트 클래스"""
    
    def test_create_contract_success(self, test_db: Session, sample_contract_data: dict):
        """계약 생성 성공 테스트"""
        response = client.post("/api/v1/contracts/", json=sample_contract_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == sample_contract_data["name"]
        assert data["data"]["contract_number"] == sample_contract_data["contract_number"]
    
    def test_create_contract_duplicate_number(self, test_db: Session, sample_contract_data: dict):
        """중복 계약번호 테스트"""
        # 첫 번째 계약 생성
        client.post("/api/v1/contracts/", json=sample_contract_data)
        
        # 동일한 계약번호로 두 번째 계약 생성 시도
        sample_contract_data["name"] = "테스트 계약 2"
        response = client.post("/api/v1/contracts/", json=sample_contract_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "이미 존재하는 계약번호" in data["detail"]
    
    def test_create_contract_invalid_data(self, test_db: Session):
        """유효하지 않은 데이터로 계약 생성 테스트"""
        # 필수 필드 누락
        contract_data = {
            "name": "",  # 빈 문자열
            "contract_amount": -1000,  # 음수
            "contract_date": "2024-01-15T00:00:00"
        }
        
        response = client.post("/api/v1/contracts/", json=contract_data)
        assert response.status_code == 422  # Validation Error
    
    def test_get_contracts_success(self, test_db: Session):
        """계약 목록 조회 성공 테스트"""
        response = client.get("/api/v1/contracts/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    def test_get_contracts_with_pagination(self, test_db: Session):
        """페이징을 포함한 계약 목록 조회 테스트"""
        response = client.get("/api/v1/contracts/?skip=0&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data["size"] == 5
        assert data["page"] == 1
    
    def test_get_contracts_with_search(self, test_db: Session):
        """검색을 포함한 계약 목록 조회 테스트"""
        response = client.get("/api/v1/contracts/?search=테스트")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_get_contracts_with_status_filter(self, test_db: Session):
        """상태 필터를 포함한 계약 목록 조회 테스트"""
        response = client.get("/api/v1/contracts/?status=진행중")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_get_contract_success(self, test_db: Session, sample_contract_data: dict):
        """계약 상세 조회 성공 테스트"""
        # 먼저 계약 생성
        create_response = client.post("/api/v1/contracts/", json=sample_contract_data)
        contract_id = create_response.json()["data"]["id"]
        
        # 계약 상세 조회
        response = client.get(f"/api/v1/contracts/{contract_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == contract_id
        assert data["data"]["name"] == sample_contract_data["name"]
    
    def test_get_contract_not_found(self, test_db: Session):
        """존재하지 않는 계약 조회 테스트"""
        response = client.get("/api/v1/contracts/non-existent-id")
        
        assert response.status_code == 404
        data = response.json()
        assert "계약을 찾을 수 없습니다" in data["detail"]
    
    def test_update_contract_success(self, test_db: Session, sample_contract_data: dict):
        """계약 수정 성공 테스트"""
        # 먼저 계약 생성
        create_response = client.post("/api/v1/contracts/", json=sample_contract_data)
        contract_id = create_response.json()["data"]["id"]
        
        # 계약 수정
        update_data = {
            "name": "수정된 계약명",
            "contract_amount": 2000000
        }
        response = client.put(f"/api/v1/contracts/{contract_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == update_data["name"]
        assert data["data"]["contract_amount"] == update_data["contract_amount"]
    
    def test_update_contract_not_found(self, test_db: Session):
        """존재하지 않는 계약 수정 테스트"""
        update_data = {
            "name": "수정된 계약명"
        }
        response = client.put("/api/v1/contracts/non-existent-id", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "계약을 찾을 수 없습니다" in data["detail"]
    
    def test_update_contract_invalid_data(self, test_db: Session, sample_contract_data: dict):
        """유효하지 않은 데이터로 계약 수정 테스트"""
        # 먼저 계약 생성
        create_response = client.post("/api/v1/contracts/", json=sample_contract_data)
        contract_id = create_response.json()["data"]["id"]
        
        # 유효하지 않은 데이터로 수정
        update_data = {
            "contract_amount": -1000  # 음수
        }
        response = client.put(f"/api/v1/contracts/{contract_id}", json=update_data)
        
        assert response.status_code == 422  # Validation Error
    
    def test_delete_contract_success(self, test_db: Session, sample_contract_data: dict):
        """계약 삭제 성공 테스트"""
        # 먼저 계약 생성
        create_response = client.post("/api/v1/contracts/", json=sample_contract_data)
        contract_id = create_response.json()["data"]["id"]
        
        # 계약 삭제
        response = client.delete(f"/api/v1/contracts/{contract_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "계약이 성공적으로 삭제되었습니다" in data["message"]
    
    def test_delete_contract_not_found(self, test_db: Session):
        """존재하지 않는 계약 삭제 테스트"""
        response = client.delete("/api/v1/contracts/non-existent-id")
        
        assert response.status_code == 404
        data = response.json()
        assert "계약을 찾을 수 없습니다" in data["detail"]


class TestContractValidation:
    """계약 검증 테스트 클래스"""
    
    def test_contract_date_validation(self, test_db: Session):
        """계약 날짜 검증 테스트"""
        contract_data = {
            "name": "테스트 계약",
            "contract_number": "CON-2024-005",
            "contract_amount": 1000000,
            "contract_date": "2024-01-15T00:00:00",
            "client_name": "테스트 발주처",
            "vendor_id": "test-vendor-id",
            "start_date": "2024-02-01T00:00:00",
            "end_date": "2024-01-01T00:00:00"  # 시작일보다 이전
        }
        
        response = client.post("/api/v1/contracts/", json=contract_data)
        assert response.status_code == 422  # Validation Error
    
    def test_contract_amount_validation(self, test_db: Session):
        """계약 금액 검증 테스트"""
        contract_data = {
            "name": "테스트 계약",
            "contract_number": "CON-2024-006",
            "contract_amount": 0,  # 0원
            "contract_date": "2024-01-15T00:00:00",
            "client_name": "테스트 발주처",
            "vendor_id": "test-vendor-id"
        }
        
        response = client.post("/api/v1/contracts/", json=contract_data)
        assert response.status_code == 422  # Validation Error
    
    def test_required_fields_validation(self, test_db: Session):
        """필수 필드 검증 테스트"""
        contract_data = {
            "contract_amount": 1000000,
            "contract_date": "2024-01-15T00:00:00"
            # name, contract_number, client_name, vendor_id 누락
        }
        
        response = client.post("/api/v1/contracts/", json=contract_data)
        assert response.status_code == 422  # Validation Error 