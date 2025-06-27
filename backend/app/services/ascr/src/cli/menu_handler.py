#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 메뉴 핸들러

이 모듈은 ASCR의 명령행 인터페이스 메뉴들을 관리합니다.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 로깅 설정
from src.utils.log import get_logger
logger = get_logger(__name__)

def ensure_directories():
    """필요한 디렉토리들을 생성합니다."""
    directories = ["input", "output", "logs", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def check_environment():
    """환경 설정을 확인합니다."""
    checks = {}
    
    # Python 버전 확인
    checks["Python 버전"] = sys.version_info >= (3, 8)
    
    # 필수 디렉토리 확인
    checks["입력 디렉토리"] = Path("input").exists()
    checks["출력 디렉토리"] = Path("output").exists()
    
    # 필수 패키지 확인
    try:
        import pypdf
        checks["pypdf"] = True
    except ImportError:
        checks["pypdf"] = False
    
    try:
        import pandas
        checks["pandas"] = True
    except ImportError:
        checks["pandas"] = False
    
    return checks

def check_required_files(file_paths):
    """필요한 파일들이 존재하는지 확인합니다."""
    for file_path in file_paths:
        if not Path(file_path).exists():
            return False
    return True

def run_script_with_feedback(script_path, description):
    """스크립트를 실행하고 결과를 피드백합니다."""
    try:
        print(f"\n🔄 {description} 실행 중...")
        print("=" * 50)
        
        # 프로젝트 루트 디렉토리로 작업 디렉토리 설정
        project_root = Path(__file__).parent.parent.parent
        
        # 스크립트 실행 (명령행 인수 지원)
        if isinstance(script_path, list):
            # 리스트 형태의 명령어인 경우
            # 항상 Python 인터프리터를 명시적으로 추가
            cmd = [sys.executable] + script_path
            result = subprocess.run(cmd, 
                                  capture_output=True, text=True, encoding='utf-8',
                                  cwd=project_root,
                                  env={**os.environ, "PYTHONPATH": str(project_root)})
        else:
            # 단일 스크립트 경로인 경우
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True, encoding='utf-8',
                                  cwd=project_root,
                                  env={**os.environ, "PYTHONPATH": str(project_root)})
        
        # 출력 표시
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("경고:", result.stderr)
        
        # 결과 확인
        if result.returncode == 0:
            print(f"✅ {description} 완료")
            return True
        else:
            print(f"❌ {description} 실패 (종료 코드: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} 실행 중 오류: {e}")
        return False

def show_project_info():
    """프로젝트 정보를 표시합니다."""
    print("\n=== 📋 ASCR 프로젝트 정보 ===")
    print("프로젝트명: ASCR (Automated Standard Construction Report)")
    print("목적: 건설업계 표준 문서 자동화 처리")
    print("버전: 2.0")
    print("개발 언어: Python 3.8+")
    
    print("\n=== 🔧 주요 기능 ===")
    print("• PDF 텍스트 추출 및 목차 분석")
    print("• 장별/부문별 PDF 분할")
    print("• 목차 구조 JSON 생성")
    print("• 자동화된 워크플로우")
    print("• 품질 검증 및 보고서 생성")
    
    print("\n=== 📁 디렉토리 구조 ===")
    print("input/: 입력 PDF 파일")
    print("input/By_year_Construction_work_standard_price_list/: 연도별 표준품셈 PDF")
    print("output/: 처리 결과 파일")
    print("logs/: 로그 파일")
    print("scripts/: 처리 스크립트")
    print("src/: 소스 코드")
    
    print("\n=== 💡 사용법 ===")
    print("1. input/By_year_Construction_work_standard_price_list 폴더에 PDF 파일 추가")
    print("2. 메인 메뉴에서 원하는 기능 선택")
    print("3. output 폴더에서 결과 확인")
    
    print("\n=== 🔮 향후 개발 예정 ===")
    print("• 표준가격표 자동 다운로드")
    print("• 웹 인터페이스")
    print("• 고급 분석 기능")
    
    input("\nEnter를 누르면 메인 메뉴로 돌아갑니다...")

def show_pdf_processing_menu():
    """PDF 처리 메뉴"""
    while True:
        print("\n=== 📄 PDF 처리 ===")
        print("1. 표준품셈 목차 추출 (index.pdf 파일 만드는 공정)")
        print("2. 텍스트 추출 및 목차 분석 (기존 index.pdf 파일 사용)")
        print("3. 부문별 PDF 분할 (부문별 폴더 아래에, 장별 PDF 파일들이 들어가는 구조)")
        print("4. 목차 텍스트 구조 추출 (index_ex.md 파일 사용)")
        print("5. 계층 구조 검증 및 수정 (기존 JSON 파일 수정)")
        print("6. 검증 규칙 테스트")
        print("0. 메인 메뉴로 돌아가기")
        
        choice = input("\n선택하세요: ").strip()
        
        if choice == "0":
            break
        
        elif choice == "1":
            # 표준품셈 목차 추출 (index.pdf 파일 만드는 공정)
            print("💡 표준가격표 PDF를 input/By_year_Construction_work_standard_price_list 폴더에 추가한 후 실행하세요.")
            print("📋 자동 다운로드 기능은 추후 개발 예정입니다.")
            
            # input/By_year_Construction_work_standard_price_list 폴더에 표준가격표 PDF가 있는지 확인
            pdf_files = list(Path("input/By_year_Construction_work_standard_price_list").glob("*construction_work_standard_price_list*.pdf"))
            if not pdf_files:
                print("❌ input/By_year_Construction_work_standard_price_list 폴더에 표준가격표 PDF를 찾을 수 없습니다.")
                print("💡 {년도}_construction_work_standard_price_list.pdf 파일을 input/By_year_Construction_work_standard_price_list 폴더에 추가한 후 다시 시도해주세요.")
                continue
            
            # 사용 가능한 년도 목록 표시
            available_years = []
            for pdf_file in pdf_files:
                filename = pdf_file.stem
                if "_construction_work_standard_price_list" in filename:
                    year_part = filename.split("_")[0]
                    try:
                        year = int(year_part)
                        available_years.append(year)
                    except ValueError:
                        continue
            
            if available_years:
                available_years.sort()
                print(f"\n📅 사용 가능한 년도: {available_years}")
                
                # 대화형 년도 선택 (기본값) - 메뉴에서 직접 선택
                print(f"\n📅 사용 가능한 년도: {available_years}")
                while True:
                    try:
                        selected_year = input(f"사용할 년도를 선택하세요 (기본값: {max(available_years)}): ").strip()
                        
                        if not selected_year:
                            selected_year = max(available_years)
                        else:
                            selected_year = int(selected_year)
                        
                        if selected_year in available_years:
                            print(f"✅ {selected_year}년을 선택했습니다.")
                            script_args = ["--year", str(selected_year)]
                            break
                        else:
                            print(f"❌ {selected_year}년은 사용할 수 없습니다. 다시 선택해주세요.")
                    except ValueError:
                        print("❌ 올바른 년도를 입력해주세요.")
                    except KeyboardInterrupt:
                        print("\n❌ 사용자가 취소했습니다.")
                        continue
            else:
                script_args = []
            
            # 새로운 목차 추출 스크립트 사용
            script_path = "scripts/main_entry/extract_index_from_standard_price.py"
            if Path(script_path).exists():
                run_script_with_feedback(
                    [script_path] + script_args,
                    "표준품셈 목차 추출 (index.pdf 파일 만드는 공정)"
                )
            else:
                print("❌ 표준품셈 목차 추출 스크립트를 찾을 수 없습니다.")
                print("💡 스크립트 파일이 누락되었습니다.")
        
        elif choice == "2":
            # 텍스트 추출 및 목차 분석 (기존 index.pdf 파일 사용)
            print("💡 input/By_year_Construction_work_standard_price_list/index.pdf 파일을 사용하여 목차를 분석합니다.")
            print("🔧 계층 구조 자동 수정 기능이 포함되어 있습니다.")
            print("📊 정답 데이터 검증 기능이 포함되어 있습니다.")
            
            if check_required_files(["input/By_year_Construction_work_standard_price_list/index.pdf"]):
                print("\n📋 분석 옵션:")
                print("1. 기본 분석 (계층 구조 자동 수정 + 정답 데이터 검증)")
                print("2. 기본 분석 (계층 구조 자동 수정만)")
                print("3. 기본 분석 (수정 없음)")
                print("4. 고급 분석 (상세 설정)")
                
                analysis_choice = input("\n분석 방법을 선택하세요 (1-4, 기본값: 1): ").strip()
                
                if analysis_choice == "" or analysis_choice == "1":
                    # 기본 분석 (자동 수정 + 정답 데이터 검증)
                    print("\n🚀 기본 분석을 시작합니다 (계층 구조 자동 수정 + 정답 데이터 검증)...")
                    success = run_script_with_feedback(
                        ["scripts/main_entry/extract_and_split.py", "input/By_year_Construction_work_standard_price_list/index.pdf", "--extract-only", "--auto-fix", "true", "--validate-ground-truth"],
                        "기본 분석 (계층 구조 자동 수정 + 정답 데이터 검증)"
                    )
                    
                elif analysis_choice == "2":
                    # 기본 분석 (자동 수정만)
                    print("\n🚀 기본 분석을 시작합니다 (계층 구조 자동 수정만)...")
                    success = run_script_with_feedback(
                        ["scripts/main_entry/extract_and_split.py", "input/By_year_Construction_work_standard_price_list/index.pdf", "--extract-only", "--auto-fix", "true"],
                        "기본 분석 (계층 구조 자동 수정만)"
                    )
                    
                elif analysis_choice == "3":
                    # 기본 분석 (수정 없음)
                    print("\n🚀 기본 분석을 시작합니다 (수정 없음)...")
                    success = run_script_with_feedback(
                        ["scripts/main_entry/extract_and_split.py", "input/By_year_Construction_work_standard_price_list/index.pdf", "--extract-only", "--auto-fix", "false"],
                        "기본 분석 (수정 없음)"
                    )
                    
                elif analysis_choice == "4":
                    # 고급 분석 (상세 설정)
                    print("\n🚀 고급 분석을 시작합니다...")
                    print("📋 추가 옵션:")
                    print("1. 정답 데이터 검증 포함")
                    print("2. 정답 데이터 검증 제외")
                    
                    validation_choice = input("\n정답 데이터 검증을 포함하시겠습니까? (1-2, 기본값: 1): ").strip()
                    
                    if validation_choice == "" or validation_choice == "1":
                        success = run_script_with_feedback(
                            ["scripts/main_entry/extract_and_split.py", "input/By_year_Construction_work_standard_price_list/index.pdf", "--extract-only", "--auto-fix", "true", "--validate-ground-truth"],
                            "고급 분석 (정답 데이터 검증 포함)"
                        )
                    else:
                        success = run_script_with_feedback(
                            ["scripts/main_entry/extract_and_split.py", "input/By_year_Construction_work_standard_price_list/index.pdf", "--extract-only", "--auto-fix", "true"],
                            "고급 분석 (정답 데이터 검증 제외)"
                        )
                else:
                    print("❌ 잘못된 선택입니다.")
                    continue
                
                if success:
                    print("\n✅ 목차 분석이 완료되었습니다!")
                    print("📁 결과물은 output 폴더에서 확인할 수 있습니다.")
                    
                    # 정답 데이터 검증 결과가 있는지 확인
                    if analysis_choice in ["1", "4"] and validation_choice in ["", "1"]:
                        print("📊 정답 데이터 검증 결과도 함께 확인하세요.")
                else:
                    print("\n❌ 목차 분석에 실패했습니다.")
            else:
                print("❌ input/By_year_Construction_work_standard_price_list/index.pdf 파일을 추가한 후 다시 시도해주세요.")
                print("💡 먼저 '1. 표준품셈 목차 추출'을 실행하여 index.pdf를 생성하세요.")
        
        elif choice == "3":
            # 부문별 PDF 분할 (부문별 폴더 아래에, 장별 PDF 파일들이 들어가는 구조)
            json_files = list(Path("output").glob("toc_structure_*.json"))
            if json_files:
                latest_json = max(json_files, key=lambda x: x.stat().st_mtime)
                # 전체 표준품셈 PDF 파일 확인
                pdf_files = list(Path("input/By_year_Construction_work_standard_price_list").glob("*construction_work_standard_price_list*.pdf"))
                if pdf_files:
                    standard_pdf = pdf_files[0]
                    if check_required_files([str(latest_json), str(standard_pdf)]):
                        run_script_with_feedback(
                            [sys.executable, "scripts/main_entry/split_pdf.py", "--json", str(latest_json), "--pdf", str(standard_pdf), "--mode", "section", "--output", "output/split_pdfs"],
                            "부문별 PDF 분할 (부문별 폴더 아래에, 장별 PDF 파일들이 들어가는 구조)"
                        )
                    else:
                        print("❌ 필요한 파일이 누락되었습니다.")
                else:
                    print("❌ input/By_year_Construction_work_standard_price_list 폴더에 표준가격표 PDF를 찾을 수 없습니다.")
            else:
                print("💡 먼저 '2. 텍스트 추출 및 목차 분석'을 실행하여 JSON 파일을 생성하세요.")
        
        elif choice == "4":
            # 목차 텍스트 구조 추출 (index_ex.md 파일 사용)
            if check_required_files(["input/index_ex.md"]):
                run_script_with_feedback(
                    [sys.executable, "scripts/main_entry/extract_toc_from_text.py"],
                    "목차 텍스트 구조 추출 (index_ex.md 파일 사용)"
                )
            else:
                print("💡 input/index_ex.md 파일을 추가한 후 다시 시도해주세요.")
                print("💡 목차 텍스트 파일을 input/index_ex.md로 저장해주세요.")
        
        elif choice == "5":
            # 계층 구조 검증 및 수정 (기존 JSON 파일 수정)
            json_files = list(Path("output").glob("toc_structure_*.json"))
            if json_files:
                print("💡 최신 JSON 파일을 찾아서 계층 구조를 검증하고 수정합니다.")
                run_script_with_feedback(
                    [sys.executable, "scripts/main_entry/hierarchy_validator.py"],
                    "계층 구조 검증 및 수정 (기존 JSON 파일 수정)"
                )
            else:
                print("💡 먼저 '2. 텍스트 추출 및 목차 분석'을 실행하여 JSON 파일을 생성하세요.")
        
        elif choice == "6":
            # 검증 규칙 테스트
            script_path = "tests/scripts/test_validation_rules.py"
            if Path(script_path).exists():
                run_script_with_feedback(
                    script_path,
                    "검증 규칙 테스트"
                )
            else:
                print("❌ 검증 규칙 테스트 스크립트를 찾을 수 없습니다.")
        
        else:
            print("❌ 잘못된 선택입니다. 다시 선택해주세요.")

def show_automation_menu():
    """자동화 메뉴"""
    while True:
        print("\n=== 🤖 자동화 ===")
        print("1. 표준가격표 자동 다운로드 (개발 중)")
        print("2. 자동 워크플로우 실행")
        print("3. 배치 처리")
        print("0. 메인 메뉴로 돌아가기")
        
        choice = input("\n선택하세요: ").strip()
        
        if choice == "0":
            break
        
        elif choice == "1":
            print("🚧 이 기능은 현재 개발 중입니다.")
            print("💡 수동으로 표준가격표를 다운로드하여 input 폴더에 추가해주세요.")
        
        elif choice == "2":
            # 자동 워크플로우 실행
            pdf_files = list(Path("input/By_year_Construction_work_standard_price_list").glob("*construction_work_standard_price_list*.pdf"))
            if pdf_files:
                input_pdf = pdf_files[0]
                run_script_with_feedback(
                    [sys.executable, "scripts/main_entry/complete_workflow.py", str(input_pdf)],
                    "자동 워크플로우 실행"
                )
            else:
                print("❌ input/By_year_Construction_work_standard_price_list 폴더에 표준가격표 PDF를 찾을 수 없습니다.")
                print("💡 {년도}_construction_work_standard_price_list.pdf 파일을 input/By_year_Construction_work_standard_price_list 폴더에 추가한 후 다시 시도해주세요.")
        
        elif choice == "3":
            print("🚧 배치 처리 기능은 현재 개발 중입니다.")
            print("💡 개별 파일을 순차적으로 처리해주세요.")
        
        else:
            print("❌ 잘못된 선택입니다. 다시 선택해주세요.")

def show_complete_workflow_menu():
    """완전한 워크플로우 메뉴"""
    while True:
        print("\n=== 🔄 완전한 워크플로우 ===")
        print("1. 전체 워크플로우 실행 (목차 추출 → 분석 → 분할)")
        print("2. 워크플로우 단계별 실행")
        print("3. 워크플로우 검증")
        print("0. 메인 메뉴로 돌아가기")
        
        choice = input("\n선택하세요: ").strip()
        
        if choice == "0":
            break
        
        elif choice == "1":
            # 전체 워크플로우 실행
            pdf_files = list(Path("input/By_year_Construction_work_standard_price_list").glob("*construction_work_standard_price_list*.pdf"))
            if pdf_files:
                input_pdf = pdf_files[0]
                run_script_with_feedback(
                    [sys.executable, "scripts/main_entry/complete_workflow.py", str(input_pdf)],
                    "전체 워크플로우 실행"
                )
            else:
                print("❌ input/By_year_Construction_work_standard_price_list 폴더에 표준가격표 PDF를 찾을 수 없습니다.")
                print("💡 {년도}_construction_work_standard_price_list.pdf 파일을 input/By_year_Construction_work_standard_price_list 폴더에 추가한 후 다시 시도해주세요.")
        
        elif choice == "2":
            print("🚧 단계별 실행 기능은 현재 개발 중입니다.")
            print("💡 'PDF 처리' 메뉴에서 개별 단계를 실행해주세요.")
        
        elif choice == "3":
            print("🚧 워크플로우 검증 기능은 현재 개발 중입니다.")
            print("💡 '검증 규칙 테스트'를 사용해주세요.")
        
        else:
            print("❌ 잘못된 선택입니다. 다시 선택해주세요.")

def show_main_menu():
    """메인 메뉴"""
    while True:
        print("\n" + "=" * 50)
        print("🏗️  ASCR - 건설업계 표준 문서 자동화 처리 시스템")
        print("=" * 50)
        print("1. 📄 PDF 처리")
        print("2. 🤖 자동화")
        print("3. 🔄 완전한 워크플로우")
        print("4. 📋 프로젝트 정보")
        print("5. 🔧 환경 확인")
        print("0. 종료")
        
        choice = input("\n선택하세요: ").strip()
        
        if choice == "0":
            print("\n👋 ASCR를 사용해주셔서 감사합니다!")
            break
        
        elif choice == "1":
            show_pdf_processing_menu()
        
        elif choice == "2":
            show_automation_menu()
        
        elif choice == "3":
            show_complete_workflow_menu()
        
        elif choice == "4":
            show_project_info()
        
        elif choice == "5":
            # 환경 확인
            print("\n=== 🔧 환경 확인 ===")
            checks = check_environment()
            for check_name, status in checks.items():
                status_icon = "✅" if status else "❌"
                print(f"{status_icon} {check_name}: {'정상' if status else '문제'}")
            
            if all(checks.values()):
                print("\n✅ 모든 환경이 정상입니다!")
            else:
                print("\n⚠️ 일부 환경에 문제가 있습니다. 확인해주세요.")
            
            input("\nEnter를 누르면 메인 메뉴로 돌아갑니다...")
        
        else:
            print("❌ 잘못된 선택입니다. 다시 선택해주세요.") 