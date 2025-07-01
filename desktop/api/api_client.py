#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 앱 API 클라이언트
백엔드 서버와의 통신을 담당
"""

import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """API 클라이언트 클래스"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """API 요청 실행"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            logger.error(f"서버 연결 실패: {url}")
            return {"status": "error", "message": "서버에 연결할 수 없습니다"}
        except requests.exceptions.RequestException as e:
            logger.error(f"API 요청 실패: {e}")
            return {"status": "error", "message": f"API 요청 실패: {str(e)}"}
        except json.JSONDecodeError:
            logger.error(f"JSON 파싱 실패: {response.text}")
            return {"status": "error", "message": "응답 파싱 실패"}
    
    def health_check(self) -> Dict[str, Any]:
        """서버 상태 확인"""
        return self._make_request('GET', '/health')
    
    def get_contracts(self) -> Dict[str, Any]:
        """계약 목록 조회"""
        return self._make_request('GET', '/api/v1/contracts')
    
    def get_financial(self) -> Dict[str, Any]:
        """재무 정보 조회"""
        return self._make_request('GET', '/api/v1/financial')
    
    def get_labor(self) -> Dict[str, Any]:
        """노무 정보 조회"""
        return self._make_request('GET', '/api/v1/labor')
    
    def test_connection(self) -> bool:
        """연결 테스트"""
        try:
            result = self.health_check()
            return result.get('status') == 'healthy'
        except Exception:
            return False

# 전역 API 클라이언트 인스턴스
api_client = APIClient() 