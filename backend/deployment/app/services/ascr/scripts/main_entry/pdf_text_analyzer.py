#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 텍스트 분석기 - 목차 형식 파악용
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.file_paths import FilePathManager, get_standard_price_pdf_path, validate_year


def analyze_pdf_text(pdf_path: Path) -> Dict[str, Any]:
    """PDF 텍스트 분석"""
    try:
        from pypdf import PdfReader
        
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # 텍스트 분석
        analysis = {
            "total_length": len(text),
            "lines": text.split('\n'),
            "line_count": len(text.split('\n')),
            "potential_toc_lines": [],
            "patterns_found": {}
        }
        
        # 목차 관련 패턴 검색
        patterns = {
            "chapter": r'제\d+장',
            "section": r'\d+-\d+',
            "subsection": r'\d+-\d+-\d+',
            "page_number": r'···\s*\d+',
            "line_number": r'^\d+줄:',
            "bullet": r'^\s*[-•]\s*',
            "number_dot": r'^\d+\.'
        }
        
        lines = text.split('\n')
        for i, line in enumerate(lines[:100]):  # 처음 100줄만 분석
            line = line.strip()
            if not line:
                continue
            
            # 패턴 매칭
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, line):
                    if pattern_name not in analysis["patterns_found"]:
                        analysis["patterns_found"][pattern_name] = []
                    analysis["patterns_found"][pattern_name].append({
                        "line_num": i + 1,
                        "content": line[:100] + "..." if len(line) > 100 else line
                    })
            
            # 잠재적 목차 라인 식별
            if any(keyword in line for keyword in ['장', '절', '조', '···', '페이지']):
                analysis["potential_toc_lines"].append({
                    "line_num": i + 1,
                    "content": line[:100] + "..." if len(line) > 100 else line
                })
        
        return analysis
        
    except Exception as e:
        return {"error": str(e)}


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="PDF 텍스트 분석기")
    parser.add_argument("--year", type=int, help="분석할 년도 (기본값: 최신 년도)")
    parser.add_argument("--pdf", type=str, help="직접 PDF 파일 경로 지정")
    
    args = parser.parse_args()
    
    # PDF 파일 경로 결정
    if args.pdf:
        # 직접 지정된 PDF 파일 사용
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"❌ PDF 파일이 없습니다: {pdf_path}")
            return
        year_info = "직접 지정"
    else:
        # 년도 기반 PDF 파일 사용
        file_manager = FilePathManager()
        
        if args.year:
            if not validate_year(args.year):
                print(f"❌ 유효하지 않은 년도입니다: {args.year}")
                return
            year = args.year
        else:
            year = file_manager.get_latest_year()
        
        pdf_path = get_standard_price_pdf_path(year)
        if not pdf_path or not pdf_path.exists():
            print(f"❌ {year}년 표준품셈 PDF 파일이 없습니다")
            return
        year_info = f"{year}년"
    
    print(f"📄 PDF 텍스트 분석: {pdf_path.name} ({year_info})")
    print("=" * 60)
    
    analysis = analyze_pdf_text(pdf_path)
    
    if "error" in analysis:
        print(f"❌ 분석 오류: {analysis['error']}")
        return
    
    print(f"📊 분석 결과:")
    print(f"  - 총 텍스트 길이: {analysis['total_length']:,} 문자")
    print(f"  - 총 라인 수: {analysis['line_count']:,}줄")
    
    print(f"\n🔍 발견된 패턴:")
    for pattern_name, matches in analysis["patterns_found"].items():
        print(f"  - {pattern_name}: {len(matches)}개")
        for match in matches[:3]:  # 처음 3개만 출력
            print(f"    {match['line_num']}줄: {match['content']}")
        if len(matches) > 3:
            print(f"    ... (총 {len(matches)}개)")
    
    print(f"\n📋 잠재적 목차 라인:")
    for toc_line in analysis["potential_toc_lines"][:10]:  # 처음 10개만 출력
        print(f"  {toc_line['line_num']}줄: {toc_line['content']}")
    
    if len(analysis["potential_toc_lines"]) > 10:
        print(f"  ... (총 {len(analysis['potential_toc_lines'])}개)")


if __name__ == "__main__":
    main() 