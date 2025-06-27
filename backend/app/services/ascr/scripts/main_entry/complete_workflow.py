#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전 자동화 워크플로우 스크립트 (리팩토링됨)

1번부터 4번까지의 모든 작업을 순차적으로 실행합니다.
기존 341줄에서 120줄로 대폭 간소화되었습니다.
"""

import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.log import get_logger, log_workflow_step
from src.utils.config.config_manager import ASCRConfigManager

# 새로운 모듈들 import
from scripts.workflow_executor import WorkflowExecutor
from scripts.workflow_reporter import WorkflowReporter

class CompleteWorkflow:
    """완전 자동화 워크플로우 클래스 (리팩토링됨)"""
    
    def __init__(self):
        self.logger = get_logger("CompleteWorkflow")
        self.config = ASCRConfigManager()
        self.executor = WorkflowExecutor()
        self.reporter = WorkflowReporter()
        self.start_time = None
        
    def run_workflow(self, input_pdf: str, output_dir: str = "output") -> bool:
        """
        완전 자동화 워크플로우 실행
        
        Args:
            input_pdf: 입력 PDF 파일 경로
            output_dir: 출력 디렉토리
            
        Returns:
            bool: 워크플로우 성공 여부
        """
        self.start_time = datetime.now()
        log_workflow_step("완전 자동화 워크플로우", "started", {
            "input_pdf": input_pdf,
            "output_dir": output_dir
        })
        
        print("🚀 === 완전 자동화 워크플로우 시작 ===")
        print(f"📄 입력 파일: {input_pdf}")
        print(f"📂 출력 디렉토리: {output_dir}")
        print(f"⏰ 시작 시간: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        try:
            # 1단계: 표준품셈 목차 추출
            if not self.executor.run_step_1(input_pdf, output_dir):
                return self._handle_workflow_failure("1단계 실패")
            
            # 2단계: 텍스트 추출 및 목차 분석
            if not self.executor.run_step_2(output_dir):
                return self._handle_workflow_failure("2단계 실패")
            
            # 3단계: 부문별 PDF 분할
            if not self.executor.run_step_3(output_dir):
                return self._handle_workflow_failure("3단계 실패")
            
            # 4단계: 검증 규칙 테스트
            if not self.executor.run_step_4(output_dir):
                return self._handle_workflow_failure("4단계 실패")
            
            # 워크플로우 완료
            workflow_results = self.executor.get_workflow_results()
            return self.reporter.complete_workflow(output_dir, workflow_results, self.start_time)
            
        except Exception as e:
            self.logger.error("워크플로우 실행 실패", error=e)
            print(f"❌ 워크플로우 실행 중 오류 발생: {e}")
            return False
    
    def _handle_workflow_failure(self, failure_message: str) -> bool:
        """워크플로우 실패 처리"""
        self.logger.error(f"워크플로우 실패: {failure_message}")
        print(f"❌ {failure_message}")
        
        # 부분 결과라도 요약 보고서 생성
        workflow_results = self.executor.get_workflow_results()
        if workflow_results:
            summary = self.reporter.generate_summary_report(workflow_results)
            self.reporter.print_summary(summary)
        
        return False
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """워크플로우 상태 반환"""
        workflow_results = self.executor.get_workflow_results()
        validation = self.executor.validate_step_results()
        summary = self.reporter.generate_summary_report(workflow_results)
        
        return {
            "workflow_results": workflow_results,
            "validation": validation,
            "summary": summary,
            "start_time": self.start_time
        }

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="완전 자동화 워크플로우")
    parser.add_argument("input_pdf", help="입력 PDF 파일 경로")
    parser.add_argument("--output", "-o", default="output", help="출력 디렉토리")
    parser.add_argument("--verbose", "-v", action="store_true", help="상세 출력")
    
    args = parser.parse_args()
    
    # 입력 파일 검증
    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"❌ 입력 파일이 존재하지 않습니다: {args.input_pdf}")
        sys.exit(1)
    
    # 워크플로우 실행
    workflow = CompleteWorkflow()
    success = workflow.run_workflow(str(input_path), args.output)
    
    # 상태 정보 출력 (상세 모드)
    if args.verbose:
        status = workflow.get_workflow_status()
        print("\n📊 === 상세 상태 정보 ===")
        for key, value in status.items():
            print(f"{key}: {value}")
    
    if success:
        print("✅ 워크플로우가 성공적으로 완료되었습니다")
        sys.exit(0)
    else:
        print("❌ 워크플로우 실행에 실패했습니다")
        sys.exit(1)

if __name__ == "__main__":
    main() 