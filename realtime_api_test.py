#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실시간 API 연동 테스트
GUI와 백엔드 간의 실시간 통신을 테스트
"""

import sys
import os
import time
import json
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'desktop'))

from desktop.api.api_client import APIClient

class RealtimeAPITester:
    """실시간 API 테스터"""
    
    def __init__(self):
        self.api_client = APIClient("http://localhost:8000")
        self.test_count = 0
        self.success_count = 0
        self.error_count = 0
    
    def run_continuous_test(self, duration: int = 60, interval: int = 5):
        """지속적인 API 테스트 실행"""
        print(f"=== 실시간 API 연동 테스트 시작 ===")
        print(f"테스트 시간: {duration}초, 간격: {interval}초")
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.test_count += 1
            current_time = datetime.now().strftime('%H:%M:%S')
            
            print(f"\n[{current_time}] 테스트 #{self.test_count}")
            print("-" * 30)
            
            # 1. 헬스 체크
            self.test_endpoint("헬스 체크", self.api_client.health_check)
            
            # 2. 계약 목록
            self.test_endpoint("계약 목록", self.api_client.get_contracts)
            
            # 3. 재무 정보
            self.test_endpoint("재무 정보", self.api_client.get_financial)
            
            # 4. 노무 정보
            self.test_endpoint("노무 정보", self.api_client.get_labor)
            
            # 통계 출력
            success_rate = (self.success_count / self.test_count) * 100
            print(f"성공률: {success_rate:.1f}% ({self.success_count}/{self.test_count})")
            
            # 대기
            if time.time() - start_time < duration:
                print(f"{interval}초 후 다음 테스트...")
                time.sleep(interval)
        
        # 최종 결과
        self.print_final_results()
    
    def test_endpoint(self, name: str, api_call):
        """개별 엔드포인트 테스트"""
        try:
            start_time = time.time()
            result = api_call()
            response_time = (time.time() - start_time) * 1000
            
            if result.get('status') in ['success', 'healthy']:
                print(f"✅ {name}: 성공 ({response_time:.1f}ms)")
                self.success_count += 1
            else:
                print(f"❌ {name}: 실패 - {result.get('message', '알 수 없는 오류')}")
                self.error_count += 1
                
        except Exception as e:
            print(f"❌ {name}: 오류 - {str(e)}")
            self.error_count += 1
    
    def print_final_results(self):
        """최종 결과 출력"""
        print("\n" + "=" * 50)
        print("=== 실시간 API 연동 테스트 완료 ===")
        print(f"종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"총 테스트 수: {self.test_count}")
        print(f"성공: {self.success_count}")
        print(f"실패: {self.error_count}")
        
        if self.test_count > 0:
            success_rate = (self.success_count / self.test_count) * 100
            print(f"성공률: {success_rate:.1f}%")
            
            if success_rate >= 95:
                print("🎉 우수한 성능! API 연동이 안정적으로 작동합니다.")
            elif success_rate >= 80:
                print("👍 양호한 성능! API 연동이 대체로 안정적입니다.")
            elif success_rate >= 60:
                print("⚠️ 보통 성능! 일부 개선이 필요합니다.")
            else:
                print("❌ 낮은 성능! API 연동에 문제가 있습니다.")
        
        print("=" * 50)
    
    def run_single_test(self):
        """단일 테스트 실행"""
        print("=== 단일 API 연동 테스트 ===")
        
        endpoints = [
            ("헬스 체크", self.api_client.health_check),
            ("계약 목록", self.api_client.get_contracts),
            ("재무 정보", self.api_client.get_financial),
            ("노무 정보", self.api_client.get_labor)
        ]
        
        for name, api_call in endpoints:
            self.test_endpoint(name, api_call)
        
        print(f"\n테스트 완료: {self.success_count}개 성공, {self.error_count}개 실패")

def main():
    """메인 함수"""
    tester = RealtimeAPITester()
    
    print("실시간 API 연동 테스트 모드 선택:")
    print("1. 단일 테스트")
    print("2. 지속적 테스트 (1분)")
    print("3. 지속적 테스트 (5분)")
    
    try:
        choice = input("선택 (1-3): ").strip()
        
        if choice == "1":
            tester.run_single_test()
        elif choice == "2":
            tester.run_continuous_test(duration=60, interval=5)
        elif choice == "3":
            tester.run_continuous_test(duration=300, interval=10)
        else:
            print("잘못된 선택입니다. 단일 테스트를 실행합니다.")
            tester.run_single_test()
            
    except KeyboardInterrupt:
        print("\n\n테스트가 중단되었습니다.")
        tester.print_final_results()

if __name__ == "__main__":
    main() 