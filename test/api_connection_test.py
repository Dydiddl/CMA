#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 연동 테스트 스크립트
백엔드 서버와의 연결을 테스트
"""

import sys
import os
from pathlib import Path
sys.path.append(Path(Path(__file__).parent, 'desktop'))

from desktop.api.api_client import APIClient
import time

def test_api_connection():
    """API 연결 테스트"""
    print("=== CMA API 연동 테스트 ===")
    
    # API 클라이언트 생성
    api_client = APIClient("http://localhost:8000")
    
    # 1. 서버 상태 확인
    print("\n1. 서버 상태 확인...")
    try:
        health_result = api_client.health_check()
        print(f"   결과: {health_result}")
        if health_result.get('status') == 'healthy':
            print("   ✅ 서버가 정상적으로 실행 중입니다.")
        else:
            print("   ❌ 서버 상태가 비정상입니다.")
            return False
    except Exception as e:
        print(f"   ❌ 서버 연결 실패: {e}")
        return False
    
    # 2. 계약 목록 조회 테스트
    print("\n2. 계약 목록 조회 테스트...")
    try:
        contracts_result = api_client.get_contracts()
        print(f"   결과: {contracts_result}")
        if contracts_result.get('status') == 'success':
            print("   ✅ 계약 목록 조회 성공")
        else:
            print("   ❌ 계약 목록 조회 실패")
    except Exception as e:
        print(f"   ❌ 계약 목록 조회 오류: {e}")
    
    # 3. 재무 정보 조회 테스트
    print("\n3. 재무 정보 조회 테스트...")
    try:
        financial_result = api_client.get_financial()
        print(f"   결과: {financial_result}")
        if financial_result.get('status') == 'success':
            print("   ✅ 재무 정보 조회 성공")
        else:
            print("   ❌ 재무 정보 조회 실패")
    except Exception as e:
        print(f"   ❌ 재무 정보 조회 오류: {e}")
    
    # 4. 노무 정보 조회 테스트
    print("\n4. 노무 정보 조회 테스트...")
    try:
        labor_result = api_client.get_labor()
        print(f"   결과: {labor_result}")
        if labor_result.get('status') == 'success':
            print("   ✅ 노무 정보 조회 성공")
        else:
            print("   ❌ 노무 정보 조회 실패")
    except Exception as e:
        print(f"   ❌ 노무 정보 조회 오류: {e}")
    
    print("\n=== 테스트 완료 ===")
    return True

if __name__ == "__main__":
    test_api_connection() 