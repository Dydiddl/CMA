#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 분할 실행 스크립트 (부문/장/페이지별)
"""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import argparse

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.split.pdf_split_utils import PDFSplitUtils
from src.utils.report import generate_split_report, generate_section_report

def main():
    parser = argparse.ArgumentParser(description="PDF 분할 실행 스크립트")
    parser.add_argument('--json', type=str, required=True, help='목차 JSON 파일 경로')
    parser.add_argument('--pdf', type=str, required=True, help='분할할 PDF 파일 경로')
    parser.add_argument('--mode', type=str, choices=['section', 'chapter', 'page'], default='chapter', help='분할 기준')
    parser.add_argument('--output', type=str, default='output/split_pdfs', help='출력 디렉토리')
    args = parser.parse_args()

    json_file = Path(args.json)
    pdf_file = Path(args.pdf)
    output_dir = Path(args.output)

    print(f"🚀 PDF 분할 시작 (mode: {args.mode})")
    print(f"- 목차 JSON: {json_file}")
    print(f"- 원본 PDF: {pdf_file}")
    print(f"- 출력 디렉토리: {output_dir}")

    splitter = PDFSplitUtils(json_file, pdf_file, output_dir)
    success = splitter.split(mode=args.mode)

    # 분할 결과 보고서 생성 (chapter/section 모드만)
    if args.mode in ['chapter', 'section']:
        analysis_report = splitter.get_analysis_report()
        chapters_by_section = analysis_report.get('chapters_by_section', {})
        # 성공/실패 카운트는 split 내에서만 출력하므로, 여기선 전체 개수만 보고
        if args.mode == 'chapter':
            generate_split_report(chapters_by_section, 0, 0, pdf_file, json_file, output_dir)
        elif args.mode == 'section':
            report_lines = []
            for section, chapters in chapters_by_section.items():
                report_lines.append(f"{section}: {len(chapters)}개 장")
            generate_section_report(report_lines, 0, pdf_file, json_file, output_dir)

    if success:
        print("\n🎉 PDF 분할이 성공적으로 완료되었습니다!")
    else:
        print("\n⚠️ 일부 분할 작업에서 오류가 발생했습니다.")

if __name__ == "__main__":
    main() 