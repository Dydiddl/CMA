#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
장/절 추출 모듈 (Chapter Extractor)

이 모듈은 목차에서 장과 절을 추출하는 기능을 제공합니다.
"""

import re
import logging
from typing import Optional, Tuple, List
from src.common.types import TOCEntry

logger = logging.getLogger(__name__)

class ChapterExtractor:
    """장/절 추출 클래스"""
    
    def __init__(self):
        # 실제 데이터 형식에 맞는 패턴으로 수정
        # 장: "제1장" + 다음 줄에 제목 + "····" + 페이지번호
        self.chapter_pattern = re.compile(r'제(\d+)장')
        self.chapter_title_pattern = re.compile(r'([가-힣A-Za-z0-9\-\s]+?)\s*·+\s*(\d+)')
        self.subsection_pattern = re.compile(r'(\d+)-(\d+)\s+([가-힣A-Za-z0-9\-\s]+?)\s*·+\s*(\d+)')
        self.item_pattern = re.compile(r'(\d+)-(\d+)-(\d+)\s+([가-힣A-Za-z0-9\-\s]+?)\s*·+\s*(\d+)')
    
    def extract_chapter(self, lines: List[str], current_index: int) -> Optional[Tuple[TOCEntry, int]]:
        """장 추출 (두 줄 처리)"""
        if current_index >= len(lines):
            return None
            
        line = lines[current_index].strip()
        match = self.chapter_pattern.search(line)
        
        if match:
            chapter_num = match.group(1)
            
            # 다음 줄에서 제목과 페이지 번호 찾기
            if current_index + 1 < len(lines):
                next_line = lines[current_index + 1].strip()
                title_match = self.chapter_title_pattern.search(next_line)
                
                if title_match:
                    title, page = title_match.groups()
                    return TOCEntry(
                        number=f"제{chapter_num}장",
                        title=title.strip(),
                        level=1,
                        page=int(page),
                        section="",
                        chapter=f"제{chapter_num}장",
                        parent=None,
                        children=[],
                        subsection=""
                    ), current_index + 2  # 다음 줄까지 처리했으므로 인덱스 +2
            
            # 제목을 찾지 못한 경우
            return TOCEntry(
                number=f"제{chapter_num}장",
                title="",
                level=1,
                page=0,
                section="",
                chapter=f"제{chapter_num}장",
                parent=None,
                children=[],
                subsection=""
            ), current_index + 1
        
        return None
    
    def extract_subsection(self, line: str) -> Optional[TOCEntry]:
        """절 추출"""
        match = self.subsection_pattern.search(line.strip())
        if match:
            subsection_num1, subsection_num2, title, page = match.groups()
            subsection_num = f"{subsection_num1}-{subsection_num2}"
            return TOCEntry(
                number=subsection_num,
                title=title.strip(),
                level=2,
                page=int(page),
                section="",
                chapter="",
                parent=None,
                children=[],
                subsection=subsection_num
            )
        return None
    
    def extract_item(self, line: str) -> Optional[TOCEntry]:
        """조/항목 추출"""
        match = self.item_pattern.search(line.strip())
        if match:
            item_num1, item_num2, item_num3, title, page = match.groups()
            item_num = f"{item_num1}-{item_num2}-{item_num3}"
            return TOCEntry(
                number=item_num,
                title=title.strip(),
                level=3,
                page=int(page),
                section="",
                chapter="",
                parent=None,
                children=[],
                subsection=""
            )
        return None
    
    def extract_any(self, line: str) -> Optional[TOCEntry]:
        """절/조 중 하나 추출 (장은 별도 처리)"""
        # 절 추출 시도
        entry = self.extract_subsection(line)
        if entry:
            return entry
        
        # 조/항목 추출 시도
        entry = self.extract_item(line)
        if entry:
            return entry
        
        return None 