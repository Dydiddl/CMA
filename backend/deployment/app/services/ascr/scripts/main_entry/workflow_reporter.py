#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
워크플로우 리포터 모듈

이 모듈은 워크플로우 결과 보고와 완료 처리를 담당합니다.
"""

import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from datetime import datetime
from typing import Dict, List, Any, Optional

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.log import get_logger, log_workflow_step

class WorkflowReporter:
    """워크플로우 리포터 클래스"""
    
    def __init__(self):
        self.logger = get_logger("WorkflowReporter")
    
    def complete_workflow(self, output_dir: str, workflow_results: Dict[str, Any], 
                         start_time: datetime) -> bool:
        """워크플로우 완료 처리"""
        try:
            end_time = datetime.now()
            duration = end_time - start_time
            
            print("\n🎉 === 워크플로우 완료 ===")
            print(f"⏰ 시작 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏰ 종료 시간: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏱️ 소요 시간: {duration}")
            print(f"📂 출력 디렉토리: {output_dir}")
            
            # 최종 보고서 생성
            self._generate_final_report(output_dir, duration, workflow_results)
            
            # 로그 기록
            log_workflow_step("완전 자동화 워크플로우", "completed", {
                "duration": str(duration),
                "output_dir": output_dir,
                "results": workflow_results
            })
            
            print("✅ 워크플로우가 성공적으로 완료되었습니다!")
            return True
            
        except Exception as e:
            self.logger.error("워크플로우 완료 처리 실패", error=e)
            print(f"❌ 워크플로우 완료 처리 중 오류: {e}")
            return False
    
    def _generate_final_report(self, output_dir: str, duration, workflow_results: Dict[str, Any]):
        """최종 보고서 생성"""
        try:
            report_path = Path(output_dir) / "workflow_final_report.txt"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=== 완전 자동화 워크플로우 최종 보고서 ===\n")
                f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"소요 시간: {duration}\n")
                f.write(f"출력 디렉토리: {output_dir}\n\n")
                
                f.write("=== 단계별 실행 결과 ===\n")
                
                # 1단계 결과
                step1_file = workflow_results.get('step1_toc_file')
                if step1_file:
                    f.write(f"✅ 1단계: 목차 추출 성공\n")
                    f.write(f"   - 생성 파일: {Path(step1_file).name}\n")
                else:
                    f.write(f"❌ 1단계: 목차 추출 실패\n")
                
                # 2단계 결과
                step2_file = workflow_results.get('step2_text_file')
                if step2_file:
                    f.write(f"✅ 2단계: 텍스트 추출 성공\n")
                    f.write(f"   - 생성 파일: {Path(step2_file).name}\n")
                else:
                    f.write(f"❌ 2단계: 텍스트 추출 실패\n")
                
                # 3단계 결과
                step3_dir = workflow_results.get('step3_split_dir')
                if step3_dir:
                    f.write(f"✅ 3단계: PDF 분할 성공\n")
                    f.write(f"   - 생성 디렉토리: {Path(step3_dir).name}\n")
                else:
                    f.write(f"❌ 3단계: PDF 분할 실패\n")
                
                # 4단계 결과
                step4_file = workflow_results.get('step4_validation_file')
                if step4_file:
                    f.write(f"✅ 4단계: 검증 테스트 성공\n")
                    f.write(f"   - 생성 파일: {Path(step4_file).name}\n")
                else:
                    f.write(f"❌ 4단계: 검증 테스트 실패\n")
                
                f.write("\n=== 생성된 파일 목록 ===\n")
                
                # 출력 디렉토리의 모든 파일 목록
                output_path = Path(output_dir)
                if output_path.exists():
                    for file_path in output_path.rglob("*"):
                        if file_path.is_file():
                            relative_path = file_path.relative_to(output_path)
                            f.write(f"   - {relative_path}\n")
                
                f.write("\n=== 워크플로우 요약 ===\n")
                success_count = sum(1 for value in workflow_results.values() if value)
                total_steps = len(workflow_results)
                f.write(f"성공한 단계: {success_count}/{total_steps}\n")
                f.write(f"성공률: {(success_count/total_steps)*100:.1f}%\n")
                
                if success_count == total_steps:
                    f.write("🎉 모든 단계가 성공적으로 완료되었습니다!\n")
                else:
                    f.write("⚠️ 일부 단계에서 실패가 발생했습니다.\n")
            
            print(f"📄 최종 보고서 생성: {report_path}")
            
        except Exception as e:
            self.logger.error("최종 보고서 생성 실패", error=e)
            print(f"❌ 최종 보고서 생성 중 오류: {e}")
    
    def generate_summary_report(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """요약 보고서 생성"""
        try:
            summary = {
                "total_steps": 4,
                "successful_steps": 0,
                "failed_steps": 0,
                "success_rate": 0.0,
                "step_details": {},
                "overall_status": "unknown"
            }
            
            # 단계별 결과 분석
            step_mapping = {
                'step1_toc_file': '목차 추출',
                'step2_text_file': '텍스트 추출',
                'step3_split_dir': 'PDF 분할',
                'step4_validation_file': '검증 테스트'
            }
            
            for step_key, step_name in step_mapping.items():
                result = workflow_results.get(step_key)
                if result:
                    summary["successful_steps"] += 1
                    summary["step_details"][step_name] = "성공"
                else:
                    summary["failed_steps"] += 1
                    summary["step_details"][step_name] = "실패"
            
            # 성공률 계산
            summary["success_rate"] = (summary["successful_steps"] / summary["total_steps"]) * 100
            
            # 전체 상태 결정
            if summary["successful_steps"] == summary["total_steps"]:
                summary["overall_status"] = "완전 성공"
            elif summary["successful_steps"] > 0:
                summary["overall_status"] = "부분 성공"
            else:
                summary["overall_status"] = "완전 실패"
            
            return summary
            
        except Exception as e:
            self.logger.error("요약 보고서 생성 실패", error=e)
            return {
                "total_steps": 4,
                "successful_steps": 0,
                "failed_steps": 4,
                "success_rate": 0.0,
                "step_details": {},
                "overall_status": "오류 발생"
            }
    
    def print_summary(self, summary: Dict[str, Any]):
        """요약 정보 출력"""
        print("\n📊 === 워크플로우 요약 ===")
        print(f"전체 상태: {summary['overall_status']}")
        print(f"성공률: {summary['success_rate']:.1f}%")
        print(f"성공한 단계: {summary['successful_steps']}/{summary['total_steps']}")
        
        print("\n단계별 결과:")
        for step_name, status in summary["step_details"].items():
            status_icon = "✅" if status == "성공" else "❌"
            print(f"  {status_icon} {step_name}: {status}")
        
        if summary["overall_status"] == "완전 성공":
            print("\n🎉 모든 단계가 성공적으로 완료되었습니다!")
        elif summary["overall_status"] == "부분 성공":
            print("\n⚠️ 일부 단계에서 실패가 발생했습니다.")
        else:
            print("\n❌ 모든 단계에서 실패가 발생했습니다.") 