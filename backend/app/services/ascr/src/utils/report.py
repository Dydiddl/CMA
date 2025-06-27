# -*- coding: utf-8 -*-
"""
보고서/로그 생성 유틸리티 (분석/분할/검증 결과)
"""
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

__all__ = [
    'generate_split_report',
    'generate_section_report'
]

def generate_processing_report(report_data: Dict[str, Any], report_path: Path) -> None:
    """
    처리 결과 보고서 생성
    
    Args:
        report_data: 보고서 데이터
        report_path: 보고서 파일 경로
    """
    report_lines = []
    report_lines.append("# 📋 PDF 처리 결과 보고서")
    report_lines.append(f"- 🕒 처리 시간: {report_data.get('processing_time', datetime.now().isoformat())}")
    report_lines.append(f"- 📄 입력 파일: {report_data.get('input_file', 'N/A')}")
    report_lines.append(f"- 📂 출력 디렉토리: {report_data.get('output_dir', 'N/A')}")
    report_lines.append(f"- 🔧 분할 모드: {report_data.get('split_mode', 'N/A')}")
    report_lines.append(f"- 📋 추출 방법: {report_data.get('extraction_method', 'N/A')}")
    report_lines.append(f"- 📊 목차 항목 수: {report_data.get('toc_entries_count', 0)}개")
    report_lines.append("")
    
    report_lines.append("## 📁 생성된 파일들")
    if report_data.get('toc_json_path'):
        report_lines.append(f"- 목차 구조: {report_data.get('toc_json_path')}")
    if report_data.get('mapping_path'):
        report_lines.append(f"- 매핑 설정: {report_data.get('mapping_path')}")
    
    report_lines.append("")
    report_lines.append("## ✅ 처리 완료")
    report_lines.append("모든 작업이 성공적으로 완료되었습니다.")
    
    # 보고서 파일 저장
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"📄 처리 결과 보고서가 저장되었습니다: {report_path}")

def generate_split_report(chapters_by_section: Dict[str, List[Dict]], success_count: int, error_count: int, pdf_file_path: Path, json_file_path: Path, output_dir: Path) -> None:
    """PDF 분할 결과 보고서 생성"""
    report_lines = []
    report_lines.append(f"# 📋 PDF 분할 결과 보고서\n")
    report_lines.append(f"- 📄 원본 PDF: {pdf_file_path}")
    report_lines.append(f"- 📑 목차 JSON: {json_file_path}")
    report_lines.append(f"- 📁 출력 디렉토리: {output_dir}")
    report_lines.append(f"- 🕒 분할 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"## 📊 부문/장별 분할 결과\n")
    for section_name, chapters in chapters_by_section.items():
        report_lines.append(f"### {section_name} ({len(chapters)}개 장)")
        for chapter in chapters:
            title = chapter.get('title', '')
            start_page = chapter.get('start_page', chapter.get('page', '?'))
            end_page = chapter.get('end_page', '?')
            report_lines.append(f"- {title} (p.{start_page}-{end_page})")
        report_lines.append("")
    report_lines.append(f"## ✅ 성공: {success_count}개 | ❌ 실패: {error_count}개\n")
    report_path = output_dir / f"split_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"📄 분할 결과 보고서가 저장되었습니다: {report_path}")

def generate_section_report(report_lines: List[str], total_files_created: int, pdf_file_path: Path, json_file_path: Path, output_dir: Path) -> None:
    """부문별 PDF 분할 결과 보고서 생성"""
    report = f"""# 📋 PDF 부문별 분할 결과 보고서
- 📄 원본 PDF: {pdf_file_path}
- 📑 목차 JSON: {json_file_path}
- 📁 출력 디렉토리: {output_dir}
- 🕒 분할 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 부문별 파일 생성 결과
"""
    report += '\n'.join(report_lines)
    report += f"\n총 생성된 파일 수: {total_files_created}\n"
    report_path = output_dir / f"section_split_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"📄 부문별 분할 결과 보고서가 저장되었습니다: {report_path}")

def generate_validation_report(validation_results: Dict[str, Any], output_dir: Path) -> None:
    """검증 결과 보고서 생성"""
    report_lines = []
    report_lines.append(f"# 📋 검증 결과 보고서\n")
    report_lines.append(f"- 🕒 검증 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"## ✅ 검증 결과\n")
    if validation_results.get('validation_passed', False):
        report_lines.append("- ✅ 모든 부문이 정상적으로 발견되었습니다.")
    else:
        report_lines.append("- ❌ 일부 부문이 누락되었습니다.")
        missing = validation_results.get('missing_sections', [])
        if missing:
            report_lines.append(f"- 누락된 부문: {', '.join(missing)}")
    report_lines.append(f"- 부문 순서: {' → '.join(validation_results.get('section_order', []))}")
    report_path = output_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"📄 검증 결과 보고서가 저장되었습니다: {report_path}") 