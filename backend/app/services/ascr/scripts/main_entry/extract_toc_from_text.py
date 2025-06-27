#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
목차 텍스트에서 구조 추출 스크립트

이 스크립트는 제공된 목차 텍스트를 분석하여 구조화된 JSON 형태로 변환합니다.
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import argparse

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.types import TOCEntry, TOCStructure
from src.common.constants import SECTION_MAPPING
from src.utils.log import get_logger

logger = get_logger(__name__)

class TextTOCExtractor:
    """텍스트 목차 추출 클래스"""
    
    def __init__(self):
        # 부문 패턴
        self.section_pattern = re.compile(r'^([가-힣\s]+부문)$')
        
        # 장 패턴 (제1장 적용기준 3)
        self.chapter_pattern = re.compile(r'^제(\d+)장\s+([가-힣A-Za-z0-9\-\s\(\)]+)\s+(\d+)$')
        
        # 절 패턴 (1-1 일반사항 3)
        self.section_item_pattern = re.compile(r'^(\d+)-(\d+)\s+([가-힣A-Za-z0-9\-\s\(\)]+)\s+(\d+)$')
        
        # 조/항목 패턴 (1-1-1 목적 3)
        self.subsection_pattern = re.compile(r'^(\d+)-(\d+)-(\d+)\s+([가-힣A-Za-z0-9\-\s\(\)]+)\s+(\d+)$')
        
        # 들여쓰기 기반 계층 구조
        self.indent_pattern = re.compile(r'^(\s*)(.+)$')
        
        # 특수 매핑 규칙
        self.special_mapping = {
            "제2장 가설공사": "공통부문"  # 가설공사는 공통부문에 포함
        }
    
    def extract_toc_structure(self, content: str) -> TOCStructure:
        """목차 구조 추출"""
        entries = []
        lines = content.split('\n')
        current_section = None
        current_chapter = None
        parent_stack = []
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 들여쓰기 레벨 확인
            indent_match = self.indent_pattern.match(line)
            if not indent_match:
                continue
            
            indent_level = len(indent_match.group(1))
            content_text = indent_match.group(2)
            
            # 부문 추출
            section_match = self.section_pattern.match(content_text)
            if section_match:
                section_name = section_match.group(1).strip()
                current_section = section_name
                
                entry = TOCEntry(
                    number=section_name,
                    title=section_name,
                    level=0,
                    page=0,
                    section=section_name,
                    chapter="",
                    parent=None,
                    children=[],
                    subsection=""
                )
                entries.append(entry)
                parent_stack = [entry]
                continue
            
            # 장 추출
            chapter_match = self.chapter_pattern.match(content_text)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_title = chapter_match.group(2).strip()
                page_num = int(chapter_match.group(3))
                
                # 부문 매핑
                section = self._determine_section(f"제{chapter_num}장 {chapter_title}")
                
                entry = TOCEntry(
                    number=f"제{chapter_num}장",
                    title=chapter_title,
                    level=1,
                    page=page_num,
                    section=section,
                    chapter=f"제{chapter_num}장",
                    parent=current_section,
                    children=[],
                    subsection=""
                )
                
                # 부모-자식 관계 설정
                if parent_stack and parent_stack[0].level == 0:
                    parent_stack[0].children.append(entry.number)
                
                entries.append(entry)
                current_chapter = entry
                parent_stack = [parent_stack[0], entry] if parent_stack else [entry]
                continue
            
            # 절 추출
            section_match = self.section_item_pattern.match(content_text)
            if section_match:
                section_num1 = section_match.group(1)
                section_num2 = section_match.group(2)
                section_title = section_match.group(3).strip()
                page_num = int(section_match.group(4))
                
                entry = TOCEntry(
                    number=f"{section_num1}-{section_num2}",
                    title=section_title,
                    level=2,
                    page=page_num,
                    section=current_section,
                    chapter=current_chapter.number if current_chapter else "",
                    parent=current_chapter.number if current_chapter else None,
                    children=[],
                    subsection=f"{section_num1}-{section_num2}"
                )
                
                # 부모-자식 관계 설정
                if current_chapter:
                    current_chapter.children.append(entry.number)
                
                entries.append(entry)
                parent_stack = parent_stack[:2] + [entry] if len(parent_stack) >= 2 else parent_stack + [entry]
                continue
            
            # 조/항목 추출
            subsection_match = self.subsection_pattern.match(content_text)
            if subsection_match:
                item_num1 = subsection_match.group(1)
                item_num2 = subsection_match.group(2)
                item_num3 = subsection_match.group(3)
                item_title = subsection_match.group(4).strip()
                page_num = int(subsection_match.group(5))
                
                entry = TOCEntry(
                    number=f"{item_num1}-{item_num2}-{item_num3}",
                    title=item_title,
                    level=3,
                    page=page_num,
                    section=current_section,
                    chapter=current_chapter.number if current_chapter else "",
                    parent=f"{item_num1}-{item_num2}",
                    children=[],
                    subsection=f"{item_num1}-{item_num2}"
                )
                
                # 부모-자식 관계 설정
                parent_number = f"{item_num1}-{item_num2}"
                for parent_entry in entries:
                    if parent_entry.number == parent_number:
                        parent_entry.children.append(entry.number)
                        break
                
                entries.append(entry)
                continue
        
        # 부문별 통계 생성
        sections = self._generate_section_stats(entries)
        
        return TOCStructure(
            entries=entries,
            sections=sections,
            metadata={
                "extraction_method": "text_structure",
                "total_entries": len(entries),
                "sections_count": len(sections),
                "extraction_time": datetime.now().isoformat()
            }
        )
    
    def _determine_section(self, chapter_title: str) -> str:
        """장 제목으로부터 부문 결정"""
        # 특수 매핑 우선 확인
        if chapter_title in self.special_mapping:
            return self.special_mapping[chapter_title]
        
        # 기본 매핑 확인
        if chapter_title in SECTION_MAPPING:
            return SECTION_MAPPING[chapter_title]
        
        # 키워드 기반 분류
        if "가설" in chapter_title:
            return "공통부문"
        elif "적용기준" in chapter_title:
            return "공통부문"
        
        return "미분류"
    
    def _generate_section_stats(self, entries: List[TOCEntry]) -> Dict[str, Any]:
        """부문별 통계 생성"""
        sections = {}
        
        for entry in entries:
            section = entry.section or "미분류"
            if section not in sections:
                sections[section] = {
                    "count": 0,
                    "entries": [],
                    "pages": [],
                    "chapters": []
                }
            
            sections[section]["count"] += 1
            sections[section]["entries"].append(entry.number)
            
            if entry.page > 0:
                sections[section]["pages"].append(entry.page)
            
            if entry.level == 1:  # 장 레벨
                sections[section]["chapters"].append(entry.number)
        
        return sections

def main():
    parser = argparse.ArgumentParser(description="텍스트에서 목차 추출")
    parser.add_argument("--input_file", type=str, default="input/By_year_Construction_work_standard_price_list/index.pdf", help="입력 PDF 파일 경로")
    args = parser.parse_args()
    input_file = Path(args.input_file)
    
    print("📖 목차 텍스트 분석 시작...")
    
    if not input_file.exists():
        print(f"❌ 입력 파일을 찾을 수 없습니다: {input_file}")
        return
    
    try:
        # PDF에서 텍스트 추출
        from src.utils.extract.pdf_text_extractor import PDFTextExtractor
        extractor = PDFTextExtractor()
        content = extractor.extract_text_by_pages(input_file)
        
        print(f"📄 파일 크기: {len(content)} 문자")
        print(f"📄 추출된 텍스트 샘플:")
        print(content[:500])
        print("..." if len(content) > 500 else "")
        
        # 목차 구조 추출
        toc_extractor = TextTOCExtractor()
        toc_structure = toc_extractor.extract_toc_structure(content)
        
        if not toc_structure.entries:
            print("❌ 목차 구조를 추출할 수 없습니다. (entries=0)")
            print("[DEBUG] content 샘플 (처음 10줄만):")
            for i, line in enumerate(content.split('\n')[:10], 1):
                print(f"{i}: {line}")
            return
        
        print(f"✅ 목차 구조 추출 완료")
        print(f"📊 총 항목 수: {len(toc_structure.entries)}")
        print(f"📁 부문 수: {len(toc_structure.sections)}")
        
        # 부문별 통계 출력
        print("\n📋 부문별 통계:")
        for section_name, stats in toc_structure.sections.items():
            print(f"  {section_name}: {stats.get('total_entries', 0)}개 항목, {stats.get('chapters_count', 0)}개 장")
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path("output") / f"toc_structure_text_{timestamp}.json"
        output_file.parent.mkdir(exist_ok=True)
        
        # JSON 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(toc_structure.to_dict(), f, ensure_ascii=False, indent=2)
        
        print(f"💾 JSON 파일 저장: {output_file}")
        
        # 마크다운 출력
        markdown_file = output_file.with_suffix('.md')
        markdown_content = generate_markdown_output(toc_structure)
        
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"📝 마크다운 출력 완료: {markdown_file}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 