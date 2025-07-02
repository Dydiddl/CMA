#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 실행기

모든 테스트를 체계적으로 실행하고 결과를 보고합니다.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import argparse

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_pytest_tests(test_path: str = ".", verbose: bool = True) -> dict:
    """pytest를 사용하여 테스트 실행"""
    print(f"🧪 pytest 테스트 실행: {test_path}")
    
    try:
        # 현재 실행 중인 Python 인터프리터 사용
        python_executable = sys.executable
        print(f"🐍 사용 중인 Python: {python_executable}")
        
        # pytest 명령어 구성
        cmd = [python_executable, "-m", "pytest", test_path]
        if verbose:
            cmd.append("-v")
        
        # 테스트 실행
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # 결과 분석
        test_result = {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
        
        if test_result["success"]:
            print("✅ 테스트 성공")
        else:
            print("❌ 테스트 실패")
            if result.stderr:
                print(f"오류: {result.stderr}")
        
        return test_result
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(cmd) if 'cmd' in locals() else "unknown"
        }

def run_specific_test_category(category: str):
    """특정 카테고리의 테스트 실행"""
    test_paths = {
        "unit": "tests/unit",
        "integration": "tests/integration", 
        "scripts": "tests/scripts",
        "classification": "tests/unit/test_classification.py"
    }
    
    if category not in test_paths:
        print(f"❌ 알 수 없는 테스트 카테고리: {category}")
        return None
    
    return run_pytest_tests(test_paths[category])

def generate_test_report(test_results: dict, validation_results: dict = None):
    """테스트 결과 보고서 생성"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = project_root / "output" / f"test_report_{timestamp}.json"
    
    # 출력 디렉토리 생성
    report_file.parent.mkdir(exist_ok=True)
    
    # 보고서 데이터 구성
    report_data = {
        "timestamp": timestamp,
        "test_results": test_results,
        "validation_results": validation_results,
        "summary": {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "success_rate": 0.0
        }
    }
    
    # 테스트 결과 분석
    if test_results.get("success") and test_results.get("stdout"):
        stdout = test_results["stdout"]
        
        # pytest 출력에서 테스트 통계 추출
        lines = stdout.split('\n')
        for line in lines:
            if "passed" in line and "failed" in line:
                # 예: "5 passed, 1 failed in 2.34s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed":
                        report_data["summary"]["passed_tests"] = int(parts[i-1])
                    elif part == "failed":
                        report_data["summary"]["failed_tests"] = int(parts[i-1])
                
                report_data["summary"]["total_tests"] = (
                    report_data["summary"]["passed_tests"] + 
                    report_data["summary"]["failed_tests"]
                )
                
                if report_data["summary"]["total_tests"] > 0:
                    report_data["summary"]["success_rate"] = (
                        report_data["summary"]["passed_tests"] / 
                        report_data["summary"]["total_tests"]
                    ) * 100
                break
    
    # 보고서 저장
    with open(report_file, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"📊 테스트 보고서 생성: {report_file}")
    return report_file

def print_test_summary(test_results: dict):
    """테스트 결과 요약 출력"""
    if not test_results:
        print("❌ 테스트 결과가 없습니다.")
        return
    
    print("\n" + "="*50)
    print("📋 테스트 결과 요약")
    print("="*50)
    
    if test_results.get("success"):
        print("✅ 전체 테스트: 성공")
    else:
        print("❌ 전체 테스트: 실패")
    
    if test_results.get("stdout"):
        # pytest 출력에서 주요 정보 추출
        stdout = test_results["stdout"]
        lines = stdout.split('\n')
        
        for line in lines:
            if "passed" in line and "failed" in line:
                print(f"📊 {line.strip()}")
                break
            elif "ERROR" in line:
                print(f"❌ {line.strip()}")
    
    if test_results.get("stderr"):
        print(f"⚠️  오류: {test_results['stderr'][:200]}...")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="테스트 실행기")
    parser.add_argument("--category", choices=["unit", "integration", "scripts", "all"], 
                       default="all", help="실행할 테스트 카테고리")
    parser.add_argument("--verbose", "-v", action="store_true", help="상세 출력")
    parser.add_argument("--report", action="store_true", help="보고서 생성")
    
    args = parser.parse_args()
    
    print("🚀 ASCR 테스트 실행기 시작")
    print(f"📁 프로젝트 루트: {project_root}")
    
    test_results = None
    validation_results = None
    
    if args.category == "all":
        # 모든 테스트 실행
        print("\n1️⃣ 단위 테스트 실행")
        test_results = run_specific_test_category("unit")
        
        print("\n2️⃣ 통합 테스트 실행")
        integration_results = run_specific_test_category("integration")
        
        print("\n3️⃣ 스크립트 테스트 실행")
        script_results = run_specific_test_category("scripts")
        
        # 마지막 결과를 메인 결과로 사용
        test_results = script_results or integration_results or test_results
        
    else:
        # 특정 카테고리만 실행
        test_results = run_specific_test_category(args.category)
    
    # 결과 출력
    print_test_summary(test_results)
    
    # 보고서 생성
    if args.report or args.category == "all":
        report_file = generate_test_report(test_results, validation_results)
        print(f"\n📄 상세 보고서: {report_file}")
    
    # 종료 코드 설정
    if test_results and test_results.get("success"):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 