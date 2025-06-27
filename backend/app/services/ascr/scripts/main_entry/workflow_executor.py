#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
워크플로우 실행기 모듈

이 모듈은 각 단계별 워크플로우 실행을 담당합니다.
"""

import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import subprocess
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.log import get_logger, log_workflow_step
from config.file_paths import FilePathManager, get_standard_price_pdf_path, validate_year


class WorkflowExecutor:
    """워크플로우 실행기 클래스"""
    
    def __init__(self, year: int = None):
        self.logger = get_logger("WorkflowExecutor")
        self.workflow_results = {}
        self.file_manager = FilePathManager()
        
        # 년도 설정
        if year is None:
            self.year = self.file_manager.get_latest_year()
        else:
            if not validate_year(year):
                raise ValueError(f"유효하지 않은 년도입니다: {year}")
            self.year = year
        
        # 파일 경로 설정
        self.pdf_path = get_standard_price_pdf_path(self.year)
        if not self.pdf_path or not self.pdf_path.exists():
            raise FileNotFoundError(f"{self.year}년 표준품셈 PDF 파일을 찾을 수 없습니다")
        
        print(f"🎯 {self.year}년 표준품셈 PDF 사용: {self.pdf_path.name}")
    
    def run_step_1(self, output_dir: str) -> bool:
        """1단계: 표준품셈 목차 추출"""
        print("📋 === 1단계: 표준품셈 목차 추출 ===")
        
        try:
            # 1-1. 목차 추출 (extract_and_split.py 사용)
            cmd = [
                sys.executable, "scripts/main_entry/extract_and_split.py",
                str(self.pdf_path),
                "--extract-only",
                "--output", output_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                print(f"❌ 1단계 실패: {result.stderr}")
                return False
            
            print("✅ 1단계 완료: 목차 추출 성공")
            
            # 결과 파일 확인
            toc_files = list(Path(output_dir).glob("toc_structure_*.json"))
            if toc_files:
                latest_toc = max(toc_files, key=lambda x: x.stat().st_mtime)
                self.workflow_results['step1_toc_file'] = str(latest_toc)
                print(f"📄 생성된 목차 파일: {latest_toc.name}")
            
            return True
            
        except Exception as e:
            self.logger.error("1단계 실행 실패", error=e)
            print(f"❌ 1단계 실행 중 오류: {e}")
            return False
    
    def run_step_2(self, output_dir: str) -> bool:
        """2단계: 텍스트 추출 및 목차 분석"""
        print("\n�� === 2단계: 텍스트 추출 및 목차 분석 ===")
        
        try:
            # 2-1. 텍스트 추출 및 분할
            cmd = [
                sys.executable, "scripts/main_entry/extract_and_split.py",
                str(self.pdf_path),
                "--extract-only",
                "--output-dir", output_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                print(f"❌ 2단계 실패: {result.stderr}")
                return False
            
            print("✅ 2단계 완료: 텍스트 추출 및 분석 성공")
            
            # 결과 파일 확인
            toc_files = list(Path(output_dir).glob("toc_structure_*.json"))
            if toc_files:
                latest_toc = max(toc_files, key=lambda x: x.stat().st_mtime)
                self.workflow_results['step2_toc_file'] = str(latest_toc)
                print(f"📄 생성된 목차 파일: {latest_toc.name}")
            
            return True
            
        except Exception as e:
            self.logger.error("2단계 실행 실패", error=e)
            print(f"❌ 2단계 실행 중 오류: {e}")
            return False
    
    def run_step_3(self, output_dir: str) -> bool:
        """3단계: 부문별 PDF 분할"""
        print("\n📋 === 3단계: 부문별 PDF 분할 ===")
        
        try:
            # 3-1. PDF 분할
            toc_file = self.workflow_results.get('step1_toc_file', '')
            if not toc_file:
                print("⚠️ 목차 파일을 찾을 수 없어 분할을 건너뜁니다.")
                return True
            
            cmd = [
                sys.executable, "scripts/main_entry/split_pdf.py",
                "--json", toc_file,
                "--pdf", str(self.pdf_path),
                "--mode", "section",
                "--output", f"{output_dir}/split_pdfs"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                print(f"❌ 3단계 실패: {result.stderr}")
                return False
            
            print("✅ 3단계 완료: PDF 분할 성공")
            
            # 결과 파일 확인
            split_dirs = list(Path(output_dir).glob("split_pdfs"))
            if split_dirs:
                self.workflow_results['step3_split_dir'] = str(split_dirs[0])
                print(f"📂 생성된 분할 디렉토리: {split_dirs[0].name}")
            
            return True
            
        except Exception as e:
            self.logger.error("3단계 실행 실패", error=e)
            print(f"❌ 3단계 실행 중 오류: {e}")
            return False
    
    def run_step_4(self, output_dir: str) -> bool:
        """4단계: 검증 규칙 테스트"""
        print("\n📋 === 4단계: 검증 규칙 테스트 ===")
        
        try:
            # 4-1. 검증 규칙 테스트
            text_file = self.workflow_results.get('step2_text_file')
            if not text_file:
                print("⚠️ 텍스트 파일을 찾을 수 없어 검증을 건너뜁니다.")
                return True
            
            cmd = [
                sys.executable, "scripts/dev/test_validation_rules.py",
                text_file,
                "--output", output_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                print(f"❌ 4단계 실패: {result.stderr}")
                return False
            
            print("✅ 4단계 완료: 검증 규칙 테스트 성공")
            
            # 결과 파일 확인
            validation_files = list(Path(output_dir).glob("validation_*.txt"))
            if validation_files:
                latest_validation = max(validation_files, key=lambda x: x.stat().st_mtime)
                self.workflow_results['step4_validation_file'] = str(latest_validation)
                print(f"📄 생성된 검증 파일: {latest_validation.name}")
            
            return True
            
        except Exception as e:
            self.logger.error("4단계 실행 실패", error=e)
            print(f"❌ 4단계 실행 중 오류: {e}")
            return False
    
    def get_workflow_results(self) -> Dict[str, Any]:
        """워크플로우 결과 반환"""
        return self.workflow_results.copy()
    
    def validate_step_results(self) -> Dict[str, bool]:
        """단계별 결과 검증"""
        validation = {
            "step1": bool(self.workflow_results.get('step1_toc_file')),
            "step2": bool(self.workflow_results.get('step2_text_file')),
            "step3": bool(self.workflow_results.get('step3_split_dir')),
            "step4": bool(self.workflow_results.get('step4_validation_file'))
        }
        
        return validation


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="워크플로우 실행기")
    parser.add_argument("--year", type=int, help="사용할 년도 (기본값: 최신 년도)")
    parser.add_argument("--output", default="output", help="출력 디렉토리")
    
    args = parser.parse_args()
    
    try:
        # 워크플로우 실행기 초기화
        executor = WorkflowExecutor(year=args.year)
        
        # 출력 디렉토리 생성
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 워크플로우 실행
        success = True
        success &= executor.run_step_1(str(output_dir))
        success &= executor.run_step_2(str(output_dir))
        success &= executor.run_step_3(str(output_dir))
        success &= executor.run_step_4(str(output_dir))
        
        if success:
            print("\n✅ 모든 워크플로우가 성공적으로 완료되었습니다!")
        else:
            print("\n❌ 일부 워크플로우에서 오류가 발생했습니다.")
        
    except Exception as e:
        print(f"❌ 워크플로우 실행 중 오류: {e}")


if __name__ == "__main__":
    main() 