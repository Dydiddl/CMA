#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 실행 스크립트
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """명령어 실행"""
    print(f"\n{'='*50}")
    print(f"[INFO] {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 명령어 실행 실패: {e}")
        print(f"stderr: {e.stderr}")
        return False


def main():
    """메인 함수"""
    print("🧪 CMA 테스트 실행기")
    print("="*50)
    
    # 현재 디렉토리 확인
    if not Path("pytest.ini").exists():
        print("[ERROR] pytest.ini 파일을 찾을 수 없습니다. backend 디렉토리에서 실행하세요.")
        sys.exit(1)
    
    # 테스트 타입 선택
    print("\n테스트 타입을 선택하세요:")
    print("1. 전체 테스트")
    print("2. 단위 테스트만")
    print("3. 통합 테스트만")
    print("4. API 테스트만")
    print("5. 성능 테스트만")
    print("6. ASCR 모듈 테스트만")
    print("7. 커버리지 리포트 생성")
    
    choice = input("\n선택 (1-7): ").strip()
    
    commands = {
        "1": "pytest",
        "2": "pytest tests/unit/ -m unit",
        "3": "pytest tests/integration/ -m integration",
        "4": "pytest tests/api/ -m api",
        "5": "pytest tests/performance/ -m performance",
        "6": "pytest -m ascr",
        "7": "pytest --cov=app --cov-report=html --cov-report=term-missing"
    }
    
    descriptions = {
        "1": "전체 테스트 실행",
        "2": "단위 테스트 실행",
        "3": "통합 테스트 실행",
        "4": "API 테스트 실행",
        "5": "성능 테스트 실행",
        "6": "ASCR 모듈 테스트 실행",
        "7": "커버리지 리포트 생성"
    }
    
    if choice not in commands:
        print("[ERROR] 잘못된 선택입니다.")
        sys.exit(1)
    
    command = commands[choice]
    description = descriptions[choice]
    
    # 테스트 실행
    success = run_command(command, description)
    
    if success:
        print(f"\n[SUCCESS] {description} 완료")
    else:
        print(f"\n[ERROR] {description} 실패")
        sys.exit(1)


if __name__ == "__main__":
    main() 