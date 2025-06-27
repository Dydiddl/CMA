#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
목차 구조 분석 모듈 (TOC Structure Analyzer) - 개선된 버전

이 모듈은 추출된 목차의 구조를 분석하고 검증하는 기능을 제공합니다.
정답 데이터와 일치하는 형태로 목차를 추출하도록 개선되었습니다.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import traceback

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 분리된 모듈들 import
from .section_extractor import SectionExtractor
from .chapter_extractor import ChapterExtractor

# 공통 모듈 import
from src.common.constants import TOC_PATTERNS, DEFAULT_SECTIONS
from src.common.types import TOCEntry, TOCStructure
from src.common.utils import normalize_text, extract_chapter_info, clean_text, extract_page_number, determine_section

# 로거 초기화
logger = get_logger("TOCStructureAnalyzer")

class TOCStructureAnalyzer:
    """목차 구조 분석 클래스 - 개선된 버전"""
    
    def __init__(self):
        self.default_sections = DEFAULT_SECTIONS.copy()
        self.toc_patterns = TOC_PATTERNS
        self.section_extractor = SectionExtractor()
        self.chapter_extractor = ChapterExtractor()
        
        # 개선된 패턴 정의
        self.improved_patterns = {
            # 장 패턴: "제n장 제목" 형태
            "chapter": re.compile(r'^(\d+)줄:\s*제(\d+)장\s+(.+?)\s*·+\s*(\d+)$'),
            # 절 패턴: "n-n 제목" 형태
            "section": re.compile(r'^(\d+)줄:\s*(\d+-\d+)\s+(.+?)\s*·+\s*(\d+)$'),
            # 조/항목 패턴: "n-n-n 제목" 형태
            "item": re.compile(r'^(\d+)줄:\s*(\d+-\d+-\d+)\s+(.+?)\s*·+\s*(\d+)$'),
            # 기타 항목 패턴
            "other": re.compile(r'^(\d+)줄:\s*(.+?)\s*·+\s*(\d+)$')
        }
    
    def analyze_toc_structure(self, content: str, method: str = "improved") -> TOCStructure:
        """목차 구조 분석 - 개선된 방법 사용"""
        try:
            logger.info(f"목차 구조 분석 시작 (방법: {method})")
            
            # 개선된 추출 방법 사용
            if method == "improved":
                entries = self._extract_toc_entries_improved(content)
            else:
                entries = self._extract_toc_entries(content)
            
            logger.info(f"추출된 목차 항목 수: {len(entries)}")
            
            # 구조 생성
            structure = TOCStructure(
                entries=entries,
                sections=self._group_by_sections(entries),
                metadata={
                    "total_items": len(entries),
                    "analysis_method": method,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            logger.info("목차 구조 분석 완료")
            return structure
            
        except Exception as e:
            logger.error(f"목차 구조 분석 중 오류 발생: {e}\n{traceback.format_exc()}")
            return TOCStructure(
                entries=[],
                sections={},
                metadata={
                    "total_items": 0,
                    "analysis_method": method,
                    "error": str(e)
                }
            )
    
    def _extract_toc_entries_improved(self, content: str) -> List[TOCEntry]:
        """개선된 목차 항목 추출 - 실제 PDF 패턴에 맞춤"""
        entries = []
        lines = content.split('\n')
        
        current_section = "공통부문"
        current_chapter = ""
        chapter_title = ""
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith('===') or line.startswith('----'):
                i += 1
                continue
            
            # 줄 번호 제거 (예: "6줄: 제1장" -> "제1장")
            if '줄:' in line:
                line = line.split('줄:', 1)[1].strip()
            
            # 부문 확인
            if "공 통 부 문" in line:
                current_section = "공통부문"
                i += 1
                continue
            elif "토 목 부 문" in line:
                current_section = "토목부문"
                i += 1
                continue
            elif "건 축 부 문" in line:
                current_section = "건축부문"
                i += 1
                continue
            elif "기 계 설 비 부 문" in line:
                current_section = "기계설비부문"
                i += 1
                continue
            elif "유 지 관 리 부 문" in line:
                current_section = "유지관리부문"
                i += 1
                continue
            
            # 장 번호 패턴 (예: "제1장")
            chapter_match = re.match(r'^제(\d+)장$', line)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                current_chapter = f"제{chapter_num}장"
                
                # 다음 줄에서 장 제목과 페이지 번호 찾기
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if '줄:' in next_line:
                        next_line = next_line.split('줄:', 1)[1].strip()
                    
                    # 장 제목과 페이지 번호 추출
                    title_page_match = re.match(r'^(.+?)\s*[·\s]*(\d+)?$', next_line)
                    if title_page_match:
                        title = title_page_match.group(1).strip()
                        page = int(title_page_match.group(2)) if title_page_match.group(2) else 0
                        full_title = f"{current_chapter} {title}"
                        
                        print(f"[CHAPTER] {full_title} (p.{page})")
                        
                        entry = TOCEntry(
                            number=current_chapter,
                            title=full_title,
                            page=page,
                            level=1,
                            section=current_section,
                            type="chapter"
                        )
                        entries.append(entry)
                        i += 2  # 장 번호와 제목 줄을 모두 처리
                        continue
                
                i += 1
                continue
            
            # 항목 번호 패턴 (예: "1-1", "1-1-1")
            item_match = re.match(r'^(\d+(-\d+)*)$', line)
            if item_match:
                number = item_match.group(1)
                
                # 다음 줄에서 항목 제목과 페이지 번호 찾기
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if '줄:' in next_line:
                        next_line = next_line.split('줄:', 1)[1].strip()
                    
                    # 항목 제목과 페이지 번호 추출
                    title_page_match = re.match(r'^(.+?)\s*[·\s]*(\d+)?$', next_line)
                    if title_page_match:
                        title = title_page_match.group(1).strip()
                        page = int(title_page_match.group(2)) if title_page_match.group(2) else 0
                        level = number.count('-') + 2  # 1-1은 level 2, 1-1-1은 level 3
                        
                        print(f"[ITEM] {number} {title} (p.{page})")
                        
                        entry = TOCEntry(
                            number=number,
                            title=title,
                            page=page,
                            level=level,
                            section=current_section,
                            type="item"
                        )
                        entries.append(entry)
                        i += 2  # 항목 번호와 제목 줄을 모두 처리
                        continue
                
                i += 1
                continue
            
            # 기타 항목 (참고자료, 부록 등)
            other_match = re.match(r'^(.+?)\s*[·\s]*(\d+)?$', line)
            if other_match and len(line.strip()) > 3:
                title = other_match.group(1).strip()
                page = int(other_match.group(2)) if other_match.group(2) else 0
                
                # 목차 머릿말 제외
                if title in ["목", "차", "목 차", "목  차"] or title.isdigit():
                    i += 1
                    continue
                
                print(f"[OTHER] {title} (p.{page})")
                
                entry = TOCEntry(
                    number="",
                    title=title,
                    page=page,
                    level=0,
                    section=current_section,
                    type="other"
                )
                entries.append(entry)
            
            i += 1
        
        return entries
    
    def _extract_toc_entries(self, content: str) -> List[TOCEntry]:
        """기본 목차 항목 추출"""
        entries = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 각 패턴에 대해 매칭 시도
            for pattern_name, pattern in self.improved_patterns.items():
                match = pattern.match(line)
                if match:
                    if pattern_name == "chapter":
                        line_num, chapter_num, title, page = match.groups()
                        entry = TOCEntry(
                            number=f"제{chapter_num}장",
                            title=title.strip(),
                            page=int(page),
                            level=1,
                            section=self._determine_section(title),
                            type="chapter"
                        )
                    elif pattern_name == "section":
                        line_num, number, title, page = match.groups()
                        entry = TOCEntry(
                            number=number,
                            title=title.strip(),
                            page=int(page),
                            level=2,
                            section=self._determine_section(title),
                            type="section"
                        )
                    elif pattern_name == "item":
                        line_num, number, title, page = match.groups()
                        entry = TOCEntry(
                            number=number,
                            title=title.strip(),
                            page=int(page),
                            level=3,
                            section=self._determine_section(title),
                            type="item"
                        )
                    elif pattern_name == "other":
                        line_num, title, page = match.groups()
                        entry = TOCEntry(
                            number="",
                            title=title.strip(),
                            page=int(page),
                            level=0,
                            section="기타",
                            type="other"
                        )
                    
                    entries.append(entry)
                    break
        
        return entries
    
    def _determine_section(self, title: str) -> str:
        """제목으로부터 부문 결정"""
        title_lower = title.lower()
        
        if any(keyword in title_lower for keyword in ["토목", "도로", "교량", "터널", "하천"]):
            return "토목부문"
        elif any(keyword in title_lower for keyword in ["건축", "건물", "시설"]):
            return "건축부문"
        elif any(keyword in title_lower for keyword in ["기계", "설비", "전기", "통신"]):
            return "기계설비부문"
        elif any(keyword in title_lower for keyword in ["유지", "관리", "보수"]):
            return "유지관리부문"
        else:
            return "공통부문"
    
    def _group_by_sections(self, entries: List[TOCEntry]) -> Dict[str, Dict[str, Any]]:
        """부문별로 그룹화"""
        sections = {}
        for entry in entries:
            section = entry.section
            if section not in sections:
                sections[section] = {
                    "entries": [],
                    "total_items": 0,
                    "chapters": [],
                    "start_page": None,
                    "end_page": None
                }
            sections[section]["entries"].append(entry)
            sections[section]["total_items"] += 1
            
            # 페이지 범위 업데이트
            if sections[section]["start_page"] is None or entry.page < sections[section]["start_page"]:
                sections[section]["start_page"] = entry.page
            if sections[section]["end_page"] is None or entry.page > sections[section]["end_page"]:
                sections[section]["end_page"] = entry.page
            
            # 장 정보 추가
            if entry.type == "chapter":
                sections[section]["chapters"].append({
                    "number": entry.number,
                    "title": entry.title,
                    "page": entry.page
                })
        
        return sections
    
    def _group_by_chapters(self, entries: List[TOCEntry]) -> Dict[str, List[TOCEntry]]:
        """장별로 그룹화"""
        chapters = {}
        for entry in entries:
            if entry.type == "chapter":
                chapter_key = entry.number
                if chapter_key not in chapters:
                    chapters[chapter_key] = []
                chapters[chapter_key].append(entry)
        return chapters
    
    def _extract_page_number(self, line: str) -> int:
        """페이지 번호 추출"""
        # 점선 뒤의 페이지 번호 패턴
        page_match = re.search(r'[·\s]*(\d+)$', line)
        if page_match:
            return int(page_match.group(1))
        
        # 일반적인 페이지 번호 패턴
        page_match = re.search(r'(\d+)$', line)
        if page_match:
            return int(page_match.group(1))
        
        return 0 