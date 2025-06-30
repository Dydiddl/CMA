#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
검증 규칙 테스트 스크립트
추출된 텍스트 파일을 분석하여 목차 구조의 유효성을 검증합니다.
"""

import sys
import argparse
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.extract.toc_extractor import TOCExtractor
from src.common.constants import SECTION_MAPPING
from src.utils.log import get_logger, log_workflow_step

class ValidationRuleTester:
    """검증 규칙 테스트 클래스"""
    
    def __init__(self):
        self.logger = get_logger("ValidationTester")
        self.required_sections = list(SECTION_MAPPING.values())
        
    def test_toc_structure(self, text_file_path: Path) -> Dict[str, Any]:
        """
        목차 구조 검증 테스트
        
        Args:
            text_file_path: 검증할 텍스트 파일 경로
            
        Returns:
            Dict[str, Any]: 검증 결과
        """
        log_workflow_step("목차 구조 검증", "started", {"file": str(text_file_path)})
        
        try:
            # 1. 텍스트 파일 읽기
            with open(text_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📄 텍스트 파일 읽기 완료: {len(content)} 문자")
            
            # 2. 목차 구조 추출
            extractor = TOCExtractor()
            toc_structure = extractor.extract_toc_structure(content, method='auto')
            
            if not toc_structure or not toc_structure.entries:
                return {
                    'valid': False,
                    'error': '목차 구조를 추출할 수 없습니다.',
                    'details': {}
                }
            
            print(f"📊 추출된 목차 항목: {len(toc_structure.entries)}개")
            
            # 3. 검증 실행
            validation_results = self._validate_toc_structure(toc_structure)
            
            log_workflow_step("목차 구조 검증", "completed", validation_results)
            return validation_results
            
        except Exception as e:
            self.logger.error("목차 구조 검증 실패", error=e)
            return {
                'valid': False,
                'error': str(e),
                'details': {}
            }
    
    def _validate_toc_structure(self, toc_structure) -> Dict[str, Any]:
        """목차 구조 상세 검증"""
        results = {
            'valid': True,
            'total_entries': len(toc_structure.entries),
            'chapter_count': 0,
            'section_count': 0,
            'missing_sections': [],
            'section_order': [],
            'warnings': [],
            'errors': []
        }
        
        # 1. 장/절 개수 확인
        for entry in toc_structure.entries:
            if entry.level == 1:
                results['chapter_count'] += 1
            elif entry.level == 2:
                results['section_count'] += 1
        
        print(f"📋 장 개수: {results['chapter_count']}개")
        print(f"📋 절 개수: {results['section_count']}개")
        
        # 2. 부문별 검증
        found_sections = set()
        for section_name, section_data in toc_structure.sections.items():
            if section_data.get("chapters"):
                found_sections.add(section_name)
                results['section_order'].append(section_name)
                print(f"✅ {section_name}: {len(section_data['chapters'])}개 장")
        
        # 3. 누락된 부문 확인
        for required_section in self.required_sections:
            if required_section not in found_sections:
                results['missing_sections'].append(required_section)
                results['warnings'].append(f"누락된 부문: {required_section}")
        
        # 4. 검증 규칙 적용
        if results['chapter_count'] == 0:
            results['errors'].append("장 단위 항목이 없습니다.")
            results['valid'] = False
        
        if len(results['missing_sections']) > 2:  # 2개 이상 부문 누락 시 오류
            results['errors'].append(f"너무 많은 부문이 누락되었습니다: {len(results['missing_sections'])}개")
            results['valid'] = False
        
        if not results['section_order']:
            results['warnings'].append("부문 순서를 확인할 수 없습니다.")
        
        return results
    
    def generate_validation_report(self, validation_results: Dict[str, Any], 
                                 output_dir: Path) -> Path:
        """검증 결과 보고서 생성"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = output_dir / f"validation_report_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 목차 구조 검증 보고서\n\n")
            f.write(f"**생성일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 검증 결과 요약
            f.write("## 📊 검증 결과 요약\n\n")
            status = "✅ 통과" if validation_results['valid'] else "❌ 실패"
            f.write(f"**상태**: {status}\n\n")
            
            # 통계 정보
            f.write("## 📈 통계 정보\n\n")
            f.write(f"- **총 항목 수**: {validation_results['total_entries']}개\n")
            f.write(f"- **장 개수**: {validation_results['chapter_count']}개\n")
            f.write(f"- **절 개수**: {validation_results['section_count']}개\n")
            f.write(f"- **발견된 부문**: {len(validation_results['section_order'])}개\n\n")
            
            # 부문별 정보
            if validation_results['section_order']:
                f.write("## 📂 부문별 정보\n\n")
                for section in validation_results['section_order']:
                    f.write(f"- **{section}**: 발견됨\n")
                f.write("\n")
            
            # 오류 및 경고
            if validation_results['errors']:
                f.write("## ❌ 오류\n\n")
                for error in validation_results['errors']:
                    f.write(f"- {error}\n")
                f.write("\n")
            
            if validation_results['warnings']:
                f.write("## ⚠️ 경고\n\n")
                for warning in validation_results['warnings']:
                    f.write(f"- {warning}\n")
                f.write("\n")
            
            # 권장사항
            f.write("## 💡 권장사항\n\n")
            if validation_results['valid']:
                f.write("- 목차 구조가 정상적으로 검증되었습니다.\n")
                f.write("- PDF 분할 작업을 진행할 수 있습니다.\n")
            else:
                f.write("- 목차 구조에 문제가 있습니다.\n")
                f.write("- 다른 추출 방법을 시도해보세요.\n")
                f.write("- 원본 PDF의 목차 부분을 확인해보세요.\n")
        
        print(f"📄 검증 보고서 생성 완료: {report_path}")
        return report_path

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="목차 구조 검증 규칙 테스트",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python test_validation_rules.py output/index_extracted_20250623_113523.txt
  python test_validation_rules.py output/index_extracted_20250623_113523.txt --output output
        """
    )
    
    parser.add_argument("text_file", type=str, help="검증할 텍스트 파일 경로")
    parser.add_argument("--output", "-o", type=str, default="output", help="출력 디렉토리")
    
    args = parser.parse_args()
    
    # 파일 경로 검증
    text_file_path = Path(args.text_file)
    if not text_file_path.exists():
        print(f"❌ 텍스트 파일이 존재하지 않습니다: {text_file_path}")
        sys.exit(1)
    
    # 출력 디렉토리 설정
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== 목차 구조 검증 규칙 테스트 시작 ===")
    print(f"📄 검증 파일: {text_file_path}")
    print(f"📂 출력 디렉토리: {output_dir}")
    print()
    
    # 검증 실행
    tester = ValidationRuleTester()
    validation_results = tester.test_toc_structure(text_file_path)
    
    # 결과 출력
    print("\n" + "="*50)
    print("📊 검증 결과")
    print("="*50)
    
    if validation_results['valid']:
        print("✅ 검증 통과: 목차 구조가 정상적으로 검증되었습니다.")
    else:
        print("❌ 검증 실패: 목차 구조에 문제가 있습니다.")
        if 'error' in validation_results:
            print(f"   오류: {validation_results['error']}")
    
    # 상세 결과 출력
    if validation_results.get('errors'):
        print(f"\n❌ 오류:")
        for error in validation_results['errors']:
            print(f"   - {error}")
    
    if validation_results.get('warnings'):
        print(f"\n⚠️ 경고:")
        for warning in validation_results['warnings']:
            print(f"   - {warning}")
    
    if validation_results.get('section_order'):
        print(f"\n📂 발견된 부문 순서:")
        print(f"   {' → '.join(validation_results['section_order'])}")
    
    # 보고서 생성
    report_path = tester.generate_validation_report(validation_results, output_dir)
    
    print(f"\n🎯 검증 완료!")
    print(f"📄 보고서: {report_path}")
    
    if not validation_results['valid']:
        sys.exit(1)

if __name__ == "__main__":
    main() 