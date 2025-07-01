#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 데스크톱 앱용 API 클라이언트
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class APIClient:
    """백엔드 API와 통신하는 클라이언트"""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.access_token = None
        
        # 기본 헤더 설정
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def set_auth_token(self, token: str):
        """인증 토큰 설정"""
        self.access_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def clear_auth_token(self):
        """인증 토큰 제거"""
        self.access_token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """API 요청 실행"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            # 응답 상태 코드 확인
            response.raise_for_status()
            
            # JSON 응답 파싱
            if response.content:
                return response.json()
            else:
                return {"status": "success", "message": "요청이 성공적으로 처리되었습니다."}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API 요청 실패: {e}")
            raise APIError(f"API 요청 실패: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            raise APIError(f"응답 파싱 실패: {e}")
    
    # 인증 관련 API
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """사용자 로그인"""
        data = {
            "email": email,
            "password": password
        }
        return self._make_request("POST", "/api/v1/auth/login", json=data)
    
    def register(self, email: str, password: str, name: str) -> Dict[str, Any]:
        """사용자 회원가입"""
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        return self._make_request("POST", "/api/v1/auth/register", json=data)
    
    def get_current_user(self) -> Dict[str, Any]:
        """현재 사용자 정보 조회"""
        return self._make_request("GET", "/api/v1/auth/me")
    
    # 대시보드 관련 API
    def get_dashboard_data(self) -> Dict[str, Any]:
        """대시보드 데이터 조회"""
        return self._make_request("GET", "/api/v1/dashboard/")
    
    def get_contract_summary(self) -> Dict[str, Any]:
        """계약 요약 정보 조회"""
        return self._make_request("GET", "/api/v1/dashboard/contracts/summary")
    
    def get_financial_summary(self) -> Dict[str, Any]:
        """재무 요약 정보 조회"""
        return self._make_request("GET", "/api/v1/dashboard/financial/summary")
    
    def get_labor_summary(self) -> Dict[str, Any]:
        """노무 요약 정보 조회"""
        return self._make_request("GET", "/api/v1/dashboard/labor/summary")
    
    def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 조회"""
        return self._make_request("GET", "/api/v1/dashboard/system/status")
    
    def get_recent_activities(self, limit: int = 10) -> Dict[str, Any]:
        """최근 활동 조회"""
        return self._make_request("GET", f"/api/v1/dashboard/recent-activities?limit={limit}")
    
    # 계약 관련 API
    def get_contracts(self, skip: int = 0, limit: int = 10, search: str = None, status: str = None) -> Dict[str, Any]:
        """계약 목록 조회"""
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        if status:
            params["status"] = status
        
        return self._make_request("GET", "/api/v1/contracts/", params=params)
    
    def get_contract(self, contract_id: str) -> Dict[str, Any]:
        """계약 상세 조회"""
        return self._make_request("GET", f"/api/v1/contracts/{contract_id}")
    
    def create_contract(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """계약 생성"""
        return self._make_request("POST", "/api/v1/contracts/", json=contract_data)
    
    def update_contract(self, contract_id: str, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """계약 수정"""
        return self._make_request("PUT", f"/api/v1/contracts/{contract_id}", json=contract_data)
    
    def delete_contract(self, contract_id: str) -> Dict[str, Any]:
        """계약 삭제"""
        return self._make_request("DELETE", f"/api/v1/contracts/{contract_id}")
    
    # 재무 관련 API
    def get_financial_records(self, skip: int = 0, limit: int = 10, type_filter: str = None) -> Dict[str, Any]:
        """재무 기록 조회"""
        params = {"skip": skip, "limit": limit}
        if type_filter:
            params["type"] = type_filter
        
        return self._make_request("GET", "/api/v1/finance/", params=params)
    
    def create_financial_record(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """재무 기록 생성"""
        return self._make_request("POST", "/api/v1/finance/", json=financial_data)
    
    def update_financial_record(self, record_id: str, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """재무 기록 수정"""
        return self._make_request("PUT", f"/api/v1/finance/{record_id}", json=financial_data)
    
    def delete_financial_record(self, record_id: str) -> Dict[str, Any]:
        """재무 기록 삭제"""
        return self._make_request("DELETE", f"/api/v1/finance/{record_id}")
    
    # 노무 관련 API
    def get_labor_records(self, skip: int = 0, limit: int = 10, worker_id: str = None) -> Dict[str, Any]:
        """노무 기록 조회"""
        params = {"skip": skip, "limit": limit}
        if worker_id:
            params["worker_id"] = worker_id
        
        return self._make_request("GET", "/api/v1/labor/", params=params)
    
    def get_workers(self, skip: int = 0, limit: int = 10, search: str = None) -> Dict[str, Any]:
        """근로자 목록 조회"""
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        
        return self._make_request("GET", "/api/v1/labor/workers", params=params)
    
    def create_labor_record(self, labor_data: Dict[str, Any]) -> Dict[str, Any]:
        """노무 기록 생성"""
        return self._make_request("POST", "/api/v1/labor/", json=labor_data)
    
    def update_labor_record(self, record_id: str, labor_data: Dict[str, Any]) -> Dict[str, Any]:
        """노무 기록 수정"""
        return self._make_request("PUT", f"/api/v1/labor/{record_id}", json=labor_data)
    
    def delete_labor_record(self, record_id: str) -> Dict[str, Any]:
        """노무 기록 삭제"""
        return self._make_request("DELETE", f"/api/v1/labor/{record_id}")
    
    # 거래처 관련 API
    def get_vendors(self, skip: int = 0, limit: int = 10, search: str = None) -> Dict[str, Any]:
        """거래처 목록 조회"""
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        
        return self._make_request("GET", "/api/v1/vendors/", params=params)
    
    def create_vendor(self, vendor_data: Dict[str, Any]) -> Dict[str, Any]:
        """거래처 생성"""
        return self._make_request("POST", "/api/v1/vendors/", json=vendor_data)
    
    def update_vendor(self, vendor_id: str, vendor_data: Dict[str, Any]) -> Dict[str, Any]:
        """거래처 수정"""
        return self._make_request("PUT", f"/api/v1/vendors/{vendor_id}", json=vendor_data)
    
    def delete_vendor(self, vendor_id: str) -> Dict[str, Any]:
        """거래처 삭제"""
        return self._make_request("DELETE", f"/api/v1/vendors/{vendor_id}")
    
    # ASCR 관련 API
    def process_pdf(self, file_path: str, year: int) -> Dict[str, Any]:
        """PDF 처리 (ASCR 모듈)"""
        # 파일 업로드를 위한 multipart/form-data 요청
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'year': year}
            return self._make_request("POST", "/api/v1/ascr/process-pdf", files=files, data=data)
    
    def extract_toc(self, file_path: str, year: int) -> Dict[str, Any]:
        """목차 추출 (ASCR 모듈)"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'year': year}
            return self._make_request("POST", "/api/v1/ascr/extract-toc", files=files, data=data)
    
    def close(self):
        """세션 종료"""
        self.session.close()


class APIError(Exception):
    """API 관련 예외"""
    pass


# 싱글톤 패턴으로 API 클라이언트 인스턴스 관리
_api_client = None

def get_api_client() -> APIClient:
    """API 클라이언트 인스턴스 반환"""
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client

def set_api_client(client: APIClient):
    """API 클라이언트 인스턴스 설정"""
    global _api_client
    _api_client = client 